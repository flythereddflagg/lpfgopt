"""
file: c_leapfrog.py
Package: lpfgopt
Author: Mark Redd
Email: redddogjr@gmail.com
Website: http://www.r3eda.com/
About:
Contains the functions to access and use Leapfrog C Libarary from Python.

This algorithm is based the Leapfrogging Optimization Algorithm published 
by Dr. R. Russell Rhinehart. The following publications explain the technique:

- Rhinehart, R. R., M. Su, and U. Manimegalai-Sridhar, “Leapfrogging and 
  Synoptic Leapfrogging: a new optimization approach”, Computers & Chemical 
  Engineering, Vol. 40, 11 May 2012, pp. 67-81.

- Manimegalai-Sridhar, U., A. Govindarajan, and R. R. Rhinehart, “Improved 
  Initialization of Players in Leapfrogging Optimization”, Computers & 
  Chemical Engineering, Vol. 60, 2014, 426-429.

- Rhinehart, R. R., “Convergence Criterion in Optimilsation of Stochastic 
  Processes”, Computers & Chemical Engineering, Vol. 68, 4 Sept 2014, pp 1-6.
"""
import os

from ctypes import c_size_t, c_int, c_double, c_void_p, c_long
from ctypes import cast, CFUNCTYPE, POINTER
from ctypes import cdll as cdll_

from lpfgopt.opt_result import OptimizeResult

WIN_LIB = ".dll"
UNIX_LIB = ".so"
DARWIN_LIB = ".dylib"
MESSAGES = [
    "optimization completed successfully",
    "the maximum number of iterations was exceeded",
    "another error occured"
]


def load_leapfrog_lib():
    """
    Loads the leapfrog dynamic library for later use.
    @returns a reference to the ctypes library.
    """
    root = os.path.dirname(os.path.abspath(__file__))
    ext = WIN_LIB if os.name == 'nt' else UNIX_LIB
    filename = root + "/leapfrog_c" + WIN_LIB
    cdll = cdll_.LoadLibrary(filename)
    return cdll


def minimize(fun, bounds, args=(), points=20, fconstraint=None,
            discrete=[], maxit=10000, tol=1e-5, seedval=None, 
            pointset=None, callback=None, cdll_ptr=None, **kwargs):
    """
    Loads the compiled shared library named "leapfrog.dll" or
    "leapfrog.so" (depending on the operating system), runs
    the "leapfrog" function and returns the results.
    """

    cdll = load_leapfrog_lib() if cdll_ptr is None else cdll_ptr
    xlen = len(bounds)
    
    fptr, gptr, cbp = _setup_fun_ptrs(fun, args, fconstraint, callback)
    lowerp, upperp, solution = _setup_req_c_arrays(cdll, bounds, xlen)

    c_opt_arrs = _setup_opt_c_arrays(discrete, pointset, points, xlen)
    cdiscrete, discretelen, cpointset, init_pointset = c_opt_arrs

    CZERO = c_size_t(0)
    cseedval = CZERO if seedval is None else c_size_t(seedval)
    cxlen = c_size_t(xlen)
    cpoints = c_size_t(points)
    cmaxit = c_size_t(maxit)
    ctol = c_double(tol)

    cdll.minimize(
        fptr, lowerp, upperp, cxlen, cpoints, gptr, cdiscrete, discretelen, 
        cmaxit, ctol, cseedval, cpointset, init_pointset, cbp, solution
    )

    final_pointset = [[row[i] for i in range(xlen)] for row in list(cpointset)]
    output = list(solution)

    return OptimizeResult(
            x           = output[:xlen],
            success     = not bool(output[xlen]),
            status      = output[xlen],
            message     = MESSAGES[int(output[xlen])],
            fun         = output[xlen + 1],
            nfev        = int(output[xlen + 2] + points),
            nit         = int(output[xlen + 2]),
            final_error = output[xlen + 3],
            maxcv       = output[xlen + 4],
            best        = final_pointset[int(output[xlen + 5])], 
            worst       = final_pointset[int(output[xlen + 6])], 
            pointset    = final_pointset
        )


def _setup_fun_ptrs(fun, args=(), fconstraint=None, callback=None):
    """
    Makes C-compatible function pointers from Python function
    wrappers. @returns these pointers as a tuple fptr, gptr, cbp
    """
    
    def f(x, xlen):
        return fun([x[i] for i in range(xlen)], *args)

    def g(x, xlen):
        if fconstraint is None: return
        return fconstraint([x[i] for i in range(xlen)])

    def cb(x, xlen):
        if callback is None: return
        return callback([x[i] for i in range(xlen)])

    dprototype = CFUNCTYPE(c_double, POINTER(c_double), c_size_t)
    vprototype = CFUNCTYPE(c_void_p, POINTER(c_double), c_size_t)

    fptr = dprototype(f)
    gptr = POINTER(c_double)() if fconstraint is None else dprototype(g)
    cbp = POINTER(c_void_p)() if callback is None else vprototype(cb)
    
    return fptr, gptr, cbp


def _setup_req_c_arrays(cdll, bounds, xlen):
    """
    Converts the given, required Python array-likes into C array 
    pointers. @Returns pointers to lower, upper and solution arrays
    respectively.
    """

    lower = [i[0] for i in bounds]
    upper = [i[1] for i in bounds]
    lowerp = (c_double * xlen)(*lower)
    upperp = (c_double * xlen)(*upper)

    n_results = cast(cdll.N_RESULTS, POINTER(c_long)).contents.value

    solution = (c_double * (len(lower) + n_results))(*[
        0.0 for i in range(len(lower) + n_results)
    ])

    return lowerp, upperp, solution


def _setup_opt_c_arrays(discrete, pointset, points, xlen):

    cdiscrete = (c_size_t * len(discrete))(*discrete)
    discretelen = c_size_t(len(discrete))

    if pointset is None:
        pointset = [[0.0 for i in range(xlen)] for row in range(points)]
        init_pointset = c_int(1)
    else:
        init_pointset = c_int(0)

    pointset_list = [(c_double * xlen)(*row) for row in pointset]
    cpointset = (POINTER(c_double) * points)(*pointset_list)

    return cdiscrete, discretelen, cpointset, init_pointset


def _main():
    """
    runs a simple test of the C algorithm.
    """
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
    _main()
