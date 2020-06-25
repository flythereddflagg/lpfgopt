#ifndef __LEAPFROG_H__
#define __LEAPFROG_H__

#ifdef __cplusplus
extern "C"
{
#endif
void minimize(
    double (*fptr)(double*), double* lower, double* upper,
    size_t xlen, size_t points, double (*gptr)(double*),
    size_t* discrete, size_t discretelen, size_t maxit,
    double tol, size_t seedval, double** pointset,
    int init_pointset, void (*callback)(double*), 
    double* best);

const size_t N_RESULTS;

#ifdef __cplusplus
}
#endif
#endif