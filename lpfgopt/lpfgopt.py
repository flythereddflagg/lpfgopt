#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
file name      : lpfgopt.py
title          : Leap Frog Optimizer
version        : 0.6.2 ALPHA
last modified  : 11 April 2017 
author         : Mark Redd
email          : redddogjr@gmail.com

written for python version: 2

optimizer algorithm website: http://www.r3eda.com/

about:

    This optimizer was written based on the algorithm published by
    Dr. R. Russell Rhinehart.

    A full explanation of the algorithm can be found at the following URL:

    http://www.r3eda.com/leapfrogging-optimization-algorithm/

    The following are "key references" published on
    the optimization website explaining the technique:

      - Rhinehart, R. R., M. Su, and U. Manimegalai-Sridhar,
        “Leapfrogging and Synoptic Leapfrogging: a new optimization approach”,
        Computers & Chemical Engineering, Vol. 40, 11 May 2012, pp. 67-81.

      - Manimegalai-Sridhar, U., A. Govindarajan, and R. R. Rhinehart,
        “Improved Initialization of Players in Leapfrogging Optimization”,
        Computers & Chemical Engineering, Vol. 60, 2014, 426-429.

      - Rhinehart, R. R.,
        “Convergence Criterion in Optimilsation of Stochastic Processes”,
        Computers & Chemical Engineering, Vol. 68, 4 Sept 2014, pp 1-6.

How to use the optimizer:
    Needed from user: Intervals for all variables, the function that needs to be
    minimized, other constraints
"""

from warnings import warn
from numpy.random import uniform
from numpy import prod, abs as npabs, sum as npsum, argsort, zeros, array

def _err_calc(b, w, pt_set, rel=True):
    """
    __PRIVATE FUNCTION__
    Calculate the error of the system to compare against the tolerance for
    convergence. In this scope error is defined as the sum of:
    
     - the absolute or relative error of the objective function between the best 
        and worst points
     - the sum of the absolute difference between each decision variable and 
        the corresponding variable value of the best point for every point.
    
    or mathmatically:
    
    err = |(f(w) - f(b))/f(b)| + sum_i=0(sum_j=0(|(b_ij-p_ij)/b_ij|)
    
    for i points and j variables.    
    """
    if rel:                # select relative or absolute error
        if prod(b) == 0.0: # avoid divide by zero errors
            b += 1.0e-8
        norm1 = b[0]
        norm2 = b[:1]
    else:
        norm1 = 1.0
        norm2 = 1.0

    err_obj = npabs((w[0] - b[0])/norm1)            # Get the objective error
    dist_sum = 0
    for i in pt_set:                                 # sum over points
        dist = npsum(npabs((b[1:] - i[1:])/norm2)) # sum over variables
        dist_sum += dist

    return err_obj + dist_sum


def _eval_bw(pt_set):
    """
    __PRIVATE FUNCTION__
    Return the indices of the best and worst points in the point set(pt_set).
    Method: Starts by generating a sorted index array based on column 0
    and then returns the first and last elements.
    """
    index1 = argsort(pt_set[:,0])
    return index1[0], index1[-1]


def _gen_pt_set(f, intervals, points=20, constraints=None, args=()):
    """
    __PRIVATE FUNCTION__
    Generates a point set with "points" rows and "len(intervals)+1" columns
    This matrix will be the initial point set that will be used in the Leapfrog
    Algorithm. 
    Args:
        f           - The objective function to be optimized
        intervals   - A 2d array with n rows and 2 columns with n being the 
                      number of decision variables and each column being the 
                      lower and upper bounds on each variable respecively.
        points      - The number of randomly generated points to be used in the
                      optimization.
        constraints - NOT YET FUNCTIONAL
    
    The output matrix will have columns of the following form:
    
        [f(x), x[0], x[1], x[2],...x[n-1]]
    """
    number_of_cols = len(intervals) + 1
    pt_set = zeros([points, number_of_cols])
    for n in xrange(points):                # for each point make a vector
        for v in xrange(1,number_of_cols):  # for each variable
                                            
            pt_set[n][v] = uniform(         # get a random input in the interval
                intervals[v-1][0], 
                intervals[v-1][1])
            pt_set[n][0] = f(pt_set[n][1:], *args) # get objective value
    return pt_set


def _get_new_w(f, b, w, intvl, args=()):
    """
    __PRIVATE FUNCTION__
    Picks a new random interval by "Leapfrogging" the worst point over the best
    point. The new point is randomly chosen in the domain opposite the best 
    point with limits being the difference between the worst and best points and
    the bounds set by intervals in intvl. 
    """
    n_vars = len(w)-1           ## number of variables
    inputs = zeros(n_vars)   ## make an input array
    for i in xrange(n_vars):
        ## pick an interval for w that is opposite b
        new_interval = array([b[i+1] ,2*b[i+1] - w[i+1]])
        new_interval.sort() ## put the lower limit first
        ## checking that interval does not go out of bounds
        if new_interval[0] < intvl[i][0]:
            new_interval[0] = intvl[i][0] ## if the interval is out of bounds    
        if new_interval[1] > intvl[i][1]: # change the upper or lower limit
            new_interval[1] = intvl[i][1] # to be the edge of the bounds
        w[i+1] = uniform(new_interval[0], new_interval[1]) ## get a new input
        inputs[i] = w[i+1]
    w[0] = f(inputs, *args) ## get a new objective value from the new inputs
    return w


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

    for iters in xrange(maxit):

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

def lfsolve(f,x0=None,intervals=None,args=(),full_output=False,
        points=20, constraints=None, tol=1e-5, s_step=None, maxit=10000):
    """
    A numerical solver based on the Leapfrogging algorithm.
    Solver works by minimizing the sum of the absolute value of the outputs.
    This should return an optimal value of zero if the root is bracketed.
    
    Inputs may be intervals that bracket the root or a guess value vector from 
    which intervals are guessed and then made larger if a root is not found. 
    This is done by calculating a spread step and then expanding as needed 
    until a root is found.
    
    Args:
        f           - Solver function f(x) = 0
        args        - Other arguments to pass into objective function
        full_output - When set to true the function returns a dictionary of the
                        pertinent data from the optimization including:
                        
                        * root        : Values of the vector x such that:
                                        f(x) = 0
                        * final_error : Final value of f_obj
                        * opt_iters   : Final number of iterations in the 
                                        optimizer to find the root
                        * sol_iters   : Number of iterations in the solver 
                                        needed to bracket the root
                        * point_set   : Final point set from the optimizer
                        
        points      - Number of points to be used in the optimization. Default
                        is 20 points.
        constraints - NOT YET FUNCTIONAL
        tol         - Convergence tolerance or maximum error to converge.
        maxit       - Maximum attempts to bracket the root before returning. 
                        If maxit is reached the system returns a 
                        runtime warning.
    """
    # define the solver objective function
    def f_obj(x,*args): return npsum(npabs(f(x,*args))) 
    
    it1 = 0 # initialize the solver iterations
    
    if x0 == None and intervals == None: 
        # check if nothing is specified for guess or intervals
        raise ValueError("Initial guess (x0) or intervals must"\
            " be specified.")

    elif intervals == None: # if a guess value for each DV is specified
        nvs = len(x0)       # number of variables = length of the guess vector
        
        if s_step == None:  # if no spread step is specified estimate one based
            s_step = f_obj(x0,*args) * 0.1 # on the current value of the 
                                     # objective function
        spread = 0.0
        
        for it1 in xrange(maxit):
            spread += s_step                # guess an interval centered on x0
            intervals = zeros([nvs,2])   # with bounds = x0 +- spread
            for i in xrange(nvs):
                intervals[i,0] = x0[i] - spread
                intervals[i,1] = x0[i] + spread
            
            # run the optimization
            root = minimize(f_obj,intervals=intervals,args=args,
                full_output=True, points=points, constraints=constraints,
                tol=tol,rel=False, maxit=maxit)

            root_err = root['best'][0] # get the distance from zero
            
            if root_err < tol:         # check for convergence
                if full_output == True:
                    return {
                        "root":         root['best'][1:],
                        "final_error":  root['best'][0],
                        "opt_iters":    root['iterations'],
                        "sol_iters":    it1 + 1,
                        "point_set":    root["point_set"]
                        }
                else:
                    return root['best'][1:]
                    
        warn("Solver: Maximum Iterations Exceeded. \nSolver was unable to"\
             "bracket the root.", RuntimeWarning)

    else:
        # run the optimization based on the intervals specified
        root = minimize(f_obj,intervals=intervals,args=args,full_output=True,
                points=points, constraints=constraints, tol=tol,
                rel=False, maxit=maxit)
    
    if full_output == True:
        return {
            "root":         root['best'][1:],
            "final_error":  root['best'][0],
            "opt_iters":    root['iterations'],
            "sol_iters":    it1 + 1,
            "point_set":    root["point_set"]
            }
    else:
        return root['best'][1:]

#    def int_minimize(f,x0=None,intervals=None,args=(),full_output=False,
#        points=20, constraints=None, tol=1e-5, s_step=None, maxit=10000):
#        
#        pass

def _main():
    """__PRIVATE FUNCTION__ Some driver code to test the algorithm."""
    
    def test(x)      : return x[0]**2.0 + x[1]**2.0 + 3.0
    #def solve_test(x): return array([2 + x[0], 3 - x[1]])
    #def solve_test2(x, p): return array([2 + x[0], 3 - x[1] + p])
    
    int1 = [
        [-10.0,10.0],
        [-10.0,10.0]]
    x = minimize(test, int1, full_output=True)
    print '\nbest:', x['best'], '\n'
"""    
    x0 = [-3.0,3.0]
    x = lfsolve(solve_test2, x0, args=(3.0,), full_output=True)
    print x['opt_iters']
    print x['sol_iters']
    print 'root:', x['root'], '\n'

"""
"""
real    0m1.127s
user    0m1.056s
sys     0m0.022s
"""

if __name__ == "__main__":
    _main()

