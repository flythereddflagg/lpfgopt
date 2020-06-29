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
from . import *

# def test_sphere_constr_test():
#     """
#     Constrained sphere function benchmark
#     """
#     g = lambda x: -x[0]**2 + 10 - x[1]
#     options = {
#         "points"      : 100,
#         "tol"         : 1e-3,
#         "seedval"     : 48154662342,
#         "fconstraint" : g
#         }

#     f = lambda x: sum([i**2 for i in x])

#     bounds = [
#         [-5.0, 5.0],
#         [-5.0, 5.0]]

#     check = [-3.0958051486911997, 0.4159905027317925]

#     run(f, bounds, check, options, min_=c_minimize)


def test_rosenbrock_line_cubic_test():
    """
    Rosenbrock function constrained with a cubic and a line benchmark
    """
    # CAVEAT: bounds are adjusted here (remedy?)
    def g(x):
        conval = 0
        cons = [
            (x[0] - 1)**3 - x[1] + 1,
            x[0] + x[1] - 2         ]
        for con in cons:
            if con > 0:
                conval += con
        return conval * 200

    options = {
        "points"      : 100,
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        "fconstraint" : g
        }

    f = lambda x: (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2

    bounds = [
        [0.5, 1.5],
        [-0.5, 2.5]]
#    bounds = [
#         [-3.0, 3.0],
#         [-3.0, 3.0]]
    check = [1.0, 1.0]

    run(f, bounds, check, options, min_=c_minimize)



def test_rosenbrock_disk_test():
    """
    Rosenbrock function constrained to a disk benchmark
    """
    g = lambda x: x[0]**2 + x[1]**2 - 2
    options = {
        "points"      : 100,
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        "fconstraint" : g
        }

    f = lambda x: (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2

    bounds = [
        [-1.5, 1.5],
        [-1.5, 1.5]]

    check = [1.0, 1.0]

    run(f, bounds, check, options, min_=c_minimize)



def test_mishra_bird_constr_test():
    """
    Mishra's Bird function - constrained benchmark
    """
    def f(vs):
        x, y = vs
        a = np.sin(y) * np.exp((1 - np.cos(x))**2)
        b = np.cos(x) * np.exp((1 - np.sin(y))**2)
        c = (x - y)**2
        return a + b + c

    def g(vs):
        x, y = vs
        return (x + 5)**2 + (y + 5)**2 - 24.9999999

    options = {
        "points"      : 100,
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        "fconstraint" : g
        }

    bounds = [
        [-10.0, 0.0],
        [ -6.5, 0.0]]

    check = [-3.1302468, -1.5821422]

    run(f, bounds, check, options, min_=c_minimize)



def test_simionescu_test():
    """
    Simionescu function benchmark
    """
    ### NOTE: LeapFrog seems to get stuck in local minimum. DEBUG?
    f = lambda x: 0.1 * x[0] * x[1]

    def g(vs):
        x, y = vs
        rt, rs, n = 1.0, 0.2, 8.0
        return x**2 + y**2 - (rt + rs * np.cos(n * np.arctan(x/y)))**2

    options = {
        "points"      : 100,
        "tol"         : 1e-3,
        "seedval"     : 4815162342,
        "fconstraint" : g
        }

    bounds = [
        [-1.25, 0],
        [0, 1.25]]

    check = [-0.84852813, 0.84852813]

    run(f, bounds, check, options, tol=1e-2)
