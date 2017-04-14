/* add.h

   Declares the functions to be imported by our application, and exported by our
   DLL, in a flexible and elegant way.
*/

#ifdef _WIN32

  /* You should define ADD_EXPORTS *only* when building the DLL. */
  #ifdef ADD_EXPORTS
    #define ADDAPI __declspec(dllexport)
  #else
    #define ADDAPI __declspec(dllimport)
  #endif

  /* Define calling convention in one place, for convenience. */
  #define ADDCALL __cdecl

#else /* _WIN32 not defined. */

  /* Define with no value on non-Windows OSes. */
  #define ADDAPI
  #define ADDCALL

#endif

/* Make sure functions are exported with C linkage under C++ compilers. */

#ifdef __cplusplus
extern "C"
{
#endif

/* Declare our Add function using the above definitions. */
ADDAPI int ADDCALL Add(int a, int b);

#ifdef __cplusplus
} // __cplusplus defined.
#endif