#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "lpfgopt.h"


//typedef struct two_dimensional_array{
/* Structure for 2d arrays to be used in the optimization */
//    int rows;
//    int columns;
//   double** array;
//}array_2d;


void LPFGOPTCALL free_array_2d(array_2d* array)
{
/* Function for freeing mallocs for two_dimensional_array */
    for (int i = 0; i < array->rows; i++){
        free(array->array[i]);
        }
    free(array->array);
    free(array);
    /*Good rule to remember: For every 
      malloc calloc or realloc you must have one free*/
}

double uniform(double lower, double upper)
{
/* Generate a random number bewtween lower and upper */
    int rint;
    double zero_one, rinp;
    rint = rand();
    zero_one = 1.0 * rint / RAND_MAX;
    rinp = (upper - lower) * zero_one + lower;
    
    return rinp;
}


array_2d* LPFGOPTCALL zeros(int rows, int columns)
{
/* Generate a 2d array with rows rows and columns columns */
    int i;
    int j;
    array_2d* array1 = (array_2d*) malloc(sizeof(array_2d));
    double** the_array = (double**) malloc(rows*sizeof(double*));

    for (i = 0; i < rows; i++){
        the_array[i] = (double*) malloc(columns*sizeof(double));
        for (j = 0; j < columns; j++){
            the_array[i][j] = 0.0;
            }
        }

    array1->array   = the_array;
    array1->rows    = rows;
    array1->columns = columns;
    
    return array1;
}


void gen_pt_set(array_2d* matrix, array_2d* intervals,
                double (*func)(double*), double* args)
{
/* Poplulate a matrix with column 0 being the values of the 
   objective function and the other columns being the arguments
   of that function*/
    int row;
    int col;
    double rinp;   
    for (row = 0; row < matrix->rows; row++){
        for (col = 1; col < matrix->columns; col++){
            rinp = uniform(intervals->array[col-1][0],
                intervals->array[col-1][1]);
            matrix->array[row][col] = rinp;
            args[col-1] = rinp;
            }
        //rinp = func(args); //##ISSUE!!!
        matrix->array[row][0] = func(args); 
        }

}

void eval_bw(array_2d* matrix, int* bw_index)
{
/* Get the indices of the best and worst objective values 
   of the objective function */
    int b = 0;
    int w = 0;
    int i;

    for (i = 0; i < matrix->rows; i++){
        if (matrix->array[i][0] < matrix->array[b][0]) b = i;
        if (matrix->array[i][0] > matrix->array[w][0]) w = i;
        }
    bw_index[0] = b;
    bw_index[1] = w;
}


void leap_frog(double (*func)(double*), array_2d* matrix,
               int bi, int wi, array_2d* int_1, double* args)
{
/* Run one iteration of the Leapfrog algorithm given the matrix
   the objective function, intervals and the indices of the best
   and worst objective function values */
    int i;
    double itvl1;
    double itvl2;
    double lower;
    for (i = 0; i < (matrix->columns - 1); i++){
        // For each argument, choose a new interval over which
        // to leap frog based on the opposite of the difference
        // between the best and worst points
        itvl1 = matrix->array[bi][i+1];
        itvl2 = 2.0 * matrix->array[bi][i+1] - matrix->array[wi][i+1];
        if (itvl1 > itvl2){
            // Sort the two points so the lower is itvl1
            lower = itvl2;
            itvl2 = itvl1;
            itvl1 = lower;
            }
        // Check and correct for intervals going out of bounds
        if (itvl1 < int_1->array[i][0]) itvl1 = int_1->array[i][0];
        if (itvl2 > int_1->array[i][1]) itvl2 = int_1->array[i][1];
        args[i] = uniform(itvl1, itvl2); // Get a random input
        matrix->array[wi][i+1] = args[i];// Update matrix and args
        }
    matrix->array[wi][0] = func(args); // Update objective ISSUE!!!
}


double err_calc(array_2d* matrix, int bi, int wi)
{
    int i;
    int j;
    double err;

    err = fabs(matrix->array[bi][0] - matrix->array[wi][0]);

    for (i = 0; i < matrix->rows; i++){
        for (j = 1; j < matrix->columns; j++){
            err += fabs(matrix->array[bi][j] - matrix->array[i][j]);
            }
        }
        
    return err;
    /* relative error returned overflow errors */
}


double* LPFGOPTCALL minimize(double (*f1_ptr)(double*), array_2d* int_1,
              int npts, int nvars)
{
/* Minimize function that runs the leap_frog algorithm to
   minimize f1_ptr on the intervals on int_1 */
    int bi;
    int wi;
    int iter;
    int dvi;
    double err;
    // initalize maximum iterations and the tolerance;
    int maxit = 10000;
    double tol = 1E-5;
    // Heap allocate our pt_set our best and worst indexes and 
    // our arg array;
    array_2d* pt_set;
    int* bw_index = (int*)malloc(2*sizeof(int));
    double* args = (double*) malloc(nvars * sizeof(double));
    
    
    srand(time(NULL)); // Seed random number generator;
    // Generate an empty matrix and populate it with
    // objective values and random points on the intervals;
    pt_set = zeros(npts,nvars+1);
    gen_pt_set(pt_set, int_1, f1_ptr, args);
    
    // Iterate to minimize
    for (iter = 0; iter < maxit; iter++){
        eval_bw(pt_set, bw_index); // Get best and worst points;
        bi = bw_index[0];
        wi = bw_index[1];
        // Leapfrog the worst over the best
        leap_frog(f1_ptr, pt_set, bi, wi, int_1, args);
        err = err_calc(pt_set, bi, wi); // Calculate error
        
        if (err <= tol) break; // Check for convergence
        }

    if (iter == maxit){ 
        printf("Warning: maximum iterations exceeeded.\n");
        } // If maxit is reached warn user 
    
    
    double* best = (double*) malloc(nvars * sizeof(double));
    
    for (dvi = 0; dvi < nvars + 1; dvi++){
        best[dvi] = pt_set->array[bi][dvi];
        }
    // Free heap allocations
    
    free(bw_index);
    free(args);
    free_array_2d(pt_set);
    //printf("RUN SUCCESSFUL!!\n");
    return best;
   
}


/*
int main(int argc, char const* argv[])
{
    //clock_t begin = clock();
    
    array_2d* int_1;
    int nx = 20;
    int ny = 3;
    double (*f1_ptr)(double*);
    f1_ptr = &f1;

    int_1 = zeros(ny,2);
    int_1->array[0][0] = -10.0;
    int_1->array[0][1] =  10.0;
    int_1->array[1][0] = -10.0;
    int_1->array[1][1] =  10.0;
    
    
    minimize(f1_ptr, int_1, nx, ny);
    free_array_2d(int_1);
    
    //clock_t end = clock();
    //double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    //printf("Optimization performed in %.9f seconds.\n", time_spent);
    // Optimization performed in 0.003000000 seconds. (Windows)
    // This is 7.3 times faster than python did the optimization (Linux: 0.022 sec)
    // on linux it was clocked at .002 seconds which makes it 11 times faster
    // than python
    
    return 0;
}*/
