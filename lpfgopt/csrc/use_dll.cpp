#include <iostream>

#include <dlfcn.h>

using namespace std;

double f(double* x)
{
    return x[0]*x[0] + x[1]*x[1] + 100;
}

double g(double* x)
{
    return -x[0] *x[0] + 10 - x[1];
}

int main(void)
{
    void *handle;
    handle = dlopen("./leapfrog.dll", RTLD_NOW);
    if(!handle){
        cout << "ERROR! (1)\n";
    }
    typedef void ext_func(double (*)(double*), double*, double*,
                size_t, size_t, double (*)(double*), size_t*,
                size_t, size_t, double, size_t, double*);
    ext_func* minimize = (ext_func*) dlsym(handle, "minimize");

    size_t i;
    size_t xlen = 2;
    double* lower = new double[xlen];
    double* upper = new double[xlen];
    double (*fptr)(double* x) = &f;
    double (*gptr)(double* x) = &g;
    size_t discretelen = 2;
    size_t* discrete = new size_t[discretelen];
    double* best = new double[xlen + 6];

    discrete[0] = 0;
    discrete[1] = 1;

    for(i = 0; i < xlen; i++){
        lower[i] = -10.0;
        upper[i] =  10.0;
    }

    minimize(fptr, lower, upper, xlen, 20, gptr, discrete, discretelen,
             1e5, 1e-3, 1569433771, best);


    for(i = 0; i < xlen; i++){
        printf("%f ", best[i]);
    }
    printf("\n");

    delete[] lower;
    delete[] upper;
    delete[] best;
    dlclose(handle);
    return 0;
}