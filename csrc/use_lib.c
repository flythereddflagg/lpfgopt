/**
* File: use_lib.c
* Author: Mark Redd
* Email: redddogjr@gmail.com
* Website: http://www.r3eda.com/
* About:
* This is an example usage with C using a statically linked library. To be 
* compiled with gcc. Intended to be compatible with Windows and Linux.
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

#include <stdio.h>
#include <stdlib.h>
#include "leapfrog.h"
#include "dbg.h"

typedef enum {false, true} bool;

double start_pts[20][2] = {
    {-3.26,   -7.9},
    {-0.30,   2.33},
    {-7.37,   6.11},
    {-0.19,   7.01},
    {-7.21,   -8.8},
    {-6.87,   4.09},
    {-4.58,   9.06},
    {-9.75,   -8.9},
    {4.901,   -3.1},
    {-7.53,   1.69},
    {5.437,   0.57},
    {-7.73,   9.82},
    {0.549,   5.66},
    {9.238,   -7.5},
    {-1.29,   -4.2},
    {7.726,   1.42},
    {-4.32,   6.00},
    {-7.11,   9.40},
    {1.937,   7.50},
    {7.092,  -9.88}
};

double f(double* x, size_t xlen)
{
    return x[0]*x[0] + x[1]*x[1] + 100;
}

double g(double* x, size_t xlen)
{
    return -x[0] *x[0] + 10 - x[1];
}

void callback(double* x, size_t xlen)
{
    size_t i;
    for (i = 0; i < xlen; i++){
        printf("%.2f ", x[i]);
    }
    printf("\n");
}

int main(int argc, char** argv)
{
    size_t i = 0, xlen = 2, points = 20, maxit = 1e5, seedval = 1569434771;
    double tol = 1e-3;
    double* lower = (double*)malloc(sizeof(double)*xlen);
    double* upper = (double*)malloc(sizeof(double)*xlen);
    double (*fptr)(double* x, size_t xlen) = &f;
    double (*gptr)(double* x, size_t xlen) = &g;
    void (*cbptr)(double* x, size_t xlen) = &callback;
    size_t discretelen = 2;
    size_t* discrete = (size_t*)malloc(sizeof(size_t)*discretelen);
    double* best = (double*)malloc(sizeof(double)*(xlen + N_RESULTS));

    double** start_ptr = (double**)malloc(sizeof(double*)*points);

    for (size_t row = 0; row < points; row ++){
        start_ptr[row] = (double*)malloc(sizeof(double)*xlen);
        for (size_t col = 0; col < xlen; col ++){
            start_ptr[row][col] = start_pts[row][col];
        }
    }

    discrete[0] = 0;
    discrete[1] = 1;

    for(i = 0; i < xlen; i++){
        lower[i] = -10.0;
        upper[i] =  10.0;
    }
    
    minimize(fptr, lower, upper, xlen, points, gptr, discrete, discretelen,
             maxit, tol, seedval, start_ptr, false, cbptr, best);

    for(i = 0; i < xlen + N_RESULTS; i++){
        printf("%f ", best[i]);
    }
    printf("\n");

    free(best);
    free(discrete);
    free(lower);
    free(upper);
    for (size_t row = 0; row < points; row++) {
        if(start_ptr[row]) free(start_ptr[row]);
    }
    free(start_ptr);

    return 0;
}