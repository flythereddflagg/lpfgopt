#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
name: leap frog optimizer
version: 0.3 ALPHA
author: Mark Redd
email: redddogjr@gmail.com
optimizer website: http://www.r3eda.com/
"""

from random import random as rnd
from operator import itemgetter
from math import fabs, pi

# Needed from user: Intervals for all variables, the funcion that needs to be 
# minimized, other constraints


class LpFg(object):
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
        
    
    def minimize(self,f,intervals,points=None, constraints=None, tol=0.001,
        max_iterations=10000):
    
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
        
        return {
            "best":         b, 
            "worst":        w, 
            "final_error":  err, 
            "iterations":   iterations,
            "point_set":    pt_set
            }

### TESTS ###
import numpy as np
            
def f1(x):
    beta = sum([i**2 for i in x])
    return beta

intervals1 = [
    [-10000,10000],
    [-10000,10000]
    ]
    
avg_dist = sum([fabs(i[1]-i[0]) for i in intervals1])/len(intervals1)
frac = 0.05

def main(frac):
    """ example optimization """
    from time import time
    start = time()    
    opt1 = LpFg()
    
    success = 0
    print "\n"
    print "0 / 0 successful.",
    for i in range(1000):
        out = opt1.minimize(f1,intervals1, points=20, tol=0.001)
        b = out["best"]
        sol = [b[1],b[2],b[3]]
        goal = [0.0,0.0,0.0]
        err = sum([fabs(sol[j] - goal[j]) for j in range(len(sol))])/len(sol)
        
        if err < avg_dist * frac:
            success += 1
        print "\r%d / %d successful." % (success,i+1),

            
    stop = time()
    percent = int(frac * 100.0)
    print "\n"
    print "Optimization converged to within %d %s for %d out of 1000 "\
        "times." % (percent,"%",success)
    print "\n"
    # print "Optimization completed in %.9f seconds." % (stop-start)
    # print "\n"
    # print "Best:                 ", out["best"]
    # print "Worst:                ", out["worst"]
    # print "Final Error:          ", out["final_error"]
    # print "Number of iterations: ", out["iterations"]
    # print "\n"
    # for i in out["point_set"]:
        # print i
    # print "\n"
    
if __name__ == "__main__":
    main(frac)
    frac = 0.1
    main(frac)
    

"""
Convergence data with 20 points and tol=0.001:

Rastrigin function:
    Optimization converged to within  5 % for 727 out of 1000 times.
    Optimization converged to within 10 % for 982 out of 1000 times.

Sphere function:
    Optimization converged to within  5 % for 912 out of 1000 times.
    Optimization converged to within 10 % for 928 out of 1000 times.
"""