#include "dbg.h"
#include "lpfgopt.h"
#include <stdlib.h>
#include <time.h>


typedef struct {
    size_t rows;
    size_t columns;
    double** array;
} array_2d;


typedef struct {

    double (*f)(double*);
    double (*g)(double*);
    size_t xlen;

    double* lower;
    double* upper;
    array_2d* pointset;

    double* args;
    
    size_t* discrete;
    size_t discretelen;

    size_t points;
    size_t maxit;

    double tol;
    int seedval;

    size_t nfev;
    double maxcv;
    size_t total_iters;
    
    size_t besti;
    size_t worsti;
    double error;
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


array_2d* zeros(size_t rows, size_t columns)
{
    check(rows > 0 && columns > 0, 
        "'rows' and 'columns' must be greater than 0.");
    size_t i;
    size_t j;
    array_2d* matrix    = (array_2d*) malloc(sizeof(array_2d));
    double**  the_array = (double**)  malloc(rows*sizeof(double*));

    for (i = 0; i < rows; i++){
        the_array[i] = (double*) malloc(columns*sizeof(double));
        for (j = 0; j < columns; j++){
            the_array[i][j] = 0.0;
        }
    }

    matrix->array   = the_array;
    matrix->rows    = rows;
    matrix->columns = columns;
    
    return matrix;

error:
    return NULL;
}


void free_array_2d(array_2d* array)
{
/** 
* Frees all mallocs associated with @funtion zeros thereby freeing
* @param array.
*/
    for (int i = 0; i < array->rows; i++){
        if (array->array[i]) free(array->array[i]);
    }
    if(array->array) free(array->array);
    if(array) free(array);
}


void free_data(leapfrog_data* data)
{
/**
* Frees all mallocs associated with @function init_leapfrog
* will free an allocated leapfrog_data struct.
*/
    if(data->args) free(data->args);
    if(data->pointset) free_array_2d(data->pointset);
    if(data) free(data);
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
    for(size_t i = 0; i < self->pointset->rows; i++){
        if(self->pointset->array[i][0] <\
                self->pointset->array[self->best][0]){
            self->best = i;
        }
        if(self->pointset->array[i][0] >\
                self->pointset->array[self->worst][0]){
            self->worst = i;
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
                            size_t discretelen, size_t maxit, double tol, 
                            size_t seedval)
{
/**
* Allocates memory for and initalizes the main leapfrog_data struct
* to be used in the optimization.
*/
    leapfrog_data* data = (leapfrog_data*) malloc(sizeof(leapfrog_data));
    data->f = fptr;
    data->g = gptr;
    data->xlen = xlen;
    data->discretelen = discretelen;
    data->points = points;
    data->maxit = maxit;
    data->tol = tol;
    data->seedval = seedval;
    data->nfev = 0;
    data->maxcv = 0;
    data->total_iters = 0;
    data->besti = 0;
    data->worsti = 0;
    data->error = 100.0;
    data->lower = lower;
    data->upper = upper;
    data->discrete = discrete;
    data->pointset = zeros(points, data->xlen + 1);
    data->args = (double*) malloc(sizeof(double)*data->xlen);

    if(seedval) srand(seedval);
    else srand(time(0));

    for(size_t i = 0; i < data->pointset->rows; i++){
        for(size_t j = 1; j < data->pointset->columns; j++){
            data->pointset->array[i][j] = uniform(data->lower[j-1],
                                                  data->upper[j-1]);
            data->args[j-1] = data->pointset->array[i][j];
        }
        data->pointset->array[i][0] = data->f(data->args);
        data->nfev++;
    }
    enforce_constraints(data);
    eval_best_worst(data);
    return data;
}


void iterate(leapfrog_data* self)
{
/**
* Completes one iteration of the leapfrog optimization algorithm.
*/
    leapfrog(self);
    eval_best_worst(self);
    calculate_convergence(self);
    self->total_iters++;
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
    leapfrog_data* data = init_leapfrog(fptr, lower, upper, xlen, points, 
                                       gptr, discrete, discretelen, maxit, 
                                       tol, seedval);
    for(iters = 0; iters < data->maxit; iters++) {
        iterate(data);
        if(data->error < data->tol){
            cpy_data(data->pointset->array[data->besti], best, xlen+1);
            free_data(data);
            return best;
        }
    }
    log_warn("Maximum iterations exceeded.");
    cpy_data(data->pointset->array[data->besti], best, xlen+1);
    free_data(data);
    return best;
}
