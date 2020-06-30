/**
* File: leapfrog.c
* Author: Mark Redd
* Email: redddogjr@gmail.com
* Website: http://www.r3eda.com/
* About:
* This is the entire leapfrog-in-C method. It is coded such that it may be
* linked using "leapfrog.h" or compiled as a shared library (i.e. '.dll', '.so' 
* etc.). The code is explained with each function but the only functions
* and variables that are meant to be availble for export are minimize and 
* N_RESULTS. The rest are helper functions for the optimizaition algorithm.
* 
* This algorithm is based the Leapfrogging Optimization Algorithm published 
* by Dr. R. Russell Rhinehart. The following publications explain the technique:
* 
* - Rhinehart, R. R., M. Su, and U. Manimegalai-Sridhar, “Leapfrogging and 
*   Synoptic Leapfrogging: a new optimization approach”, Computers & Chemical 
*   Engineering, Vol. 40, 11 May 2012, pp. 67-81.
* 
* - Manimegalai-Sridhar, U., A. Govindarajan, and R. R. Rhinehart, “Improved 
*   Initialization of Players in Leapfrogging Optimization”, Computers & 
*   Chemical Engineering, Vol. 60, 2014, 426-429.
* 
* - Rhinehart, R. R., “Convergence Criterion in Optimilsation of Stochastic 
*   Processes”, Computers & Chemical Engineering, Vol. 68, 4 Sept 2014, pp 1-6.
*/

#include <stdlib.h>
#include <time.h>
#include <math.h>

#include "dbg.h"

#ifdef OUT_EXE
    #include "leapfrog.h"
#endif

const size_t N_RESULTS = 7;


typedef struct {

    double (*f)(double* x, size_t xlen);   // the objective function
    double (*g)(double* x, size_t xlen);   // the constraint function
    size_t xlen;            // the number of args in f and g
    size_t points;          // the number of points for optimization

    double* lower;          // the lower bounds; length = xlen
    double* upper;          // the upper bounds; length = xlen
    double** pointset;      // point set; shape = (points, xlen)
    int free_pointset;      // (bool) free the pointset when done?
    double* objs;           // the objective function values; length = points

    size_t* discrete;       // array of discrete indices
    size_t discretelen;     // length of discrete

    size_t nfev;            // number of function evaluations
    double maxcv;           // maximum constraint violation

    size_t besti;           // the index of the best point
    size_t worsti;          // the index of the worst point
    double error;           // the value of the convergence error
    double tol;             // convergence tolerance
    double big;             // punishing number. A big, positive number.

} leapfrog_data;


double uniform(double lower, double upper)
{
/**
* @returns a random double between
* @param lower and @param upper following a
* uniform distribution.
*/
    check(lower <= upper, "Invalid input! %f, %f", lower, upper);
    double frac = 1.0 * rand() / RAND_MAX;
    return (upper - lower) * frac + lower;

error:
    return 0.0;
}


double** zeros(size_t rows, size_t columns)
{
/**
* Allocs a 2d array initialized with zeros. 
* Returns a pointer to the array.
*/
    check(rows > 0 && columns > 0,
        "'rows' and 'columns' must be greater than 0.");
    size_t i;
    size_t j;
    double**  the_array = (double**)  malloc(rows*sizeof(double*));

    for (i = 0; i < rows; i++){
        the_array[i] = (double*) malloc(columns*sizeof(double));
        for (j = 0; j < columns; j++){
            the_array[i][j] = 0.0;
        }
    }

    return the_array;

error:
    return NULL;
}


void free_array_2d(double** array, size_t rows)
{
/**
* Frees all mallocs associated with @fuction zeros thereby freeing
* @param array.
*/
    for (size_t i = 0; i < rows; i++){
        if (array[i]) free(array[i]);
    }
    if(array) free(array);
}


void free_data(leapfrog_data* self)
{
/**
* Frees all mallocs associated with @function init_leapfrog
* will free an allocated leapfrog_data struct.
*/
    if(self->objs) free(self->objs);
    if(self->pointset && self->free_pointset) 
            free_array_2d(self->pointset, self->points);
    if(self) free(self);
}


void eval_best_worst(leapfrog_data* self)
{
/**
* Evaluates and adjusts @param self's best and worst
* attributes to the best and worst indices in the pointset.
*/
    for(size_t i = 0; i < self->points; i++){
        if(self->objs[i] < self->objs[self->besti]){
            self->besti = i;
        }
        if(self->objs[i] > self->objs[self->worsti]){
            self->worsti = i;
        }
    }
}


void enforce_discrete(leapfrog_data* self, size_t i, size_t j)
{
/**
* Enforces discrete variables by changing all applicable
* values to whole double values.
*/
    if(!self->discrete) return;
    for(size_t dis = 0; dis < self->discretelen; dis++){
        if(self->discrete[dis] == j){
            self->pointset[i][j] = (double)(int)self->pointset[i][j];
        }
    }
}


void enforce_constraints(leapfrog_data* self, size_t row)
{
/**
* Enforces the constraint penalties on any infeasible member of the
* point set. The penalty to any infeasible member is to be made worse
* than the worst member of the point set. This will ensure all
* infeasible members are eventually eliminated.
*
* If a constraint function is not specified, then this
* function does nothing.
*
* A constraint function must be designed to return a single
* value of the form:
*
* fconstraint(x) <= 0
*
* This means a return value > 0 from the constraint function
* indicates the constraint has been violated, otherwise the point
* is feasible.
*/
    if(!self->g) return;
    double big = 0.0, mbig, constraint_value;
    for(size_t i = 0; i < self->points; i++){
        mbig = fabs(self->objs[i]);
        if(mbig > big) big = mbig;
    }
    constraint_value = self->g(self->pointset[row], self->xlen);
    if(constraint_value > 0.0){
        if(constraint_value > self->maxcv) self->maxcv = constraint_value;
        self->objs[row] = big + constraint_value;
    }
}


void leapfrog(leapfrog_data* self)
{
/**
* Core step in the leapfrogging algorithm. Takes a best and worst
* index of the 'pointset' and generates a new point in place of
* the worst by "leapfrogging" over the point corresponding to the
* 'best' index.
*/
    double b1, b2;
    for(size_t j = 0; j < self->xlen; j++){
        b1 = self->pointset[self->besti][j];
        b2 = 2.0 * self->pointset[self->besti][j] -\
            self->pointset[self->worsti][j];
        if(b2 < b1){
            b1 = b1 + b2;
            b2 = b1 - b2;
            b1 = b1 - b2;
        }
        if(b1 < self->lower[j]) b1 = self->lower[j];
        if(b2 > self->upper[j]) b2 = self->upper[j];
        self->pointset[self->worsti][j] = uniform(b1, b2);
        enforce_discrete(self, self->worsti, j);
    }
    self->objs[self->worsti] = self->f(self->pointset[self->worsti], self->xlen);
    self->nfev++;
    enforce_constraints(self, self->worsti);
}


void calculate_convergence(leapfrog_data* self)
{
/**
* Calculates a convergence value by calculating the relative
* distance between the objective values of the best and
* worst points and average distance between each point and
* the best point and summing the two values together. This
* convergence value is taken as the error of the optimization
* and once the error <= tolerance the optimization ends.
*/
    double objective_best = self->objs[self->besti];
    double objective_worst = self->objs[self->worsti];
    double norm1, err_obj, dist_sum = 0.0, constraint_penalty = 0.0;

    if(fabs(objective_best) < self->tol) norm1 = self->tol;
    else norm1 = objective_best;
    err_obj = fabs((objective_worst - objective_best)/norm1);
    for(size_t i = 0; i < self->points; i++){
        if(self->g && self->g(self->pointset[i], self->xlen) > 0.0){
            constraint_penalty = 2.0 * self->tol;
        }
        for(size_t j = 0; j < self->xlen; j++){
            if(fabs(self->pointset[self->besti][j]) < self->tol){
                norm1 = self->tol;
            }
            else norm1 = self->pointset[self->besti][j];
            dist_sum += fabs(
                (self->pointset[self->besti][j] - self->pointset[i][j])/norm1);
        }
    }
    // log_info("\nERRS: obj: %f dst: %f", err_obj, dist_sum);
    self->error = err_obj + dist_sum + constraint_penalty;
}


void iterate(leapfrog_data* self)
{
/**
* Completes one iteration of the leapfrog optimization algorithm.
*/
    leapfrog(self);
    eval_best_worst(self);
    calculate_convergence(self);
}


leapfrog_data* init_leapfrog(double (*fptr)(double* x, size_t xlen), 
                            double* lower, double* upper, size_t xlen, size_t points,
                            double (*gptr)(double* x, size_t xlen), 
                            size_t* discrete, size_t discretelen, double tol,
                            double** pointset, int init_pointset)
{
/**
* Allocates memory for and initializes the main leapfrog_data struct
* to be used in the optimization.
*/
    leapfrog_data* self = (leapfrog_data*) malloc(sizeof(leapfrog_data));
    self->f = fptr;
    self->g = gptr;
    self->xlen = xlen;
    self->points = points;
    self->pointset = !pointset ? zeros(points, self->xlen + 1) : pointset;
    self->free_pointset = !pointset ? 1 : 0;
    self->objs = (double*) malloc(sizeof(double) * self->points);
    self->nfev = 0;
    self->maxcv = 0.0;
    self->besti = 0;
    self->worsti = 0;
    self->error = 100.0;
    self->lower = lower;
    self->upper = upper;
    self->discrete = discrete;
    self->discretelen = discretelen;
    self->tol = tol;

    if(discrete){
        for(size_t i = 0; i < discretelen; i++){
            self->lower[self->discrete[i]] = \
                ((double)(int)self->lower[self->discrete[i]]) +  0.999;
        }
    }
    for(size_t i = 0; i < self->points; i++){
        for(size_t j = 0; j < self->xlen; j++){
            if(!pointset || init_pointset)
                self->pointset[i][j] = uniform(self->lower[j], self->upper[j]);
            else self->pointset[i][j] = pointset[i][j];
            enforce_discrete(self, i, j);
        }
        self->objs[i] = self->f(self->pointset[i], self->xlen);
        self->nfev++;
    }
    eval_best_worst(self);
    for(size_t i = 0; i < self->points; i++){
        enforce_constraints(self, i);
    }
    eval_best_worst(self);
    return self;
}


void minimize(
        double (*fptr)(double*, size_t), double* lower, double* upper,
        size_t xlen, size_t points, double (*gptr)(double*, size_t),
        size_t* discrete, size_t discretelen, size_t maxit,
        double tol, size_t seedval, double** pointset,
        int init_pointset, void (*callback)(double*, size_t),
        double* solution)
{
/**
* Minimizes a function until the convergence criteria are
* satisfied or the number of iterations exceeds 'maxit'.
* The LeapFrog minimizer takes the following parameters:
* - fptr          : pointer to objective function with signature
*                   double fptr(double*)
* - lower         : variable lower bounds
* - upper         : variable upper bounds
* - xlen          : number of variables, should correspond to the lengths
*                   of lower, upper and the array passed into fptr
* - points        : point set size
* - gptr          : pointer to the constraint function with signature
*                   double gptr(double*, size_t). Must return a value <= 0.0 
*                   when all constraints are satisfied. gptr returning a value
*                   > 0.0 will make the optimizer punish that point. NULL may 
*                   be passed in to indicate unconstrained optimization
* - discrete      : size_t array of indices that correspond to
*                   discrete variables. These variables
*                   will be constrained to integer values
*                   by truncating any randomly generated
*                   number (i.e. rounding down to the
*                   nearest integer absolute value)
*                   bounds are automatically adjusted to ensure
*                   the bounded space remains the same
* - maxit         : maximum iterations
* - tol           : convergence tolerance
* - seedval       : random seed
* - pointset      : starting point set of shape (points, xlen); 
                    if given, it will be changed.
* - init_pointset : (bool) flag to say whether to use the given pointset
                    or to reinitialize the pointset before optimizing.
* - callback      : function to be called after each iteration; has
*                   signature: void callback(double*)
* - solution      : double array of length = xlen + 6 to which output
*                   is copied.
*
* ## Returns
* Optimization output is copied to solution which is a double array
* of length = xlen + N_RESULTS where the elements are (in order):
*  - solution[0], solution[1] ... solution[xlen - 1]: the optimized inputs
*  - solution[xlen]: a status code indicating the success or error of the
*       optimization. Values are:
*           0 : optimization completed successfully
*           1 : the maximum number of iterations was exceeded
*           2 : another error occured
*  - solution[xlen + 1]: the objective function value at those inputs
*  - solution[xlen + 2]: the number of iterations (value should be a
*       whole number > 0 and <= maxit)
*   - solution[xlen + 3]: the final error of the optimization
*   - solution[xlen + 6]: the maximum constraint violation that occurred during
*       the optimization. If the function pointer is NULL then it is set to 0.0
*   - solution[xlen + 4]: the index of the best player
*   - solution[xlen + 5]: the index of the worst player
*/

/***************** SANITIZE INPUT ********************/
    leapfrog_data* self = NULL;
    check(
        fptr && lower && upper && xlen && points && maxit && tol && solution, 
        "Invalid NULL passed in."
    );
/***************** END SANITIZE INPUT ****************/
    size_t iters;

    if(seedval) srand(seedval);
    else srand(time(0));

    self = init_leapfrog(
        fptr, lower, upper, xlen, points, gptr, discrete, discretelen, 
        tol, pointset, init_pointset
    );
    for(iters = 1; iters <= maxit; iters++) {
        iterate(self);
        if(self->error < tol)  break;
        if(callback) callback(self->pointset[self->besti], self->xlen);
    }
    if(iters >= maxit) log_warn("Maximum iterations exceeded.");
    
    for(size_t i = 0; i < self->xlen; i++){
        solution[i] = self->pointset[self->besti][i];
    }
    solution[xlen + 0] = iters >= maxit ? 1.0 : 0.0; // opt exit status                        
    solution[xlen + 1] = self->objs[self->besti];    // best objective funciton value     
    solution[xlen + 2] = iters;                      // number of iterations
    solution[xlen + 3] = self->error;                // the final error
    solution[xlen + 4] = self->maxcv;                // the max constraint violaion
    solution[xlen + 5] = self->besti;                // the index of the best player
    solution[xlen + 6] = self->worsti;               // the index of the worst player
error:
    if(self) free_data(self);
}
