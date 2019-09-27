import ctypes
import os

def minimize(fun,
            bounds,
            args=(),
            points=20,
            fconstraint=None,
            discrete=[],
            maxit=10000,
            tol=1e-3,
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

    cdll = ctypes.cdll.LoadLibrary(filename)

    def f(x):
        return fun(x, *args)

    prototype = ctypes.CFUNCTYPE(ctypes.c_double,
                                ctypes.POINTER(ctypes.c_double))
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
    xlen = len(lower)
    cxlen = ctypes.c_size_t(xlen)
    cpoints = ctypes.c_size_t(points)
    cdiscrete = (ctypes.c_size_t * len(discrete))(*discrete)
    discretelen = ctypes.c_size_t(len(discrete))
    cmaxit = ctypes.c_size_t(maxit)
    ctol = ctypes.c_double(tol)

    c_output = (ctypes.c_double * (len(lower)+5))(*[0.0 for i in range(len(lower)+5)])

    cdll.minimize(fptr, lowerp, upperp, cxlen, cpoints, gptr, cdiscrete,
                  discretelen, cmaxit, ctol, cseedval, c_output)

    output = list(c_output)
    return {
        'x' : output[:xlen],
        'obj' : output[xlen],
        'status' : output[xlen + 1],
        'nfev' : output[xlen + 2],
        'iters' : output[xlen + 3],
        'maxcv' : output[xlen + 4]
    }


def main():
    def f(x):
        return x[0]*x[0] + x[1]*x[1] + 100

    bounds = [[-5.0, 5.0],[-5.0, 5.0]]
    best = minimize(f, bounds, seedval = 1234)

    print("\nBest:")
    for key, value in best.items():
        print(f"    {key:<6} : {value}")


if __name__ == "__main__":
    main()
