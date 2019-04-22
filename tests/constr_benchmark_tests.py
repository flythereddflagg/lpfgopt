"""
filename       : constr_benchmark_tests.py
title          : Constrained Benchmark Tests For the LeapFrog Optimizer
author         : Mark Redd
email          : redddogjr@gmail.com

about:
    Contains constrained optimization benchmark tests for the 
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
from lpfgopt import minimize


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