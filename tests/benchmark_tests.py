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
