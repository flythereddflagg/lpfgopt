#include <stdio.h>
#include <stdlib.h>
#include "leapfrog.h"
#include "dbg.h"

double f(double* x)
{
    return x[0]*x[0] + x[1]*x[1] + 100;
}

double g(double* x)
{
    return -x[0] *x[0] + 10 - x[1];
}

int main(int argc, char** argv)
{
    size_t i;
    size_t xlen = 2;
    double* lower = (double*)malloc(sizeof(double)*xlen);
    double* upper = (double*)malloc(sizeof(double)*xlen);
    double (*fptr)(double* x) = &f;
    double (*gptr)(double* x) = &g;
    size_t discretelen = 2;
    size_t* discrete = (size_t*)malloc(sizeof(size_t)*discretelen);
    double* best = (double*)malloc(sizeof(double)*(xlen + N_RESULTS));

    discrete[0] = 0;
    discrete[1] = 1;

    for(i = 0; i < xlen; i++){
        lower[i] = -10.0;
        upper[i] =  10.0;
    }
    
    minimize(fptr, lower, upper, xlen, 20, gptr, discrete, discretelen,
             1e5, 1e-3, 1569434771, NULL, 0, NULL, best);

    for(i = 0; i < xlen + N_RESULTS; i++){
        printf("%f ", best[i]);
    }
    printf("\n");

    free(best);
    free(discrete);
    free(lower);
    free(upper);

    return 0;
}