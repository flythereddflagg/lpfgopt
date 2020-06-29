#include <iostream>
#ifdef _WIN32
    #include <windows.h>
    #define RTLD_NOW
    #define dlopen(path, mode) LoadLibrary(TEXT(path))
    #define DLL_PATH "./lpfgopt/leapfrog_c.dll"
    #define dlsym GetProcAddress
    #define dlclose FreeLibrary
    #define dlerror GetLastError
    #define ERR int
#else
    #include <dlfcn.h>
    #define HINSTANCE void*
    #define ERR char*
    #define DLL_PATH "./lpfgopt/leapfrog_c.so"
#endif


using namespace std;

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
        printf("%.5f ", x[i]);
    }
    printf("\n");
}

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

int main(void)
{
    typedef void ext_func(
                double (*)(double*, size_t), double*, double*, size_t,
                size_t, double (*)(double*, size_t), size_t*, size_t,
                size_t, double, size_t, double**, int,
                void (*)(double*, size_t), double*);
    typedef size_t nr;

    HINSTANCE handle = dlopen(DLL_PATH, RTLD_NOW);

    if(!handle){
        cout << "ERROR! (1)\n" << (ERR) dlerror() << "\n";
        return -1;
    }

    ext_func* minimize = (ext_func*) dlsym(handle, "minimize");
    const size_t N_RESULTS = (size_t) *((nr*) dlsym(handle, "N_RESULTS"));

    size_t i = 0, j = 0, xlen = 2, points = 20, maxit = 1e5, 
        seedval = 1569434771;
    double tol = 1e-3;
    double* lower = new double[xlen];
    double* upper = new double[xlen];
    double (*fptr)(double* x, size_t xlen) = &f;
    double (*gptr)(double* x, size_t xlen) = &g;
    void (*cbptr)(double* x, size_t xlen) = &callback;
    size_t discretelen = 2;
    size_t* discrete = new size_t[discretelen];
    double* best = new double[xlen + N_RESULTS];

    double** start_ptr = new double*[points];
    for (size_t row = 0; row < points; row ++){
        start_ptr[row] = new double[xlen];
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

    printf("SOLUTION: \n");
    for(i = 0; i < xlen + N_RESULTS; i++){
        printf("%f ", best[i]);
    }
    printf("\n");
    for(i = 0; i < points; i++){
        for(j = 0; j < xlen; j++){
            printf("%f ", start_ptr[i][j]);
        }
        printf("\n");
    }

    delete[] best;
    delete[] discrete;
    delete[] lower;
    delete[] upper;
    for (size_t row = 0; row < points; row ++){
        delete[] start_ptr[row];
    }
    delete[] start_ptr;

    dlclose(handle);

    return 0;
}