#ifndef __LPFGOPT_H__
#define __LPFGOPT_H__

#ifdef _WIN32

  /* You should define LPFGOPT_EXPORTS *only* when building the DLL. */
  #ifdef LPFGOPT_EXPORTS
    #define WINAPI __declspec(dllexport)
  #else
    #define WINAPI __declspec(dllimport)
  #endif

  /* Define calling convention in one place, for convenience. */
  #define WINCALL __cdecl

#else /* _WIN32 not defined. (LINUX OR MAC) */

  /* Define with no value on non-Windows OSes. */
  #define WINAPI
  #define WINCALL

#endif

// #define WINAPI
// #define WINCALL

#ifdef __cplusplus
extern "C"
{
#endif

/* Declare our functions using the above definitions. */

WINAPI void WINCALL minimize(
                double (*fptr)(double*), double* lower, double* upper,
                size_t xlen, size_t points, double (*gptr)(double*),
                size_t* discrete, size_t discretelen, size_t maxit,
                double tol, size_t seedval, double* best);

#ifdef __cplusplus
}
#endif
#endif