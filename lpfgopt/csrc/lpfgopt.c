#include "dbg.h"
#include "lpfgopt.h"
#include <stdlib.h>
#include <time.h>


typedef struct {

    double (*f)(double*);   // the objective function
    double (*g)(double*);   // the constraint function
    size_t xlen;            // the number of args in f and g
    size_t points;          // the number of points for optimization

    double* lower;          // the lower bounds; length = xlen
    double* upper;          // the upper bounds; length = xlen
    double** pointset;      // the objective function values and 
                            // corresponding points with the objective
                            // function value as the first value in each
                            // row; shape = (points, xlen + 1)
    
    double* args;           // the array holding the current arguments to be
                            // passed into the function; length = xlen
    
    size_t* discrete;       // array of discrete indices
    size_t discretelen;     // length of discrete

    size_t nfev;            // number of function evaluations
    double maxcv;           // maxiumum constraint violation
    
    size_t besti;           // the index of the best point
    size_t worsti;          // the index of the worst point
    double error;           // the value of the convergence error

} leapfrog_data;


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
* Frees all mallocs associated with @funtion zeros thereby freeing
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
    if(self->args) free(self->args);
    if(self->pointset) free_array_2d(self->pointset, self->points);
    if(self) free(self);
}


double uniform(double lower, double upper)
{
/**
* @returns a random double between
* @param lower and @param upper following a
* uniform distribution.
*/
    double frac = 1.0 * rand() / RAND_MAX;
    return (upper - lower) * frac + lower;
}


void enforce_constraints(leapfrog_data* self)
{
    ;
}


void eval_best_worst(leapfrog_data* self)
{
/**
* Evaluates and adjusts @param self's best and worst
* attributes to the best and worst indices in the pointset.
*/
    for(size_t i = 0; i < self->points; i++){
        if(self->pointset[i][0] < self->pointset[self->besti][0]){
            self->besti = i;
        }
        if(self->pointset[i][0] > self->pointset[self->worsti][0]){
            self->worsti = i;
        }
    }
}


void enforce_discrete(leapfrog_data* self)
{
    ;
}


void leapfrog(leapfrog_data* self)
{
    ;
}


void calculate_convergence(leapfrog_data* self)
{
    ;
}


leapfrog_data* init_leapfrog(double (*fptr)(double*), double* lower, 
                            double* upper, size_t xlen, size_t points, 
                            double (*gptr)(double*), size_t* discrete,
                            size_t discretelen)
{
/**
* Allocates memory for and initalizes the main leapfrog_data struct
* to be used in the optimization.
*/
    leapfrog_data* self = (leapfrog_data*) malloc(sizeof(leapfrog_data));
    self->f = fptr;
    self->g = gptr;
    self->xlen = xlen;
    self->points = points;
    self->nfev = 0;
    self->maxcv = 0;
    self->besti = 0;
    self->worsti = 0;
    self->error = 100.0;
    self->lower = lower;
    self->upper = upper;
    self->discrete = discrete;
    self->discretelen = discretelen;
    self->pointset = zeros(points, self->xlen + 1);
    self->args = (double*) malloc(sizeof(double)*self->xlen);

    for(size_t i = 0; i < self->points; i++){
        for(size_t j = 1; j < self->xlen + 1; j++){
            self->pointset[i][j] = uniform(self->lower[j-1],
                                                  self->upper[j-1]);
            self->args[j-1] = self->pointset[i][j];
        }
        self->pointset[i][0] = self->f(self->args);
        self->nfev++;
    }
    enforce_constraints(self);
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


LPFGOPTAPI double* LPFGOPTCALL minimize(
                double (*fptr)(double*), double* lower, double* upper, 
                size_t xlen, size_t points, double (*gptr)(double*), 
                size_t* discrete, size_t discretelen, size_t maxit, 
                double tol, int seedval)
{
/*
* Minimizes a function until the convergence criteria are 
* satisfied or the number of iterations exceeds 
* 'maxit'.
*/
    size_t iters;
    double* best = (double*) malloc(sizeof(double)*(xlen+1));

    if(seedval) srand(seedval);
    else srand(time(0));

    leapfrog_data* self = init_leapfrog(fptr, lower, upper, xlen, points, 
                                       gptr, discrete, discretelen); 
    for(iters = 0; iters < maxit; iters++) {
        iterate(self);
        if(self->error < tol){
            break;
        }
    }
    if(iters >= maxit) log_warn("Maximum iterations exceeded.");
    cpy_data(self->pointset[self->besti], best, xlen+1);
    free_data(self);
    return best;
}
