#include "dbg.h"
#include "lpfgopt.h"
#include <stdio.h>
#include <stdlib.h>

double f(double* x)
{
    return x[0]*x[0] + x[1]*x[1] + 100;
}

// double g(double* x)
// {
//     return -x[0] *x[0] + 10 - x[1];
// }

int main(int argc, char** argv)
{
    size_t i;
    size_t xlen = 2;
    double* lower = malloc(sizeof(double)*xlen);
    double* upper = malloc(sizeof(double)*xlen);
    double (*fptr)(double* x) = &f;
    // double (*gptr)(double* x) = &g;
    // size_t discretelen = 2;
    // size_t* discrete = malloc(sizeof(size_t)*discretelen);

    // discrete[0] = 0;
    // discrete[1] = 1;

    for(i = 0; i < xlen; i++){
        lower[i] = -5.0;
        upper[i] =  5.0;
    }

    double* out = minimize(
                        fptr, lower, upper, xlen, 20,
                        NULL, NULL, 0, 1e2,
                        1e-1, 1569433771);

    free(lower);
    free(upper);
    for(i = 0; i < xlen+1; i++){
        printf("%f ", out[i]);
    }
    printf("\n");
    double outs[2] = {out[1], out[2]};
    double* outp = &outs;
    printf("%f\n", f(outp));

    check(out, "out does not exist!");
    free(out);

    return 0;

error:

    return -1;
}