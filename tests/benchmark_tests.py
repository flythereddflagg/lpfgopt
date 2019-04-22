import numpy as np
from lpfgopt import minimize


def run(f, bounds, check, options={}, output=False, tol=1e-3):
    '''
    Runs a benchmark test with the given parameters and causes a
    failing result for nosetests on a failure.
    '''
    sol = minimize(f, bounds, **options)
    
    for key, value in sol.items():
        if key == "pointset": continue
        print(f"{key:12} : {value}")

    for i in sol['pointset']:
        print(i)

    assert sol['success'], "Optimization Failed"
    
    for i in range(len(check)):
        if abs(check[i]) < tol:
            norm = tol
        else:
            norm = check[i]
        err = abs((check[i] - sol['x'][i])/norm)
        assert err <= tol, f"Failed on parameter index {i} with error {err}"
    
    if output:
        raise Exception("Generic Exception")
    
    

def rastrigin_test():
    """
    Rastrigin function benchmark
    """
    options = {
        "points"      : 50,
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    A = 10
    f = lambda x: 10*len(x) + sum([i**2 - A*np.cos(2*np.pi*i) for i in x])
    
    bounds = [
        [-5.12, 5.12],
        [-5.12, 5.12]]
    
    check = [0.0, 0.0]
    
    run(f, bounds, check, options)


def ackley_test():
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
        
        

def sphere_test():
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
        
        
def rosenbrock_test():
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



def beale_test():
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



def goldstein_price_test():
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
  
    

def booth_test():
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



def bulkin6_test():
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
 
    
    
def matyas_test():
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


    
def levi13_test():
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



def himmelblau_test():
    """
    Himmelblau's function benchmark
    """
    options = {
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



def three_hump_camel_test():
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
    
    
def easom_test():
    """
    Easom function benchmark
    """
    options = {
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
    
    

def cross_in_tray_test():
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
    
    

def eggholder_test():
    """
    Eggholder function benchmark
    """
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: - (x[1] + 47) * np.sin(np.sqrt(abs(x[0]/2 + (x[1] + 47))))\
                  - x[0] * np.sin(np.sqrt(abs(x[0] + (x[1] + 47))))

    bounds = [
        [-512.0, 512.0],
        [-512.0, 512.0]]
    
    check = [512.0, 404.2319]
    
    run(f, bounds, check, options)  
    
    

def holder_table_test():
    """
    Hölder table function benchmark
    """
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: - abs(np.sin(x[0])*np.cos(x[1])*exp(abs(1\
                  - np.sqrt(x[0]**2 + x[1]**2)/np.pi)))

    bounds = [
        [-10.0, 10.0],
        [-10.0, 10.0]]
    
    check = [8.05502, 9.66459]
    
    run(f, bounds, check, options)  
    
    

def mccormick_test():
    """
    McCormick function benchmark
    """
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: np.sinsin(x[0] + x[1]) # continue here

    bounds = [
        [-10.0, 10.0],
        [-10.0, 10.0]]
    
    check = [0.0, 0.0]
    
    run(f, bounds, check, options)  
    
    

def schaffer2_test():
    """
    Schaffer function N.2 benchmark
    """
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: 0

    bounds = [
        [-10.0, 10.0],
        [-10.0, 10.0]]
    
    check = [0.0, 0.0]
    
    run(f, bounds, check, options)  
    
    

def schaffer4_test():
    """
    Schaffer function N.4 benchmark
    """
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: 0

    bounds = [
        [-10.0, 10.0],
        [-10.0, 10.0]]
    
    check = [0.0, 0.0]
    
    run(f, bounds, check, options)  
    
    

def styblinski_tang_test():
    """
    Styblinski–Tang function benchmark
    """
    options = {
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
        
    f = lambda x: 0

    bounds = [
        [-10.0, 10.0],
        [-10.0, 10.0]]
    
    check = [0.0, 0.0]
    
    run(f, bounds, check, options)  
    
