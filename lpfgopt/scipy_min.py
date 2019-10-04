from lpfgopt.leapfrog import LeapFrog
from lpfgopt.c_leapfrog import minimize as c_minimize
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