def minimize(f,intervals,args=(),full_output=False, points=20,
    constraints=None, tol=1e-5, rel=True, maxit=10000):
    """
    Minimize f on the array of intervals for each decision variable.
    
    Args:
        f           - The objective function to be minimized
        args        - Other arguments to pass into objective function
        full_output - When set to true the function returns a dictionary of the
                        pertinent data from the optimization including:
                        
                        * best       : best point in the point set
                        * worst      : worst point in the point set
                        * final_error: final overall error
                        * iterations : iterations to convergence or max
                        * point_set  : the final state of the point set
                        
        points      - Number of points to be used in the optimization. Default
                        is 20 points.
        constraints - NOT YET FUNCTIONAL
        tol         - Convergence tolerance or maximum error to converge.
        maxit       - Maximum iterations before returning. If maxit is reached
                        the system returns a runtime warning.
    """
    pt_set = _gen_pt_set(f,intervals,points, args=args) # generate the point set

    for iters in range(maxit):

        bi, wi = _eval_bw(pt_set)  # Get the indices of the best and worst points
        b = pt_set[bi]
        w = pt_set[wi]
        w_new = _get_new_w(f,b,w,intervals, args=args) 
        pt_set[wi] = w_new                # Replace the worst with the new point
        err = _err_calc(b, w_new, pt_set, rel) # Get the overall error
        
        if err < tol:                     # Check for convergence
            if full_output == True:
                return {
                    "best":         b,
                    "worst":        w,
                    "final_error":  err,
                    "iterations":   iters + 1,
                    "point_set":    pt_set
                    }
            else:
                return b

    warn("Optimizer: Maximum Iterations Exceeded", RuntimeWarning)
    
    if full_output == True:
        return {
            "best":         b,
            "worst":        w,
            "final_error":  err,
            "iterations":   iters + 1,
            "point_set":    pt_set
            }
    else:
        return b