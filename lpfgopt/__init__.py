"""
file: __init__.py
Package: lpfgopt
Author: Mark Redd
Email: redddogjr@gmail.com
Website: http://www.r3eda.com/
About:
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

API:
This package exposes the following API to make using the Leapfrogging 
Optimization Algorithm easier:

 - minimize() [function]: a general-use wrapper for optimization.
 - c_minimize() [function]: a wrapper for optimization explicitly using the 
    C library instead of the Python LeapFrog class.
 - load_leapfrog_lib() [function]: a function that returns a reference to the 
    leapfrog C library to avoid loading the library multiple times.
 - LeapFrog() [class]: a class for step-by-step analysis of leapfrog 
    optimization.
 - leapfrog_method() [function]: a wrapper function to allow the leapfrog method
    to be used with "scipy.optimize.minimize". Pass this function into the 
    'method' parameter to use it with scipy.
"""

from __future__ import print_function
from lpfgopt.leapfrog import LeapFrog
from lpfgopt.c_leapfrog import minimize as c_minimize, load_leapfrog_lib
from lpfgopt.scipy_min import leapfrog_method

# get version of lpfgopt
import os
mypackage_root_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(mypackage_root_dir, '../VERSION')) as version_file:
    __version__ = version_file.read().strip()
del os


def minimize(fun, bounds, args=(), points=20, fconstraint=None, discrete=[],
             maxit=10000, tol=1e-5, seedval=None, pointset=None, callback=None,
             use_c_lib=False, cdll_ptr=None):
    """
    General-use wrapper function to interface with the LeapFrog optimizer class.
    Contains the data and methods necessary to run a LeapFrog optimization.
    Accepts constraints, discrete variables and allows for a variety of options.
    
    parameters:
        - fun         : {callable} objective function 
        - bounds      : {array-like with shape=(n, 2)} variable upper and lower 
                        bounds
        - args        : {iterable} other arguments to be passed 
                        into the function
        - points      : {int} point set size
        - fconstraint : {callable} constraint function of the form g(x) <= 0
        - discrete    : {array-like} list of indices that correspond to 
                        discrete variables. These variables will be constrained 
                        to integer values by truncating any randomly generated
                        number (i.e. rounding down to the nearest absolute
                        integer value)
        - maxit       : {int} maximum iterations
        - tol         : {float} convergence tolerance
        - seedval     : {int} random seed
        - pointset    : {array-like with shape=(m, n)} starting point set
        - callback    : {callable} function to be called after each iteration
    
    returns:
        - solution    : a dictionary-like object containing the results of the 
                        optimization. The members of the solution are listed 
                        below.
            
            - x           : {array-like, list} The solution vector or the vector
                            of decision variables that produced the lowest 
                            objective function value
            - success     : {bool} Whether or not the optimizer exited successfully.
            - status      : {int}
                            Termination status of the optimizer. Its value 
                            depends on the underlying solver. Refer to 
                            message for details.
            - message     : {string}
                            Description of the cause of the termination.
            - fun         : {float}
                            The objective function value at 'x'
            - nfev        : {int}
                            The number of function evaluations of the objective
                            function
            - nit         : {int}
                            The number of iterations performed
            - maxcv       : {float}
                            The maximum constraint violation evaluated during
                            optimization
            - best        : {array-like, list} 
                            The member of the population that had the lowest
                            objective value in the point set having the form
                            [f(x), x[0], x[1], ..., x[n-1]]
            - worst       : {array-like, list} 
                            The member of the population that had the highest
                            objective value in the point set having the form
                            [f(x), x[0], x[1], ..., x[n-1]]
            - final_error : {float}
                            The optimization convergence value upon termination
            - pointset    : {array-like, list of lists}
                            The entire point set state upon termination having 
                            the form:
                            
                            [
                            [f(x[0]),   x[0][0],   x[0][1],   ..., x[0][n-1]],
                            [f(x[1]),   x[1][0],   x[1][1],   ..., x[1][n-1]],
                            ...,
                            [f(x[m-1]), x[m-1][0], x[m-1][1], ..., x[m-1][n-1]]
                            ]
                            
                            where n is the number of decision variables and m 
                            is the number of points in the search population.
    """
    options = {
        "fun"         : fun, 
        "bounds"      : bounds,
        "args"        : args,
        "points"      : points,
        "fconstraint" : fconstraint,
        "discrete"    : discrete,
        "maxit"       : maxit,
        "tol"         : tol,
        "seedval"     : seedval,
        "pointset"    : pointset,
        "callback"    : callback,
        "use_c_lib"   : use_c_lib,
        "cdll_ptr"    : cdll_ptr
        }
    
    if use_c_lib:
        return c_minimize(**options)
    lf = LeapFrog(**options)
    return lf.minimize()
