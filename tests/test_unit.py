import timeit
import time

from lpfgopt.leapfrog import LeapFrog
from . import *


def _f_test(x, offset):
    return 2.0 * x[0]**2 + x[1]**2 + offset

_g1 = lambda x: x[0] + 3

_intvls = [
    [-10.0, 10.0],
    [-10.0, 10.0]]

_starting_points = [
    [-3.269716623,   -7.930871],
    [-0.301065303,   2.3311285],
    [-7.378448241,   6.1100162],
    [-0.191330390,   7.0158780],
    [-7.217230801,   -8.815178],
    [-6.878029799,   4.0923533],
    [-4.587077226,   9.0630253],
    [-9.755670223,   -8.901648],
    [4.9019506940,   -3.184652],
    [-7.532104399,   1.6987271],
    [5.4372269021,   0.5777975],
    [-7.739404401,   9.8297502],
    [0.5493843932,   5.6662483],
    [9.2385537811,   -7.513752],
    [-1.295963317,   -4.268123],
    [7.7269409075,   1.4205298],
    [-4.322107922,   6.0013770],
    [-7.112370271,   9.4093474],
    [1.9372210724,   7.5056536],
    [7.0920413003,  -9.8860190]]

_options = {
    "fun"         : _f_test,
    "bounds"      : _intvls,
    "args"        : (3.0,),
    "points"      : len(_starting_points),
    "fconstraint" : _g1,
    "discrete"    : [0,1],
    "maxit"       : 5000,
    "tol"         : 1e-3,
    "seedval"     : 1235,
    "pointset"    : _starting_points
    }


def test_unit():
    """
    General use unit test; performs Constrained and discrete optimization
    """
    lf = LeapFrog(**_options)

    print("\nCONSTRAINED AND DISCRETE OPTIMIZATION:\nBEFORE:")
    print(lf)
    solution = lf.minimize()
    print("AFTER:")
    print(lf)

    print("\nPoint Set:")
    for i in solution['pointset']:
        print(i)
    print()

    check = [21.0, -3, 0]
    for i in range(len(solution["best"])):
        assert solution["best"][i] == check[i], f"Unit test failed on {i}"


def test_unit_c():
    """
    General use unit test for the C code. Performs 
    Constrained and discrete optimization
    """
    solution = c_minimize(**_options)

    print(solution)

    check = [ -3, 0]
    for i in range(len(solution["best"])):
        assert solution["best"][i] == check[i], f"Unit test failed on {i}"


def test_unit_c2():
    """
    General use unit test for the C code. Performs 
    Constrained and discrete optimization
    """
    solution = minimize(**_options, use_c_lib=True)

    print(solution)

    check = [ -3, 0]
    for i in range(len(solution["best"])):
        assert solution["best"][i] == check[i], f"Unit test failed on {i}"


def test_c_vs_py():
    """
    General use unit test for the C code. Performs 
    Constrained and discrete optimization
    """
    cfev, pyfev = 0, 0
    ntimes = 10
    start = time.perf_counter()
    for i in range(ntimes):
        cfev += c_minimize(**_options, cdll_ptr=lpfg_lib).nfev
        # minimize(**_options, use_c_lib=True, cdll_ptr=lpfg_lib)
        # minimize(**_options)
    stop = time.perf_counter()
    ctime = stop - start

    start = time.perf_counter()
    for i in range(ntimes):
        # minimize(**_options, use_c_lib=True, cdll_ptr=lpfg_lib)
        pyfev += minimize(**_options).nfev
    stop = time.perf_counter()
    pytime = stop - start


    assert False,\
        f"""C code is underperforming
Ctime : {ctime:.12f} fev: {cfev:4d} t/fev: {ctime/cfev}
Pytime: {pytime:.12f} fev: {pyfev:4d} t/fev: {pytime/pyfev}
{((pytime/pyfev) - (ctime/cfev))/(pytime/pyfev)*100} % better than Python
"""
