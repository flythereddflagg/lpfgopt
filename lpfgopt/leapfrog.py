"""
filename: leapfrog.py
Package: lpfgopt
Author: Mark Redd
Email: redddogjr@gmail.com
Website: http://www.r3eda.com/
About:
Contains the Leapfrog class for general use in Leapfrog Optimization in Python.

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

Example usage:
"""
from random import seed, uniform
from lpfgopt.opt_result import OptimizeResult

class LeapFrog():
    """
    Contains the data and methods necessary to run a LeapFrog optimization.
    Accepts constraints, discrete variables and allows for a variety of options.
    
    The LeapFrog object constructor takes the following parameters:
        - fun         : objective function 
        - bounds      : variable upper and lower bounds
        - args        : other arguments to be passed into the function
        - points      : point set size
        - fconstraint : constraint function
        - discrete    : list of indices that correspond to 
                        discrete variables. These variables
                        will be constrained to integer values
                        by truncating any randomly generated
                        number (i.e. rounding down to the 
                        nearest integer absolute value)
        - maxit       : maximum iterations
        - tol         : convergence tolerance
        - seedval     : random seed
        - pointset    : starting point set
        - callback    : function to be called after each iteration
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
                tol=1e-5,
                seedval=None,
                pointset=None,
                callback=None,
                **kwargs):
                
        self.fun         = fun
        self.bounds      = bounds
        self.args        = args
        self.points      = points
        self.fconstraint = fconstraint
        self.discrete    = discrete
        self.maxit       = maxit
        self.tol         = tol
        self.seed        = seedval
        self.callback    = callback
        self.nfev        = 0
        self.maxcv       = 0
        self.total_iters = 0
        self.error       = None

        
        # seed the random number generator
        seed(self.seed)
        
        # build the point set
        self.n_columns = len(self.bounds) + 1
        
        self.pointset = [
            [0.0 for i in range(self.n_columns)] for j in range(self.points)
            ]
        
        for row in range(points):
            for column in range(1, self.n_columns):
                if pointset is None:
                    self.pointset[row][column] = uniform(*self.bounds[column-1])
                else:
                   self.pointset[row][column] = pointset[row][column-1] 
            
            self.pointset[row][1:] = self.enforce_discrete(
                                                    self.pointset[row][1:])
            self.pointset[row][0] = self.f(self.pointset[row][1:])
        
        self.enforce_constraints()
        
        # get the initial best and worst
        self.besti, self.worsti = self.get_best_worst()
    
    
    def __repr__(self):
        return f"""
Leap Frog Optimizer State:
 best obj      : {self.pointset[self.besti][0]}
 best point    : {self.pointset[self.besti][1:]}
 fun evals     : {self.nfev}
 iterations    : {self.total_iters}
 maxcv         : {self.maxcv}
 best          : {self.pointset[self.besti]}
 worst         : {self.pointset[self.worsti]}
 current error : {self.error}
 """
    
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
                    if constraint_value > self.maxcv:
                        self.maxcv = constraint_value
                    self.pointset[i][0] = big + constraint_value
    
    
    def enforce_discrete(self, args):
        """
        Returns a copy of @param args with the indices in the class
        parameter 'self.discrete' made to be integer values by
        truncating the float value.
        """
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
        """
        Core step in the leapfrogging algorithm. Takes a best and worst
        index of the 'pointset' and generates a new point in place of 
        the worst by "leapfrogging" over the point corresponding to the 
        'best' index.       
        """
        
        punish = abs(self.pointset[worsti][0])
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
            
            new_point[i+1] = uniform(*new_bound)
        
        new_point[1:] = self.enforce_discrete(new_point[1:])       
        new_point[0]  = self.f(new_point[1:])
        
        if self.fconstraint is not None:
            constraint_value = self.fconstraint(new_point[1:])
            if constraint_value > 0:
                if constraint_value > self.maxcv:
                        self.maxcv = constraint_value
                new_point[0] += constraint_value + punish

        return new_point
    
    
    def calculate_convergence(self):
        """
        Calculates a convergence value by calculating the relative 
        distance between the objective values of the best and 
        worst points and average distance between each point and
        the best point and summing the two values together. This
        convergence value is taken as the error of the optimization
        and once the error <= tolerance the optimization ends.
        """
        obj_best = self.pointset[self.besti][0]
        point_best = self.pointset[self.besti][1:]
        
        obj_worst = self.pointset[self.worsti][0]

        if abs(obj_best) < self.tol:
            norm1 = self.tol        
        else:
            norm1 = obj_best

        err_obj = abs((obj_worst - obj_best)/norm1) 
        
        dist_sum = 0.0
        constraint_penalty = 0.0
        for point in self.pointset:
            vars = point[1:]
            
            if self.fconstraint is not None and self.fconstraint(vars) > 0.0:
                    constraint_penalty = 2 * self.tol
                
            for i in range(self.n_columns-1):
                if abs(point_best[i]) < self.tol:
                    norm1 = self.tol        
                else:
                    norm1 = point_best[i]
                dist_sum += abs((point_best[i] - vars[i])/norm1)
        
        return err_obj + dist_sum + constraint_penalty
    

    def iterate(self):
        """
        Completes one iteration of a leapfrog optimization initialized 
        in the class constructor.
        """
        self.pointset[self.worsti] = self.leapfrog(self.besti, self.worsti)
        self.besti, self.worsti = self.get_best_worst()
        self.error = self.calculate_convergence()
        self.total_iters += 1
        
    
    
    def minimize(self):
        """
        Minimizes a function until the convergence criteria are 
        satisfied or the number of iterations exceeds 
        'self.maxit'.
        """
        success, status, message = False, 1, "Maximum Iterations Exceeded"
        for iters in range(self.maxit):
            self.iterate()
            
            if self.error < self.tol:
                success, status = True, 0, 
                message  = "Tolerance condition satisfied"
                break

            if self.callback is not None:
                self.callback(self.pointset[self.besti][1:])
        
        return OptimizeResult(
            x           = self.pointset[self.besti][1:],
            success     = success,
            status      = status,
            message     = message,
            fun         = self.pointset[self.besti][0],
            nfev        = self.nfev,
            nit         = self.total_iters,
            maxcv       = self.maxcv,
            best        = self.pointset[self.besti],
            worst       = self.pointset[self.worsti],
            final_error = self.error,
            pointset    = self.pointset
        )


    
def _main():
    """
    Run a simple test on the optimizer.
    """
    # optimize a simple, 2-parameter quadratic
    test = lambda x: x[0]**2.0 + x[1]**2.0 + 3.0
    
    int2 = [
        [-10.0,10.0],
        [-10.0,10.0]]
    
    options = {
        "fun"         : test, 
        "bounds"      : int2,
        "args"        : (),
        "points"      : 3,
        "fconstraint" : None,
        "discrete"    : [],
        "maxit"       : 5000,
        "tol"         : 1e-3,
        "seedval"     : 1235
        }
    
    # Unconstrained optimization ----------------------------------------------
    lf = LeapFrog(**options)
    print("\nUNCONSTRAINED:\nBEFORE:")
    print(lf)
    x = lf.minimize()
    print("AFTER:")
    print(lf)
    

    # Constrained optimization ------------------------------------------------
    g1 = lambda x: x[0] + 3
    
    options["fconstraint"] = g1
    options["points"]      = 20
    
    
    lf = LeapFrog(**options)
    
    print("\n\nCONSTRAINED:\nBEFORE:")
    print(lf)        
    x = lf.minimize() 
    print("AFTER:")
    print(lf)
    
    print("\nPoint Set:")
    for i in x['pointset']:
        print(i)
        
    # Constrained and discrete optimization -----------------------------------
    options["discrete"]    = [0,1]
    
    lf = LeapFrog(**options)
    
    print("\n\nCONSTRAINED AND DISCRETE:\nBEFORE:")
    print(lf)        
    x = lf.minimize() 
    print("AFTER:")
    print(lf)
    
    print("\nPoint Set:")
    for i in x['pointset']:
        print(i)
    print()

    
if __name__ == "__main__":
    _main()
