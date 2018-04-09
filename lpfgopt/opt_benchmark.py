#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
file name      : opt_benchmark.py
title          : Leap Frog Optimizer
author         : Mark Redd
email          : redddogjr@gmail.com
github         : flythereddflagg/lpfgopt

written for python version: 3

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

class Solution():
    def __init__(self, f, intervals, start_pts=None, seed=None, args=(),
                points=20, constraints=None, tol=1e-5, rel=True, maxit=10000):
            
        self.f = f
        self.intervals = intervals
        self.args = args
        self.points = points
        self.constraints = constraints
        self.tol = tol
        self.rel = rel
        self.f_evals = 0
        self.maxit = maxit
        self.err = tol + 1000
        
        self.gen_pt_set() # generate the point set
        self.bi, self.wi = self.eval_bw()  # Get the indices of the best and worst points
        self.best = self.pt_set[self.bi]
        self.worst = self.pt_set[self.wi]
    
    def minimize(self):
        for iters in range(self.maxit):
            self.get_new_w() # leap frog over the best to get a new point
            self.pt_set[self.wi] = self.worst # replace worst with new point
            self.bi, self.wi = self.eval_bw()  # Get the indices of the best and worst points
            self.best = self.pt_set[self.bi] # set best
            self.worst = self.pt_set[self.wi] # set worst
            self.err = self.err_calc() # Get the overall error
            
            if self.err < self.tol: # Check for convergence
                return

        warn("Optimizer: Maximum Iterations Exceeded", RuntimeWarning)


    def err_calc(self):
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
        if self.rel:                # select relative or absolute error
            if prod(self.best) == 0.0: # avoid divide by zero errors
                self.best += 1.0e-8
            norm1 = self.best[0]
            norm2 = self.best[:1]
        else:
            norm1 = 1.0
            norm2 = 1.0

        err_obj = npabs((self.worst[0] - self.best[0])/norm1)  # Get the objective error
        dist_sum = 0
        for i in self.pt_set:                                 # sum over points
            dist = npsum(npabs((self.best[1:] - i[1:])/norm2)) # sum over variables
            dist_sum += dist

        return err_obj + dist_sum


    def eval_bw(self):
        """
        __PRIVATE FUNCTION__
        Return the indices of the best and worst points in the point set(pt_set).
        Method: Starts by generating a sorted index array based on column 0
        and then returns the first and last elements.
        """
        index1 = argsort(self.pt_set[:,0])
        return index1[0], index1[-1]


    def gen_pt_set(self):
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
        number_of_cols = len(self.intervals) + 1
        self.pt_set = zeros([self.points, number_of_cols])
        for n in range(self.points):                # for each point make a vector
            for v in range(1,number_of_cols):  # for each variable
                                                
                self.pt_set[n][v] = uniform(   # get a random input in the interval
                    self.intervals[v-1][0], 
                    self.intervals[v-1][1])
                self.pt_set[n][0] = self.f(self.pt_set[n][1:], *self.args) # get objective value


    def get_new_w(self):
        """
        __PRIVATE FUNCTION__
        Picks a new random interval by "Leapfrogging" the worst point over the best
        point. The new point is randomly chosen in the domain opposite the best 
        point with limits being the difference between the worst and best points and
        the bounds set by intervals in intvl. 
        """
        n_vars = len(self.worst)-1           ## number of variables
        inputs = zeros(n_vars)   ## make an input array
        for i in range(n_vars):
            ## pick an interval for w that is opposite b
            new_interval = array(
                [self.best[i+1] ,2*self.best[i+1] - self.worst[i+1]])
            new_interval.sort() ## put the lower limit first
            ## checking that interval does not go out of bounds
            if new_interval[0] < self.intervals[i][0]:
                new_interval[0] = self.intervals[i][0] ## if the interval is out of bounds    
            if new_interval[1] > self.intervals[i][1]: # change the upper or lower limit
                new_interval[1] = self.intervals[i][1] # to be the edge of the bounds
            self.worst[i+1] = uniform(new_interval[0], new_interval[1]) ## get a new input
            inputs[i] = self.worst[i+1]
        self.worst[0] = self.f(inputs, *self.args) ## get a new objective value from the new inputs


def minimize(f,intervals,args=(),full_output=False, points=20,
    constraints=None, tol=1e-5, rel=True, maxit=10000, start_pts=None,
    seed=None):
    """
    Minimize `f` on the array of intervals for each decision variable.

    * *Parameters:*  
      - `f`           - The objective function to be minimized. Will be called 
        as `f(x)` where `x` is an array-like object of decision variables based 
        on the length of `intervals`.
      - `intervals`   - Array-like object with `shape = (num_DV, 2)` (e.g. a 
        list of lists with the sub-lists all having a length of 2)
        the sub-arrays' first and second elements should hold the lower and 
        upper limits of each decision variable respecively.
      - `args`        - Other arguments to pass into objective 
        function (NOT YET FUNCTIONAL MAY STILL HAVE BUGS)
      - `full_output` - When set to `True` the function returns a dictionary of 
        the pertinent data from the optimization including:

        * `'best'`       : best point in the point set
        * `'worst'`      : worst point in the point set
        * `'final_error'`: final overall error
        * `'iterations'` : iterations to convergence or maxit if convergence 
            was not reached
        * `'point_set'`  : the final state of the point set

      - `points`      - Number of points to be used in the optimization. 
        Default is 20 points.
      - `constraints` - NOT YET FUNCTIONAL
      - `tol`         - Convergence tolerance or maximum error to converge 
        (will be based on relative or absolute error 
                      based on the state of the `rel` parameter)
      - `rel`         - When set to `True`, error/convergence is calculated on 
        a relative basis. When set to `False` 
                      error/convergence is calculated on absolute basis.
      - `maxit`       - Maximum iterations before returning. If maxit is 
        reached, the system returns a runtime warning.

    * *Returns:*  
      - `b`           - An array of floats that have the value of the optimized 
        objective function followed by the optimized values of each descision 
        variable (i.e. `[ f(x), x[0], x[1], x[2], ..., x[n-1] ]`)
      - `bdict`       - Returned instead of `b` when `full_output` 
        is set to True. A dictionary of the pertinent data from the optimization
        including:
        * `'best'`       : best point in the point set
        * `'worst'`      : worst point in the point set
        * `'final_error'`: final overall error
        * `'iterations'` : iterations to convergence or maxit if convergence was not reached
        * `'point_set'`  : the final state of the point set 
    """
    solution = Solution(
            f,
            intervals,
            start_pts,
            seed,
            args, 
            points,
            constraints, 
            tol, 
            rel, 
            maxit)
    solution.minimize()
    return solution.best



def _main():
    """__PRIVATE FUNCTION__ Some driver code to test the algorithm."""
    
    def test(x)      : return x[0]**2.0 + x[1]**2.0 + 3.0
    #def solve_test(x): return array([2 + x[0], 3 - x[1]])
    #def solve_test2(x, p): return array([2 + x[0], 3 - x[1] + p])
    
    int1 = [
        [-10.0,10.0],
        [-10.0,10.0]]
    x = minimize(test, int1)
    print('\nbest:', x, '\n')

"""
real    0m1.127s
user    0m1.056s
sys     0m0.022s
"""

if __name__ == "__main__":
    _main()

