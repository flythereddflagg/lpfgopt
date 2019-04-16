import numpy as np
from scipy.optimize import minimize as opt_min, OptimizeResult
from lpfgopt import minimize
from lpfgopt.scipy_min import leapfrog_method


def _f_test(x):
    return 2.0 * x[0]**2 + x[1]**2 + 3.0

_g1 = lambda x: x[0] + 3

_intvls = np.array([
    [-10.0, 10.0],
    [-10.0, 10.0]])

options = {
    "fun"         : _f_test, 
    "bounds"      : _intvls,
    "args"        : (),
    "points"      : 10,
    "fconstraint" : _g1,
    "discrete"    : np.array([0,1]),
    "maxit"       : 5000,
    "tol"         : 1e-3,
    "seedval"     : 1235,
    "pointset"    : None
    }

def numpy_test():
    """
    numpy and minimize compatibility test
    """    
    # Constrained and discrete optimization -----------------------------------    
    solution = minimize(**options)
   
    check = np.array([21.0, -3, 0])
    assert len(check) == len(solution["best"]), "Solutions do not match form."
    for i in range(len(solution["best"])):
        assert solution["best"][i] == check[i], f"numpy test failed on {i}"

        
def scipy_test():
    """
    scipy.optimize.minimize compatibility test
    """    
    # Constrained and discrete optimization -----------------------------------    
    del options['bounds']
    del options['args']
    del options['fun']
    
    def cb(x):
        print(x)
    
    solution = opt_min(_f_test, [0], bounds=_intvls, callback=cb,
                        method=leapfrog_method, options=options)
   
    check = np.array([-3, 0])
    print(check, solution.x)
    assert len(check) == len(solution.x), "Solutions do not match form."
    for i in range(len(solution.x)):
        assert solution.x[i] == check[i], f"numpy test failed on {i}"
    options['bounds'] = _intvls
    options['args'] = ()
    options['fun'] = _f_test
