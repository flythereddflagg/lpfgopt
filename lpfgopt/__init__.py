from __future__ import print_function
from lpfgopt.leapfrog import LeapFrog

# get version of lpfgopt
import os
mypackage_root_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(mypackage_root_dir, 'VERSION.txt')) as version_file:
    __version__ = version_file.read().strip()
del os


def minimize(fun, bounds, args=(), points=20, fconstraint=None, discrete=[],
             maxit=10000, tol=1e-5, seedval=None, pointset=None, callback=None):
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
                        discrete variables. These variables
                        will be constrained to integer values
                        by truncating any randomly generated
                        number (i.e. rounding down to the 
                        nearest integer absolute value)
        - maxit       : {int} maximum iterations
        - tol         : {float} convergence tolerance
        - seedval     : {int} random seed
        - pointset    : {array-like with shape=(m, n)} starting point set
        - callback    : {callable} function to be called after each iteration
    
    returns:
        - solution    : a dictionary containing the results of the optimization.
                        The members of the solution are listed below.
            
            - x           : {array-like, list} 
                            The solution vector or the vector of 
                            decision variables that produced the lowest 
                            objective function value
            - success     : {bool}
                            Whether or not the optimizer exited successfully.
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
        "callback"    : callback
        }
        
    lf = LeapFrog(**options)
    return lf.minimize()
