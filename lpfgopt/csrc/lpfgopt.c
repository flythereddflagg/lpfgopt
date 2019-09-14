
typedef struct {
    size_t rows;
    size_t columns;
    double** array;
} array_2d;


typedef struct {

    double* (*f)(double*, double*);
    double* (*g)(double*);
    size_t xlen;

    array_2d* bounds;
    array_2d* pointset;
    
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


void free_array_2d(array_2d* array)
{
/* EXT Function for freeing mallocs for two_dimensional_array */
    for (int i = 0; i < array->rows; i++){
        if (array->array[i]) free(array->array[i]);
    }
    if(array->array) free(array->array);
    if(array) free(array);
}s


void free_data(leapfrog_data* data)
{
    ;
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
}

void iterate(leapfrog_data* self)
{
    leapfrog(self);
    get_best_worst(self);
    calculate_convergence(self);
    self->total_iters += 1;

}


void leapfrog(leapfrog_data* self)
{
    ;
}


void get_best_worst(leapfrog_data* self)
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
                            size_t maxit, double tol, int seedval)
{
    leapfrog_data* data = malloc(sizeof(leapfrog_data));
    data->f = fptr;
    data->g = gptr;
    data->xlen = xlen;
    data->discretelen = discretelen;
    data->points = points;
    data->maxit = maxit;
    data->tol = tol;
    data->seedval = seedval;
    data->nfev = nfev;
    data->maxcv = maxcv;
    data->total_iters = 0;
    data->besti = 0;
    data->worsti = 0;
    data->error = 100.0;

// array_2d* bounds;
// array_2d* pointset;

// size_t* discrete;
    
}


double* minimize(double (*fptr)(double*), double* lower, double* upper, 
                size_t xlen, size_t points, double (*gptr)(double*), 
                size_t discrete, size_t maxit, double tol, int seedval)
{
    size_t iters;
    leapfrog_data* data = init_leapfrog(fptr, lower, upper, xlen, points, 
                                       gptr, discrete, maxit, tol, seedval);
    for(iters = 0; iters < data->maxit; iters++) {
        iterate(data);
        if(data->error < data->tol){
            free_data(data);
            return data->pointset->array[data->besti];
        }
    }
    free_data(data);
    return data->pointset->array[data->besti];
}
