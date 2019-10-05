#include <iostream>
#ifdef _WIN32
    #include <windows.h>
#else
    #include <dlfcn.h>
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
    typedef void ext_func(double (*)(double*), double*, double*,
                size_t, size_t, double (*)(double*), size_t*,
                size_t, size_t, double, size_t, double*);

#ifdef _WIN32
    HINSTANCE handle;  
    handle = LoadLibrary(TEXT("./leapfrog.dll")); 
#else
    void *handle;
    handle = dlopen("./leapfrog.so", RTLD_NOW);
#endif  
 
    if(!handle){
        cout << "ERROR! (1)\n";
        return -1;
    }

#ifdef _WIN32
    ext_func* minimize = (ext_func*) GetProcAddress(handle, "minimize");
#else
    ext_func* minimize = (ext_func*) dlsym(handle, "minimize");
#endif

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


    for(i = 0; i < xlen+6; i++){
        printf("%f ", best[i]);
    }
    printf("\n");

    delete[] best;
    delete[] discrete;
    delete[] lower;
    delete[] upper;
    

#ifdef _WIN32
    FreeLibrary(handle); 
#else
    dlclose(handle);
#endif
    
    return 0;
}