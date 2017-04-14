#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
name: leap frog optimizer
version: 0.4 ALPHA
author: Mark Redd
email: redddogjr@gmail.com
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
        “Convergence Criterion in Optimization of Stochastic Processes”, 
        Computers & Chemical Engineering, Vol. 68, 4 Sept 2014, pp 1-6.

"""

from random import random as rnd
from operator import itemgetter
from math import fabs, pi

# Needed from user: Intervals for all variables, the funcion that needs to be 
# minimized, other constraints


class LeapFrog(object):
    def __init__(self, points=20, constraints=None):
        self.points = points
        self.constraints = constraints


    def rand_input1(self, interval):
        return (interval[1]-interval[0])*rnd() + interval[0]


    def eval_bw(self, pt_set):
        z_sort = sorted(pt_set, key=itemgetter(1))
        best = z_sort[0]
        worst = z_sort[-1]
        return z_sort, best, worst


    def gen_pt_set(self, f, intervals, points=None, constraints=None):
        # 20 random points in space
        # [ID number, opt_val"f(x1,x2,x3,...xn)",x1, x2, x3,...xn]
        if points == None:
            points = self.points
        if constraints == None:
            constraints = self.constraints
            
        pt_set = []
        for i in range(points):
            pt1 = []
            for j in intervals:
                pt1.append(self.rand_input1(j))
            pt1.insert(0,f(pt1))
            pt1.insert(0,i)
            pt_set.append(pt1)
        return pt_set # use a dictionary?
        


    def get_new_w(self, f, b, w, intvl):
        inputs = []
        for i in range(len(w)-2):
            new_interval = sorted([b[i+2] ,2*w[i+2] - b[i+2]])
            if new_interval[0] < intvl[i][0]:
                new_interval[0] = intvl[i][0]
            if new_interval[1] > intvl[i][1]:
                new_interval[1] = intvl[i][1]
            w[i+2] = self.rand_input1(new_interval)
            inputs.append(w[i+2])
        w[1] = f(inputs)
        return w


    def replace_worst(self, w, list1):
        id_list = sorted(list1, key=itemgetter(0))
        id_list[w[0]] = w
        return id_list
    
    
    def err_var(self, b, pt_set):
        dist_sum = 0
        for i in pt_set:
            dist = sum([fabs(b[j+2] - i[j+2]) for j in range(len(i)-2)])
            dist_sum += dist
        return dist_sum
        
    
    def minimize(self,f,intervals,args=(),full_output=False, points=None, 
        constraints=None, tol=0.001, max_iterations=10000):
    
        if points == None:
            points = self.points
        if constraints == None:
            constraints = self.constraints
        pt_set = self.gen_pt_set(f,intervals,points)
        err = tol + 100.0
        iterations = 0
        while err > tol:
            sort_l, b, w = self.eval_bw(pt_set)
            w_new = self.get_new_w(f,b,w,intervals)
            pt_set = self.replace_worst(w_new,sort_l)
            err_obj = fabs(w[1] - b[1])
            err_var1 = self.err_var(b,pt_set)
            err = err_obj + err_var1 * 10.0
            iterations += 1
            if iterations > max_iterations:
                raise RuntimeError("Maximum Iterations Exceeded")
        if full_output == True:
            return {
                "best":         b, 
                "worst":        w, 
                "final_error":  err, 
                "iterations":   iterations,
                "point_set":    pt_set
                }
        elif full_output == False:
            return b
    
    
    def lfsolve(self,f,x0=None,intervals=None,args=(),full_output=False, 
        points=None, constraints=None, tol=0.01, s_step=1.1, 
        max_iterations=10000):

        def f_obj(x): return fabs(f(x))

        if x0 == None and intervals == None:
            raise ValueError("Initial guess (x0) or intervals must"\
                " be specified.")

        elif intervals == None:
            spread = 0.0
            root1 = 10.0
            it1 = 0
            while root1 > tol:
                spread += s_step
                intervals = []
                for i in xrange(len(x0)):
                    intervals.append([x0[i]-spread,x0[i]+spread])
                root = self.minimize(f_obj,intervals,args,full_output, points,
                    constraints, tol, max_iterations)
                root1 = root[1]
                it1 += 1
                if it1 > max_iterations:
                    raise RuntimeError("Maximum Iterations Exceeded")
            return root
        
        else:
            root = self.minimize(f_obj,intervals,args,full_output, points, 
            constraints, tol, max_iterations)
            return root
    
### TESTS ###
import numpy as np
            
def f1(x):
    beta = sum([i**2 for i in x])
    return beta

intervals1 = [
    [-20.0,20.0]
    ]

solver1 = True

def f2(x): return (x[0] - 3.0)*(x[0] + 5.0)*(x[0] - 10.0)

def main():
    """ example optimization """
    from time import time
    start = time()    
    opt1 = LeapFrog()
    if solver1:
        x = opt1.lfsolve(f2,x0=[0])
        stop = time()
        print x
        print stop - start
        return
        
    avg_dist = sum([fabs(i[1]-i[0]) for i in intervals1])/len(intervals1)
    frac5 = 0.05
    frac10 = 0.10
    goal = [0.0,0.0,0.0]
    percent1 = int(frac5 * 100.0)
    percent2 = int(frac10 * 100.0)
    tests = 1000
    success5 = 0
    success10 = 0
    print "\n"
    print "0 / 0 successful.",
    for i in range(tests):
        b = opt1.minimize(f1,intervals1, points=20, tol=0.001)
        sol = [b[1],b[2],b[3]]
        err = sum([fabs(sol[j] - goal[j]) for j in range(len(sol))])/len(sol)
        
        if err < avg_dist * frac5:
            success5 += 1
        if err < avg_dist * frac10:
            success10 += 1
            
        print "\r %d /%d (for %d%s), %d /%d (for %d%s) successful."\
            % (success5,i+1,percent1,"%",success10,i+1,percent2,"%"),

    stop = time()

    print "    %d optimization tests completed in %.9f seconds."\
        % (tests,stop-start)
    print "\n"

    
if __name__ == "__main__":
    main()

"""
Convergence data with 20 points and tol=0.001:

Rastrigin function: 727 /1000 (for 5%), 982 /1000 (for 10%) successful.

Sphere function: 901 /1000 (for 5%), 922 /1000 (for 10%) successful.
1000 optimization tests completed in 115.681999922 seconds.

"""
