#include "dbg.h"
#include "lpfgopt.h"

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
    size_t xlen = 2
    double lower[xlen] = {-20.0, -20.0};
    double upper[xlen] = { 20.0,  20.0};
    double* plower = &lower;
    double* pupper = &upper;
    double (*fptr)(double* x) = &f;
    double (*gptr)(double* x) = &g;
    

    double* out = minimize(
                        fptr, plower, pupper, xlen, 20, 
                        gptr, NULL, 0, 100, 1e-3, 1234);

    return 0;

error:

    return -1;
}