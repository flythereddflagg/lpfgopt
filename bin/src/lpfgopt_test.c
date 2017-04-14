#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "lpfgopt.h"

/* lpfg_test.c

   Demonstrates using the function imported from the DLL, in a flexible and
   elegant way.
*/

double f1(double* x)
{
/* Test function to be optimized */
    double x2 = x[1];
    double y  = x[0] * x[0] * 2.0 + pow(x2,2.0) + 3.0;
    return y;
}

int main(int argc, char** argv)
{
    array_2d* int_1;
    int i;
    int nx = 20;
    int nvars = 2;
    double (*f1_ptr)(double*);
    double* best;
    f1_ptr = &f1;

    int_1 = zeros(nvars,2);
    int_1->array[0][0] = -10.0;
    int_1->array[0][1] =  10.0;
    int_1->array[1][0] = -10.0;
    int_1->array[1][1] =  10.0;
    
    
    best = minimize(f1_ptr, int_1, nx, nvars);
    printf("Best: {");
    for (i = 0; i<nvars+1; i++){
        printf(" %.9f", best[i]);
        }
    printf(" }\n");
    free(best);
    free_array_2d(int_1);
    
    //clock_t end = clock();
    //double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    //printf("Optimization performed in %.9f seconds.\n", time_spent);
    // Optimization performed in 0.003000000 seconds. (Windows)
    // This is 7.3 times faster than python did the optimization (Linux: 0.022 sec)
    // on linux it was clocked at .002 seconds which makes it 11 times faster
    // than python
    
    return 0;
}
