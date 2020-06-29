"""
filename       : discrete_benchmark_tests.py
title          : Discrete Benchmark Tests For the LeapFrog Optimizer
author         : Mark Redd
email          : redddogjr@gmail.com

about:
    Contains discrete optimization benchmark tests for the 
    LeapFrog Optimizer. Designed to be used with the 'nose' module. Tests are 
    tuned individually to find a single optimum and are taken from the 
    following wikipedia article:

        https://en.wikipedia.org/wiki/Test_functions_for_optimization
    
    The results of each test may be run individually by importing this module
    running the desired test.
    
    Performance is measured by the optimizer successfully finding the optimum 
    x vector of each test function to within 0.1% of the real optimum or better.
    In cases where the optimum x vector would be 0.0 the optimizer must find 
    a value where:
    
        x_i <= 0.001
    
"""

import numpy as np
from . import *


def test_rosenbrock_discrete_test():
    """
    Rosenbrock function constrained to a disk benchmark
    """
    # adjust limits to improve optimization for large domains
    g = lambda x: x[0]**2 + x[1]**2 - 2
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        "fconstraint" : g,
        "discrete"    : [0,1]
        }
        
    f = lambda x: (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2
    
    bounds = [
        [-11.0, 11.0],
        [-11.0, 11.0]]
        
    check = [1.0, 1.0]
    
    run(f, bounds, check, options)
    
    
    
def test_sphere_constr_test():
    """
    Constrained sphere function benchmark
    """
    g = lambda x: -x[0]**2 + 10 - x[1] 
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        "fconstraint" : g,
        "discrete"    : [0]
        }
      
    f = lambda x: sum([i**2 for i in x])
    
    bounds = [
        [-20.0, 20.0],
        [-20.0, 20.0]]
    
    check = [-3, 1.0]
    
    run(f, bounds, check, options)
