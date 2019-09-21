#ifndef __LPFGOPT_H__
#define __LPFGOPT_H__
/* LPFGOPT.h
   Declares the functions to be imported by our application, and exported by our
   DLL, in a flexible and elegant way.
*/
//#ifndef LPFGOPT_H
//#define LPFGOPT_H

// #ifdef _WIN32

//   /* You should define LPFGOPT_EXPORTS *only* when building the DLL. */
//   #ifdef LPFGOPT_EXPORTS
//     #define LPFGOPTAPI __declspec(dllexport)
//   #else
//     #define LPFGOPTAPI __declspec(dllimport)
//   #endif

//   /* Define calling convention in one place, for convenience. */
//   #define LPFGOPTCALL __cdecl

// #else /* _WIN32 not defined. (LINUX OR MAC) */

//   /* Define with no value on non-Windows OSes. */
//   #define LPFGOPTAPI
//   #define LPFGOPTCALL

// #endif

#define LPFGOPTAPI
#define LPFGOPTCALL

/* Make sure functions are exported with C linkage under C++ compilers. */

#ifdef __cplusplus
extern "C"
{
#endif

// #ifdef PY_EXPORTS
// // Py Exports from the following URL:
// // http://stackoverflow.com/questions/15160077/assigning-python-function-to-ctypes-pointer-variable
// // Setting up external function pointers from a python script.
// #include "dbg.h"

// typedef double (*FUNC)(double*);
// LPFGOPTAPI FUNC pfunc;
// LPFGOPTAPI void set(FUNC f)
// {
//     pfunc = f;
// }

// double func_ext(double* x)
// {
//     return pfunc(x);
// }

// LPFGOPTAPI double func_1(double* x)
// {
//     return func_ext(x);
// }
// #endif

/* Declare our functions using the above definitions. */

LPFGOPTAPI double* LPFGOPTCALL minimize(
                double (*fptr)(double*), double* lower, double* upper, 
                size_t xlen, size_t points, double (*gptr)(double*), 
                size_t* discrete, size_t discretelen, size_t maxit, 
                double tol, size_t seedval);

#ifdef __cplusplus
} // __cplusplus defined.
#endif

#endif