#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
name: leap frog optimizer (Modular Edition)
version: 0.5 ALPHA
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
# to be added
# args
# integer optimizer
# numpy additions
# numerical additons

from numpy.random import uniform
import numpy as np
from operator import itemgetter
from math import fabs
from time import time

# Needed from user: Intervals for all variables, the funcion that needs to be 
# minimized, other constraints



def rand_input1(interval):
    return uniform(interval[0], interval[1])


def eval_bw(pt_set):
    z_sort = sorted(pt_set, key=itemgetter(1))
    best = z_sort[0]
    worst = z_sort[-1]
    return z_sort, best, worst


def gen_pt_set(f, intervals, points=20, constraints=None):
    # 20 random points in space
    # [ID number, opt_val"f(x1,x2,x3,...xn)",x1, x2, x3,...xn]            
    start = time()
    number_of_vars = len(intervals)
    pt_set = np.zeros([points, number_of_vars + 2]) # or np.empty
    for n in xrange(points):
        for v in xrange(2,number_of_vars + 2):
            pt_set[n][v] = uniform(intervals[v-2][0], intervals[v-2][1])
        pt_set[n][1] = f(pt_set[n][1:])
        pt_set[n][0] = n
    new_time = time() - start
    print pt_set
    start = time()
    pt_set = []
    for i in range(points):
        pt1 = []
        for j in intervals:
            pt1.append(rand_input1(j))
        pt1.insert(0,f(pt1))
        pt1.insert(0,i)
        pt_set.append(pt1)
    old_time = time() - start
    for i in pt_set:
        print i
    print "Times:", np.array([old_time, new_time])
    return pt_set # use a dictionary?
    

def get_new_w(f, b, w, intvl):
    inputs = []
    for i in range(len(w)-2):
        new_interval = sorted([b[i+2] ,2*w[i+2] - b[i+2]])
        if new_interval[0] < intvl[i][0]:
            new_interval[0] = intvl[i][0]
        if new_interval[1] > intvl[i][1]:
            new_interval[1] = intvl[i][1]
        w[i+2] = rand_input1(new_interval)
        inputs.append(w[i+2])
    w[1] = f(inputs)
    return w


def replace_worst(w, list1):
    id_list = sorted(list1, key=itemgetter(0))
    id_list[w[0]] = w
    return id_list


def err_var(b, pt_set):
    dist_sum = 0
    for i in pt_set:
        dist = sum([fabs(b[j+2] - i[j+2]) for j in range(len(i)-2)])
        dist_sum += dist
    return dist_sum
    

def minimize(f,intervals,args=(),full_output=False, points=20, 
    constraints=None, tol=1e-5, max_iterations=10000):

    pt_set = gen_pt_set(f,intervals,points)
    err = tol + 100.0
    iterations = 0
    while err > tol:
        sort_l, b, w = eval_bw(pt_set)
        w_new = get_new_w(f,b,w,intervals)
        pt_set = replace_worst(w_new,sort_l)
        err_obj = fabs((w[1] - b[1])/b[1])
        err_var1 = err_var(b,pt_set)
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

        
def lfsolver(f,x0=None,intervals=None,args=(),full_output=False, 
        points=20, constraints=None, tol=0.01, s_step=1.01, 
        max_iterations=10000):

        def f_obj(x): return fabs(sum(f(x)))

        if x0 == None and intervals == None:
            raise ValueError("Initial guess (x0) or intervals must"\
                " be specified.")

        elif intervals == None:
            spread = 0.0
            root_err = tol*1000.0
            it1 = 0
            while root_err > tol:
                spread += s_step
                intervals = []
                for i in xrange(len(x0)):
                    intervals.append([x0[i]-spread,x0[i]+spread])
                
                root = minimize(f_obj,intervals,args,full_output, points,
                    constraints, tol, max_iterations)
                root_err = root[1]
                it1 += 1
                if it1 > max_iterations:
                    raise RuntimeError("Maximum Iterations Exceeded")
        
        else:
            root = minimize(f_obj,intervals,args,full_output, points, 
            constraints, tol, max_iterations)
        
        root.pop(0)
        root.pop(0)
        return root

def test(x): return x[0]**2.0 + x[1]**2.0 + 3.0
        
def main():
    int1 = [
        [-10.0,10.0],
        [-10.0,10.0]]
    x = minimize(test, int1, full_output=True)
    print '\nbest:', x['best'], '\n'
   
if __name__ == "__main__":
    main()
