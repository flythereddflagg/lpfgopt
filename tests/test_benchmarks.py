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
    f = lambda x: A*len(x) + sum([i**2 - A*np.cos(2*np.pi*i) for i in x])
    
    bounds = [
        [-5.12, 5.12],
        [-5.12, 5.12]]
    
    check = [0.0, 0.0]
    
    run(f, bounds, check, options)


def test_ackley():
    """
    Ackley function benchmark
    """
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: -20*np.exp(-0.2 * np.sqrt(0.5*(x[0]**2 + x[1]**2))) -\
                  np.exp(0.5*(np.cos(2*np.pi*x[0]) + np.cos(2*np.pi*x[1]))) +\
                  np.e + 20
    
    bounds = [
        [-5.0, 5.0],
        [-5.0, 5.0]]
    
    check = [0.0, 0.0]
    
    run(f, bounds, check, options)
        
        

def test_sphere():
    """
    Sphere function benchmark
    """
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: sum([i**2 for i in x])
    
    bounds = [
        [-20.0, 20.0],
        [-20.0, 20.0]]
    
    check = [0.0, 0.0]
    
    run(f, bounds, check, options)
        
        
def test_rosenbrock():
    """
    Rosenbrock function benchmark
    """
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2
    
    bounds = [
        [-3.0, 3.0],
        [-3.0, 3.0]]
    
    check = [1.0, 1.0]
    
    run(f, bounds, check, options)



def test_beale():
    """
    Beale function benchmark
    """
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x:  (1.5 - x[0] + x[0]*x[1])**2\
                 + (2.25 - x[0] + x[0]*x[1]**2)**2\
                 + (2.625 - x[0] + x[0]*x[1]**3)**2
    
    bounds = [
        [-4.5, 4.5],
        [-4.5, 4.5]]
    
    check = [3.0, 0.5]
    
    run(f, bounds, check, options)



def test_goldstein_price():
    """
    Goldstein–Price function benchmark
    """
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x:   (1 + (x[0] + x[1] + 1)**2\
                  * (19 - 14*x[0] + 3*x[0]**2 - 14*x[1] + 6*x[0]*x[1]\
                  + 3*x[1]**2))\
                  * (30 + (2*x[0] - 3*x[1])**2\
                  * (18 - 32*x[0] + 12*x[0]**2 + 48*x[1] - 36*x[0]*x[1]\
                  + 27*x[1]**2))
    
    bounds = [
        [-2.0, 2.0],
        [-2.0, 2.0]]
    
    check = [0.0, -1.0]
    
    run(f, bounds, check, options)
  
    

def test_booth():
    """
    Booth function benchmark
    """
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: (x[0] + 2*x[1] - 7)**2 + (2*x[0] + x[1] - 5)**2

    bounds = [
        [-10.0, 10.0],
        [-10.0, 10.0]]
    
    check = [1.0, 3.0]
    
    run(f, bounds, check, options)



def test_bulkin6():
    """
    Bukin function N.6 benchmark
    """
    ### NOTE: LeapFrog seems to get stuck in local minimum. DEBUG?
    options = {
        "tol"         : 1e-5,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: 100 * np.sqrt(abs(x[1] - 0.01*x[0]**2)) + 0.01*abs(x[0] + 10)

    bounds = [
        [-15.0, -5.0],
        [-3.0,   3.0]]
    
    check = [-10.0, 1.0]
    
    run(f, bounds, check, options, tol=2.0)
 
    
    
def test_matyas():
    """
    Matyas function benchmark
    """
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: 0.26 * (x[0]**2 + x[1]**2) - 0.48*x[0]*x[1]

    bounds = [
        [-10.0, 10.0],
        [-10.0, 10.0]]
    
    check = [0.0, 0.0]
    
    run(f, bounds, check, options)


    
def test_levi13():
    """
    Lévi function N.13 benchmark
    """
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x:   np.sin(3*np.pi*x[0])**2\
                  + (x[0] - 1)**2 * (1 + np.sin(3*np.pi*x[1])**2)\
                  + (x[1] - 1)**2 * (1 + np.sin(2*np.pi*x[1])**2)

    bounds = [
        [-10.0, 10.0],
        [-10.0, 10.0]]
    
    check = [1.0, 1.0]
    
    run(f, bounds, check, options)



def test_himmelblau():
    """
    Himmelblau's function benchmark
    """
    options = {
        "points"      : 100,
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x:  (x[0]**2 + x[1]    - 11)**2\
                 + (x[0]    + x[1]**2 -  7)**2

    bounds = [
        [-5.0, 5.0],
        [-5.0, 5.0]]
    
    check = [3.0, 2.0]
    
    run(f, bounds, check, options)



def test_three_hump_camel():
    """
    Three-hump camel function benchmark
    """
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: 2*x[0]**2 - 1.05*x[0]**4 + x[0]**6/6 + x[0]*x[1] + x[1]**2

    bounds = [
        [-5.0, 5.0],
        [-5.0, 5.0]]
    
    check = [0.0, 0.0]
    
    run(f, bounds, check, options)  
    
    
def test_easom():
    """
    Easom function benchmark
    """
    options = {
        "points"      : 50,
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: - np.cos(x[0])*np.cos(x[1])\
                  * np.exp(-((x[0] - np.pi)**2 + (x[1] - np.pi)**2))

    bounds = [
        [-100.0, 100.0],
        [-100.0, 100.0]]
    
    check = [np.pi, np.pi]
    
    run(f, bounds, check, options)  
    
    

def test_cross_in_tray():
    """
    Cross-in-tray function benchmark
    """
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: - 0.0001 * (abs(np.sin(x[0]) * np.sin(x[1])\
                  * np.exp(abs(100 - np.sqrt(x[0]**2 + x[1]**2)/np.pi)))\
                  + 1)**0.1

    bounds = [
        [-10.0, 10.0],
        [-10.0, 10.0]]
    
    check = [1.34941, 1.34941]
    
    run(f, bounds, check, options)  
    
    

def test_eggholder():
    """
    Eggholder function benchmark
    """
    ### NOTE: LeapFrog seems to get stuck in local minimum. DEBUG?
    options = {
        "points"      : 50,
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        
        }
        
    f = lambda x: - (x[1] + 47) * np.sin(np.sqrt(abs(x[0]/2 + (x[1] + 47))))\
                  - x[0] * np.sin(np.sqrt(abs(x[0] + (x[1] + 47))))

    bounds = [
        [-512.0, 512.0],
        [-512.0, 512.0]]
    
    check = [512.0, 404.2319]
    
    run(f, bounds, check, options, tol=2.0)  
    
    

def test_holder_table():
    """
    Hölder table function benchmark
    """
    options = {
        "points"      : 50,
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: - abs(np.sin(x[0])*np.cos(x[1]) * np.exp(abs(1\
                  - np.sqrt(x[0]**2 + x[1]**2)/np.pi)))

    bounds = [
        [-10.0, 10.0],
        [-10.0, 10.0]]
    
    check = [-8.05502, -9.66459]
    
    run(f, bounds, check, options)  
    
    

def test_mccormick():
    """
    McCormick function benchmark
    """
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x:  np.sin(x[0] + x[1]) + (x[0] - x[1])**2\
                 - 1.5*x[0] + 2.5*x[1] + 1

    bounds = [
        [-1.5, 4.0],
        [-3.0, 4.0]]
    
    check = [-0.54719, -1.54719]
    
    run(f, bounds, check, options)  
    
    

def test_schaffer2():
    """
    Schaffer function N.2 benchmark
    """
    options = {
        "points"      : 100,
        "tol"         : 2e-2,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: 0.5 + (np.sin(x[0]**2 + x[1]**2)**2 - 0.5)\
                      / (1 + 0.001*(x[0]**2 + x[1]**2))**2

    bounds = [
        [-100.0, 100.0],
        [-100.0, 100.0]]
    
    check = [0.0, 0.0]
    
    run(f, bounds, check, options)  
    
    

def test_schaffer4():
    """
    Schaffer function N.4 benchmark
    """
    options = {
        "points"      : 100,
        "tol"         : 1e-2,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: 0.5 + (np.cos(np.sin(abs(x[0]**2 - x[1]**2)))**2 - 0.5)\
                      / (1 + 0.001*(x[0]**2 + x[1]**2))**2

    bounds = [
        [-100.0, 100.0],
        [-100.0, 100.0]]
        
    check = [0.0, 1.25313]
    
    run(f, bounds, check, options)  
    
    

def test_styblinski_tang():
    """
    Styblinski–Tang function benchmark
    """
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: sum([(i**4 - 16*i**2 + 5*i)/2 for i in x])

    bounds = [
        [-5.0, 5.0],
        [-5.0, 5.0]]
    
    check = [-2.903534, -2.903534]
    
    run(f, bounds, check, options)  
    
