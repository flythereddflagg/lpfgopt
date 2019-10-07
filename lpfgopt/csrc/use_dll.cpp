#include <iostream>
#ifdef _WIN32
    #include <windows.h>
    #define RTLD_NOW
    #define dlopen(path, mode) LoadLibrary(TEXT(path))
    #define DLL_PATH "./leapfrog.dll"
    #define dlsym GetProcAddress
    #define dlclose FreeLibrary
    #define dlerror GetLastError
    #define ERR int
#else
    #include <dlfcn.h>
    #define HINSTANCE void*
    #define ERR char*
    #define DLL_PATH "./leapfrog.so"
#endif


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
    typedef void ext_func(
                double (*)(double*), double*, double*, size_t,
                size_t, double (*)(double*), size_t*, size_t,
                size_t, double, size_t, double**,
                void (*)(double*), double*);

    HINSTANCE handle = dlopen(DLL_PATH, RTLD_NOW);

    if(!handle){
        cout << "ERROR! (1)\n" << (ERR) dlerror() << "\n";
        return -1;
    }

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
             1e5, 1e-3, 1569434771, NULL, NULL, best);


    for(i = 0; i < xlen+6; i++){
        printf("%f ", best[i]);
    }
    printf("\n");

    delete[] best;
    delete[] discrete;
    delete[] lower;
    delete[] upper;

    dlclose(handle);

    return 0;
}