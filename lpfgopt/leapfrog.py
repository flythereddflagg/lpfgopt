#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import seed, uniform
from warnings import warn

class LeapFrog():
    """
    Contains the data and methods necessary to run a LeapFrog optimization.
    Accepts constraints, discrete variables and allows for a variety of options.
    
    The Genetic object constructor takes the following parameters:
            - fun             : objective function
            - bounds          : variable upper and lower bounds
            - con             : constraint function
            - discrete        : list of indices that correspond to 
                                discrete variables. These variables
                                will be constrained to integer values
                                by truncating any randomly generated
                                number (i.e. rounding down to the 
                                nearest integer absolute value)
            - pop_size        : point set size
            - seed            : random seed
    """
    def __init__(
                self, 
                fun, 
                bounds,
                args=(),
                points=20,
                fconstraint=None,
                discrete=[],
                maxit=10000,
                full_output=False, 
                tol=1e-5,
                seedval=None):
                
        self.fun         = fun
        self.bounds      = bounds
        self.args        = args
        self.points      = points
        self.fconstraint = fconstraint
        self.discrete    = discrete
        self.maxit       = maxit
        self.full_output = full_output
        self.tol         = tol
        self.seed        = seedval
        self.nfev        = 0
        
        # seed the random number generator
        seed(self.seed)
        
        # build the point set
        self.n_columns = len(self.bounds) + 1
        self.pointset = [
            [0.0 for i in range(self.n_columns)] for j in range(self.points)
            ]
        
        for row in range(points):
            for column in range(1, self.n_columns):
                self.pointset[row][column] = uniform(*self.bounds[column-1])
            self.pointset[row][1:] = self.enforce_discrete(
                                                    self.pointset[row][1:])
            self.pointset[row][0] = self.f(self.pointset[row][1:])
        
        self.enforce_constraints()
        
        # get the initial best and worst
        self.besti, self.worsti = self.get_best_worst()
    

    
    def f(self, x):
        self.nfev += 1
        return self.fun(x, *self.args)
    
    
    def enforce_constraints(self):
        """
        Enforces the constraint penalties on any infeasible member of the 
        point set. The penalty to any infeasible member is to be made worse 
        than the worst member of the point set. This will ensure all 
        infeasible members are eventually eliminated.
        
        If a constraint function is not specified, then this 
        function does nothing.
        
        A constraint function must be designed to return a single 
        value of the form:
        
        fconstraint(x) <= 0
        
        This means a return value > 0 from the constraint function
        indicates the constraint has been violated, otherwise the point
        is feasible.
        """
        if self.fconstraint is not None:
            big = max([abs(i[0]) for i in self.pointset])
            for i in range(self.points):
                constraint_value = self.fconstraint(self.pointset[i][1:])
                if constraint_value > 0:
                    self.pointset[i][0] = big + constraint_value
    
    
    def enforce_discrete(self, args):
        args = args.copy()
        for i in self.discrete:
            args[i] = int(args[i])
        return args
    
    def get_best_worst(self):
        best, worst = 0, 0
        
        for i in range(self.points):
            if self.pointset[i][0] < self.pointset[best][0]:
                best = i
        
            if self.pointset[i][0] > self.pointset[worst][0]:
                worst = i
        
        return best, worst
        

    def leapfrog(self, besti, worsti):
        
        new_point = [0.0 for i in range(self.n_columns)]
        
        for i in range(self.n_columns-1):
            new_bound = sorted([
                self.pointset[self.besti][i+1], 
                self.pointset[self.besti][i+1] * 2 -\
                    self.pointset[self.worsti][i+1]
                ])
            
            if new_bound[0] < self.bounds[i][0]:
                new_bound[0] = self.bounds[i][0]
            
            if new_bound[1] > self.bounds[i][1]:
                new_bound[1] = self.bounds[i][1]
            
            new_point[i] = uniform(*new_bound)
        
        new_point[1:] = self.enforce_discrete(new_point[1:])
        new_point[0] = self.f(new_point[1:])
        
        return new_point
    
    
    def calculate_convergence(self):
        obj_best = self.pointset[self.besti][0]
        point_best = self.pointset[self.besti][1:]
        
        obj_worst = self.pointset[self.worsti][0]

        if abs(obj_best) < self.tol:
            norm1 = 1.0         
        else:
            norm1 = obj_best

        err_obj = abs((obj_worst - obj_best)/norm1) 
        
        dist_sum = 0
        for point in self.pointset:
            vars = point[1:]
            for i in range(self.n_columns-1):
                if abs(point_best[i]) < self.tol:
                    norm2 = 1.0
                else:
                    norm2 = point_best[i]
                    
                dist_sum += abs((point_best[i] - vars[i])/norm2)
        
        avg_dist = dist_sum / (self.n_columns + self.points - 1)
        
        return err_obj + avg_dist
        
    
    def minimize(self):
        for iters in range(self.maxit):
            self.besti, self.worsti = self.get_best_worst()
            self.pointset[self.worsti] = self.leapfrog(self.besti, self.worsti)
            self.enforce_constraints()
            self.error = self.calculate_convergence()
            
            if self.error < self.tol:
                if self.full_output == True:
                    return {
                        "best"        : self.pointset[self.besti],
                        "worst"       : self.pointset[self.worsti],
                        "final_error" : self.error,
                        "iterations"  : iters + 1,
                        "pointset"    : self.pointset,
                        "nfev"        : self.nfev,
                        "message"     : "Tolerance condition satisfied"
                        }
                else:
                    return self.pointset[self.besti]

        
        if self.full_output == True:
            return {
                "best"        : self.pointset[self.besti],
                "worst"       : self.pointset[self.worsti],
                "final_error" : self.error,
                "iterations"  : iters + 1,
                "pointset"    : self.pointset,
                "nfev"        : self.nfev,
                "message"     : "Maximum Iterations Exceeded"
                }
        else:
            return self.pointset[self.besti]

    

    
def _main():

    test = lambda x: x[0]**2.0 + x[1]**2.0 + 3.0
    
    int2 = [
        [-10.0,10.0],
        [-10.0,10.0]]
    
    
    lf = LeapFrog(test, int2, full_output=True, tol=1e-3, points=2)
    x = lf.minimize() 
    print()
    for key in [
            "best",      
            "worst",      
            "final_error",
            "iterations",   
            "nfev",       
            "message"]:
        print(f" {key:15} : {x[key]}")
    print("\nPoint Set:")
    for i in x['pointset']:
        print(i)
       
       
    g1 = lambda x: -2 * x[0] + 3
    lf = LeapFrog(test, int2, full_output=True, tol=1e-3, points=20,
                  fconstraint=g1, discrete=[0,1], maxit=10000)
    x = lf.minimize() 
    print()
    for key in [
            "best",      
            "worst",      
            "final_error",
            "iterations",   
            "nfev",       
            "message"]:
        print(f" {key:15} : {x[key]}")
    print("\nPoint Set:")
    for i in x['pointset']:
        print(i)
       

if __name__ == "__main__":
    _main()