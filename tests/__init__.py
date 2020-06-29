import numpy as np
from lpfgopt import minimize, c_minimize


def run(
        f, bounds, check, options={}, tol=1e-3, 
        output_ptset=False, min_=minimize
    ):
    '''
    Runs a benchmark test with the given parameters and causes a
    failing result for nosetests on a failure.
    '''
    sol = min_(f, bounds, **options)

    r = "Correct opt"
    print(f"{r:12} : {check}\n")

    for key, value in sol.items():
        if key == "pointset": continue
        print(f"{key:12} : {value}")

    if output_ptset:
        for i in sol['pointset']:
            if 'fconstraint' in options.keys():
                print(i, options['fconstraint'](i[1:]))
            else:
                print(i)

    assert sol['success'], "Optimization Failed"

    for i in range(len(check)):
        if abs(check[i]) < tol:
            norm = 1.0
        else:
            norm = check[i]
        err = abs((check[i] - sol['x'][i])/norm)
        assert err <= tol, f"{min_} Fail: on: {i} err: {err}"
