#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from lpfgopt.leapfrog import LeapFrog

# get version of lpfgopt
import os
mypackage_root_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(mypackage_root_dir, 'VERSION.txt')) as version_file:
    __version__ = version_file.read().strip()
del os


def minimize(fun, bounds, args=(), points=20, fconstraint=None, discrete=[],
             maxit=10000, tol=1e-5, seedval=None, pointset=None, callback=None):
    """
    Basic wrapper function to interface with the LeapFrog optimizer class.
    Best for general use.
    """
    options = {
        "fun"         : fun, 
        "bounds"      : bounds,
        "args"        : args,
        "points"      : points,
        "fconstraint" : fconstraint,
        "discrete"    : discrete,
        "maxit"       : maxit,
        "tol"         : tol,
        "seedval"     : seedval,
        "pointset"    : pointset,
        "callback"    : callback
        }
        
    lf = LeapFrog(**options)
    return lf.minimize()
