#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script will do a unit test on all modules before distribution.
"""

import numpy as np
from opt import minimize
from opt_benchmark import minimize as min_bnch

def _f_test(x): return 2.0 * x[0]**2 + x[1]**2 + 3.0

_intvls = [
    [-10.0, 10.0],
    [-10.0, 10.0]]

st = np.array([
    [
    -3.2697166231384163,
    -0.30106530328420966,
    -7.378448241157214,
    -0.19133039000762153,
    -7.217230801276617,
    -6.878029799128475,
    -4.5870772269281845,
    -9.755670223146646,
    4.901950694047175,
    -7.53210439905029,
    5.437226902143324,
    -7.739404401287377,
    0.5493843932578741,
    9.238553781141974,
    -1.2959633175173106,
    7.726940907585597,
    -4.322107922945564,
    -7.112370271528952,
    1.9372210724194634,
    7.092041300360016],
    [
    -7.9308713940187054,
    2.33112855695415,
    6.110016234356376,
    7.015878041115521,
    -8.815178089521446,
    4.09235333218373,
    9.063025349530239,
    -8.901648760731792,
    -3.1846529197432965,
    1.6987271250465952,
    0.5777975810329501,
    9.82975029607995,
    5.666248382585389,
    -7.51375223005337,
    -4.268123633459329,
    1.4205298992133244,
    6.001377038848506,
    9.409347426473332,
    7.505653601073554,
    -9.886019041975583]]).T
 
def main():
    solution_test = minimize(_f_test, _intvls)
    print('\nopt best:', solution_test, '\n')
    
    solution_test = min_bnch(_f_test, _intvls)
    print(
        '\nopf best:', 
        solution_test.best, 
        '\nNumber of calls:', 
        solution_test.f_evals,
        "\n")
    
    solution_test = min_bnch(_f_test, _intvls, start_pts=st,seed=234)
    print(
        '\nopf best:', 
        solution_test.best, 
        '\nNumber of calls:', 
        solution_test.f_evals,
        "\n")
    

if __name__ == "__main__":
    main()
