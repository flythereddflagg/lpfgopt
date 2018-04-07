#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script will do a unit test on all modules before distribution.
"""

from opt  import minimize

def _f_test(x): return 2.0 * x[0]**2 + x[1]**2 + 3.0

_intvls = [
    [-10.0, 10.0],
    [-10.0, 10.0]]
    
def main():
    sol = minimize(_f_test, _intvls)
    print "\n [",
    for i in sol:
        print " %.5f" % i,
    print "]"

if __name__ == "__main__":
    main()
