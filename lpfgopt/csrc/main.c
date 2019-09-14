#include "dbg.h"
#include "lpfgopt.h"
#include <stdio.h>
#include <stdlib.h>

double f(double* x)
{
    return x[0]*x[0] + x[1]*x[1];
}

double g(double* x)
{
    return -x[0] *x[0] + 10 - x[1];
}

int main(int argc, char** argv)
{
    size_t i;
    size_t xlen = 2;
    double* lower = malloc(sizeof(double)*xlen);
    double* upper = malloc(sizeof(double)*xlen);
    double (*fptr)(double* x) = &f;
    double (*gptr)(double* x) = &g;
    
    for(i = 0; i < xlen; i++){
        lower[i] = -20.0;
        upper[i] =  20.0;
    }

    double* out = minimize(
                        fptr, lower, upper, xlen, 20, 
                        gptr, NULL, 0, 100, 1e-3, 1234);
    
    free(lower);
    free(upper);
    for(i = 0; i < xlen+1; i++){
        printf("%f", out[i]);
    }
    printf("\n");

    check(out, "out does not exist!");
    free(out);

    return 0;

error:

    return -1;
}