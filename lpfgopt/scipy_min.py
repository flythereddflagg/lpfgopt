from lpfgopt.leapfrog import LeapFrog
from scipy.optimize import OptimizeResult

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
        - tol and constraints are currently handled in the options dictionary
            (see lpfgopt.leapfrog.LeapFrog for more details)
        - callback is not yet implemented and will be ignored
    """
    kwargs["fun"]  = fun
    kwargs["x0"]   = x0
    kwargs["args"] = args
        
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