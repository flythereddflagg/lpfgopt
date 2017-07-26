#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script will do a unit test on all modules before distribution.
"""

from copt  import minimize
from cyopt import minimize as min1

def _f_test(x): return 2.0 * x[0]**2 + x[1]**2 + 3.0

_intvls = [
    [-10.0, 10.0],
    [-10.0, 10.0]]
    
def _main():
    sol = minimize(_f_test, _intvls)
    print "\n [",
    for i in sol:
        print " %.9f" % i,
    print "]\n"
    
    sol = min1(_f_test, _intvls)
    print "\n [",
    for i in sol:
        print " %.9f" % i,
    print "]\n"

if __name__ == "__main__":
    _main()
