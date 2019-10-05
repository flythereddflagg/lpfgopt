#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <stdio.h>

#include "lpfgopt.h"
#include "dbg.h"


typedef struct {

    double (*f)(double*);   // the objective function
    double (*g)(double*);   // the constraint function
    size_t xlen;            // the number of args in f and g
    size_t points;          // the number of points for optimization

    double* lower;          // the lower bounds; length = xlen
    double* upper;          // the upper bounds; length = xlen
    double** pointset;      // point set shape = (points, xlen)
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


void cpy_data(double* src, double* dest, size_t len)
{
/**
* copies an array of length @param len from
* @param src to @param dest.
*/
    for(size_t i = 0; i < len; i++){
        dest[i] = src[i];
    }
}


double** zeros(size_t rows, size_t columns)
{
/**
* Allocs a 2d array initialized with zeros.
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
    if(self->pointset) free_array_2d(self->pointset, self->points);
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
    constraint_value = self->g(self->pointset[row]);
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
    self->objs[self->worsti] = self->f(self->pointset[self->worsti]);
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
    double obj_best = self->objs[self->besti];
    double obj_worst = self->objs[self->worsti];
    double norm1, err_obj, dist_sum = 0.0, constraint_penalty = 0.0;

    if(fabs(obj_best) < self->tol) norm1 = self->tol;
    else norm1 = obj_best;
    err_obj = fabs((obj_worst - obj_best)/norm1);
    for(size_t i = 0; i < self->points; i++){
        if(self->g && self->g(self->pointset[i]) > 0.0){
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


leapfrog_data* init_leapfrog(double (*fptr)(double*), double* lower,
                            double* upper, size_t xlen, size_t points,
                            double (*gptr)(double*), size_t* discrete,
                            size_t discretelen, double tol)
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
    self->pointset = zeros(points, self->xlen + 1);
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

    for(size_t i = 0; i < self->points; i++){
        for(size_t j = 0; j < self->xlen; j++){
            self->pointset[i][j] = uniform(self->lower[j], self->upper[j]);
            enforce_discrete(self, i, j);
        }
        self->objs[i] = self->f(self->pointset[i]);
        self->nfev++;
    }
    eval_best_worst(self);
    for(size_t i = 0; i < self->points; i++){
        enforce_constraints(self, i);
    }
    eval_best_worst(self);
    return self;
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


WINAPI void WINCALL minimize(
                double (*fptr)(double*), double* lower, double* upper,
                size_t xlen, size_t points, double (*gptr)(double*),
                size_t* discrete, size_t discretelen, size_t maxit,
                double tol, size_t seedval, double* best)
{
/**
* Minimizes a function until the convergence criteria are
* satisfied or the number of iterations exceeds
* 'maxit'.
* output is copied to "best" which is a double array of length = xlen + 6
* where the outputs are (in order):
*  - best[0], best[1] ... best[xlen - 1]: the optimized inputs
*  - best[xlen]: the objective function value at those inputs
*  - best[xlen + 1]: a status code indicating the success or error of the
*       optimization. Values are:
*           0 : optimization completed successfully
*           1 : the maximum number of iterations was exceeded
*  - best[xlen + 2]: the number of function evaluations in the optimization
*       (value should be a whole number > 0 and <= maxit + points)
*  - best[xlen + 3]: the number of iterations (value should be a
*       whole number > 0 and <= maxit)
*  - best[xlen + 4]: the maximum constraint violation that occurred during
*       the optimization. If the function pointer is NULL then it is
*       set to 0.0
*   - best[xlen + 5]: the final error of the optimization
*/
    size_t iters;

    if(seedval) srand(seedval);
    else srand(time(0));

    leapfrog_data* self = init_leapfrog(fptr, lower, upper, xlen, points,
                                       gptr, discrete, discretelen, tol);
    for(iters = 0; iters < maxit; iters++) {
        iterate(self);
        if(self->error < tol){
            break;
        }
    }
    if(iters >= maxit) log_warn("Maximum iterations exceeded.");
    cpy_data(self->pointset[self->besti], best, xlen);
    best[xlen] = self->objs[self->besti];
    best[xlen + 1] = iters >= maxit ? 1.0 : 0.0;
    best[xlen + 2] = self->nfev;
    best[xlen + 3] = iters;
    best[xlen + 4] = self->maxcv;
    best[xlen + 5] = self->error;

    free_data(self);
}
