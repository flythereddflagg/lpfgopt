"""
filename: scipy_min.py
Package: lpfgopt
Author: Mark Redd
Email: redddogjr@gmail.com
Website: http://www.r3eda.com/
About:
Contains the wrapper functions for use with "scipy.optimize.minimize".

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
from lpfgopt.leapfrog import LeapFrog
from lpfgopt.c_leapfrog import minimize as c_minimize
try:
    from scipy.optimize import OptimizeResult
except ModuleNotFoundError:
    OptimizeResult = dict


def leapfrog_method(fun, x0, args, **kwargs):
    """
    Wrapper function for use in scipy.optimize.minimize
    basic usage:
        from lpfgopt.scipy_min import leapfrog_method
        from scipy.optimize import minimize

        solution = minimize(fun, [0], method=leapfrog_method,
                            bounds=bounds, options=options)
        print(solution.x)

    Other options can be passed into the dictionary 'options' argument. x0 has
    no meaning in this context so it is just filled with an arbitrary object.

    NOTES:
        - the 'constraints' variable is ignored for the leapfrog_method. To pass
            in constraints, a constraint function may be passed in as
            the 'fconstraint' option having the form: fconstraint(x) <= 0.
            The function should return a value greater than 0 whenever any
            constraint is violated. The optimizer checks this function for every
            new point and punishes objective when it is violated. 'fconstraint'
            is passed in the options dictionary (see lpfgopt.leapfrog.LeapFrog
            for more details)
    """
    kwargs["fun"]  = fun
    kwargs["x0"]   = x0
    kwargs["args"] = args

    use_clib = False if "use_clib" not in kwargs else kwargs["use_clib"]
    if use_clib:
        solution = c_minimize(**kwargs)
    else:
        lf = LeapFrog(**kwargs)
        solution = lf.minimize()

    opt_res = OptimizeResult()

    for key, val in solution.items():
        opt_res[key] = val

    opt_res["jac"]      = None
    opt_res["hess"]     = None
    opt_res["hess_inv"] = None
    opt_res["njev"]     = 0
    opt_res["nhev"]     = 0

    return opt_res
