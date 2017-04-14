/* LPFGOPT.h

   Declares the functions to be imported by our application, and exported by our
   DLL, in a flexible and elegant way.
*/

#ifdef _WIN32

  /* You should define LPFGOPT_EXPORTS *only* when building the DLL. */
  #ifdef LPFGOPT_EXPORTS
    #define LPFGOPTAPI __declspec(dllexport)
  #else
    #define LPFGOPTAPI __declspec(dllimport)
  #endif

  /* Define calling convention in one place, for convenience. */
  #define LPFGOPTCALL __cdecl

#else /* _WIN32 not defined. */

  /* Define with no value on non-Windows OSes. */
  #define LPFGOPTAPI
  #define LPFGOPTCALL

#endif

/* Make sure functions are exported with C linkage under C++ compilers. */

#ifdef __cplusplus
extern "C"
{
#endif

#ifdef PY_EXPORTS
// ADDITIONS FROM :
// http://stackoverflow.com/questions/15160077/assigning-python-function-to-ctypes-pointer-variable
// Setting up external function pointers from a python script.

typedef double (*FUNC)(double*);
LPFGOPTAPI FUNC pfunc;
LPFGOPTAPI void set(FUNC f)
{
    pfunc = f;
}

double func_ext(double* x)
{
    return pfunc(x);
}

LPFGOPTAPI double func_1(double* x)
{
    return func_ext(x);
}
// END ADDITIONS
#endif

/* Struct def*/
LPFGOPTAPI typedef struct two_dimensional_array{
/* Structure for 2d arrays to be used in the optimization */
    int rows;
    int columns;
    double** array;
}array_2d;

/* Declare our Add function using the above definitions. */
LPFGOPTAPI double* LPFGOPTCALL minimize(double (*f1_ptr)(double*), array_2d* int_1,
              int npts, int nvars);
LPFGOPTAPI void LPFGOPTCALL free_array_2d(array_2d* array);
LPFGOPTAPI array_2d* LPFGOPTCALL zeros(int rows, int columns);



#ifdef __cplusplus
} // __cplusplus defined.
#endif