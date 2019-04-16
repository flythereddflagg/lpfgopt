import numpy as np
from lpfgopt import minimize


def run(f, bounds, check, options={}, output=False):
    sol = minimize(f, bounds, **options)
    
    for key, value in sol.items():
        if key == "pointset": continue
        print(f"{key:12} : {value}")

    for i in sol['pointset']:
        print(i)

    assert sol['success'], "Optimization Failed"
    
    for i in range(len(check)):
        assert check[i] == sol['x'][i], f"Failed on {i}"
    
    if output:
        raise Exception("Generic Exception")
    
    

def rastrigin_test():
    """
    Rastrigin function benchmark
    """
    options = {
        "points"      : 4,
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
    A = 10
    f = lambda x: 10*len(x) + sum([i**2 - A*np.cos(2*np.pi*i) for i in x])
    
    bounds = [
        [-5.12, 5.12],
        [-5.12, 5.12]]
    
    check = [0.0, 0.0]
    
    run(f, bounds, check, output=True)


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
        "points"      : 3,
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
        "points"      : 4,
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        }
    f = lambda x: (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2
    
    bounds = [
        [-3.0, 3.0],
        [-3.0, 3.0]]
    
    check = [1.0, 1.0]
    
    run(f, bounds, check, options)
        
        
