import ctypes
import os
from opt_result import OptimizeResult

WIN_LIB = "/leapfrog.dll"
UNIX_LIB = "/leapfrog_c.so"
DARWIN_LIB = "/leapfrog_c.dylib"

def minimize(fun, bounds, args=(), points=20, fconstraint=None,
            discrete=[], maxit=10000, tol=1e-5, seedval=None, 
            pointset=None, callback=None, **kwargs):
    """
    Loads the compiled shared library named "leapfrog.dll" or
    "leapfrog.so" (depending on the operating system), runs
    the "leapfrog" function and returns the results.
    """

    root = os.path.dirname(os.path.abspath(__file__))
    if os.name == 'nt':
        filename = root + WIN_LIB
    else:
        filename = root + UNIX_LIB

    cdll = ctypes.cdll.LoadLibrary(filename)

    def f(x, xlen):
        return fun([x[i] for i in range(xlen)], *args)

    def g(x, xlen):
        if fconstraint is None: return
        return fconstraint([x[i] for i in range(xlen)])

    def cb(x, xlen):
        if callback is None: return
        return callback([x[i] for i in range(xlen)])

    dprototype = ctypes.CFUNCTYPE(
        ctypes.c_double,
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_size_t
    )
    vprototype = ctypes.CFUNCTYPE(
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_size_t
    )

    NULL_DPTR = ctypes.POINTER(ctypes.c_double)()
    NULL_VPTR = ctypes.POINTER(ctypes.c_void_p)()
    CZERO = ctypes.c_size_t(0)

    fptr = dprototype(f)
    gptr = NULL_DPTR if fconstraint is None else dprototype(g)
    cbp = NULL_VPTR if callback is None else vprototype(cb)
    cseedval = CZERO if seedval is None else ctypes.c_size_t(seedval)

    xlen = len(bounds)  
    lower = [i[0] for i in bounds]
    upper = [i[1] for i in bounds]
    lowerp = (ctypes.c_double * len(lower))(*lower)
    upperp = (ctypes.c_double * len(upper))(*upper)
    cxlen = ctypes.c_size_t(xlen)
    cpoints = ctypes.c_size_t(points)
    cdiscrete = (ctypes.c_size_t * len(discrete))(*discrete)
    discretelen = ctypes.c_size_t(len(discrete))
    cmaxit = ctypes.c_size_t(maxit)
    ctol = ctypes.c_double(tol)

    if pointset is None:
        pointset = [[0.0 for i in range(xlen)] for row in range(points)]
        init_pointset = ctypes.c_int(1)
    else:
        init_pointset = ctypes.c_int(0)

    pointset_list = [(ctypes.c_double * xlen)(*row) for row in pointset]
    cpointset = (ctypes.POINTER(ctypes.c_double) * points)(*pointset_list)

    n_results = ctypes.cast(
        cdll.N_RESULTS, 
        ctypes.POINTER(ctypes.c_long)
    ).contents.value

    solution = (ctypes.c_double * (len(lower) + n_results))(
                *[0.0 for i in range(len(lower) + n_results)])
    print("init done")
    cdll.minimize(
        fptr, lowerp, upperp, cxlen, cpoints, gptr, cdiscrete,
        discretelen, cmaxit, ctol, cseedval, cpointset, init_pointset,
        cbp, solution
    )
# void minimize(
#     double (*fptr)(double*, size_t), 
#     double* lower, 
#     double* upper,
#     size_t xlen, 
#     size_t points, 
#     double (*gptr)(double*, size_t),
#     size_t* discrete, 
#     size_t discretelen, 
#     size_t maxit,
#     double tol, 
#     size_t seedval, 
#     double** pointset,
#     int init_pointset, 
#     void (*callback)(double*, size_t),
#     double* solution
# );
    print("opt_done")
    final_pointset = [[row[i] for i in range(xlen)] for row in list(cpointset)]

    output = list(solution)
    messages = [
        "optimization completed successfully",
        "the maximum number of iterations was exceeded",
        "another error occured"
    ]
    return OptimizeResult(
            x           = output[:xlen],
            success     = not bool(output[xlen]),
            status      = output[xlen],
            message     = messages[int(output[xlen])],
            fun         = output[xlen + 1],
            nfev        = output[xlen + 2] + points,
            nit         = output[xlen + 2],
            final_error = output[xlen + 3],
            maxcv       = output[xlen + 4],
            best        = final_pointset[int(output[xlen + 5])], 
            worst       = final_pointset[int(output[xlen + 6])], 
            pointset    = final_pointset
        )


def main():
    def f(x):
        return x[0]*x[0] + x[1]*x[1] + 100
    
    def g(x):
        return -x[0] *x[0] + 10 - x[1]
    
    def cb(x):
        print(x)

    bounds = [[-5.0, 5.0],[-5.0, 5.0]]
    best = minimize(f, bounds, 
        seedval = 1234, callback = cb,
        fconstraint = g
    )
    print("\nOutput:")
    for key, value in best.items():
        print(f"    {key:<12} : {value}")


if __name__ == "__main__":
    main()
