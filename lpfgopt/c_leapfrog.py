import ctypes
import os

def minimize(fun, 
            bounds,
            args=(),
            points=20,
            fconstraint=None,
            discrete=[],
            maxit=10000,
            tol=1e-5,
            seedval=None,
            pointset=None,
            callback=None,
            **kwargs):
    """
    Loads the compiled shared library named "leapfrog.dll" or
    "leapfrog.so" (depending on the operating system), runs
    the FORTRAN "leapfrog" subroutine and returns the results.
    """
    
    root = os.path.dirname(os.path.abspath(__file__))
    if os.name == 'nt':
        filename = root + "/leapfrog.dll"
    else:
        filename = root + "/leapfrog.so"

    print(filename)
    cdll = ctypes.cdll.LoadLibrary(filename)

    def f(x):
        return fun(x, *args)

    prototype = ctypes.CFUNCTYPE(
        ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    fptr = prototype(f)
    if fconstraint is not None:
        gptr = prototype(fconstraint)
    else:
        gptr = ctypes.POINTER(ctypes.c_double)()

    if seedval is not None:
        cseedval = ctypes.c_size_t(seedval)
    else:
        cseedval = ctypes.c_size_t(0)

    lower = [i[0] for i in bounds]
    upper = [i[1] for i in bounds]
    lowerp = (ctypes.c_double * len(lower))(*lower)
    upperp = (ctypes.c_double * len(upper))(*upper)
    xlen = ctypes.c_size_t(len(lower))
    cpoints = ctypes.c_size_t(points)
    cdiscrete = (ctypes.c_size_t * len(discrete))(*discrete)
    discretelen = ctypes.c_size_t(len(discrete))
    cmaxit = ctypes.c_size_t(maxit)
    ctol = ctypes.c_double(tol)

    cbest = cdll.minimize(fptr, lowerp, upperp, xlen, cpoints, gptr, 
                        cdiscrete, discretelen, cmaxit, ctol, cseedval)
    best = ctypes.cast(cbest, ctypes.POINTER(ctypes.c_double * len(upper))).contents
    """
    double (*fptr)(double*), 
    double* lower, 
    double* upper,
    size_t xlen, 
    size_t points,
    double (*gptr)(double*),
    size_t* discrete, 
    size_t discretelen, 
    size_t maxit,
    double tol, 
    size_t seedval
    """

    return [best[i] for i in range(len(upper))]


def main():
    def f(x):
        return x[0]*x[0] + x[1]*x[1] + 100
    
    bounds = [[-5.0, 5.0],[-5.0, 5.0]]

    print("Best:", minimize(f, bounds))
    

if __name__ == "__main__":
    main()
