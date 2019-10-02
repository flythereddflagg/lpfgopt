"""
filename       : benchmarks.py
title          : Unconstrained Benchmark Tests For the LeapFrog Optimizer
author         : Mark Redd
email          : redddogjr@gmail.com

about:
    Contains 20 unconstrained optimization benchmark tests for the 
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
    
    Currently the following functions are under-performing according to this
    definition:
        - Bukin function N.6
        - Eggholder function
"""

import numpy as np
from lpfgopt import c_minimize as minimize


def run(f, bounds, check, options={}, output=False, tol=1e-3):
    '''
    Runs a benchmark test with the given parameters and causes a
    failing result for nosetests on a failure.
    '''
    sol = minimize(f, bounds, **options)
    
    r = "Correct opt"
    print(f"{r:12} : {check}\n")
    
    for key, value in sol.items():
        if key == "pointset": continue
        print(f"{key:12} : {value}")

    for i in sol['pointset']:
        print(i)

    assert sol['success'], "Optimization Failed"
    
    for i in range(len(check)):
        if abs(check[i]) < tol:
            norm = 1.0
        else:
            norm = check[i]
        err = abs((check[i] - sol['x'][i])/norm)
        assert err <= tol, f"Failed on parameter index {i} with error {err}"
    
    if output:
        raise Exception("Generic Exception")
    
    

def test_rastrigin():
    """
    Rastrigin function benchmark
    """
    options = {
        "points"      : 50,
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    A = 10
    len1 = 2
    f = lambda x: A*len1 + x[0]**2 - A*np.cos(2*np.pi*x[0]) + \
                x[1]**2 - A*np.cos(2*np.pi*x[1])
    
    bounds = [
        [-5.12, 5.12],
        [-5.12, 5.12]]
    
    check = [0.0, 0.0]
    
    run(f, bounds, check, options)

