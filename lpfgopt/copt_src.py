#!/usr/bin/python
# -*- coding: utf-8 -*-

# for windows and linux
from ctypes import *
from os import name as osname

libname = "./liblpfgopt.so" if osname == "posix" else "./lpfgopt.dll"

class array_2d(Structure):
    pass

array_2d._fields_ = [
    ("rows", c_int),
    ("columns", c_int),
    ("array", POINTER(POINTER(c_double)))
    ]

def minimize(f,ivls):
    
    mydll = cdll.LoadLibrary(libname)

    ivl         = array_2d()
    ivl.rows    = 2
    ivl.columns = 2

    ptr_row = (POINTER(c_double) * ivl.rows)()

    for i in range(ivl.rows):
        row1 = (c_double * ivl.columns)()
        for j in range(ivl.columns):
            row1[j] = ivls[i][j]
        cast(row1, POINTER(c_double))
        ptr_row[i] = row1

    ivl.array = ptr_row
    ivlp = pointer(ivl)


    FUNC = CFUNCTYPE(c_double, POINTER(c_double))

    @FUNC
    def f1(x): return f(x)

    mydll.set.argtypes = [FUNC]
    mydll.set.restypes = None
    mydll.set(f1)

    pfunc = FUNC.in_dll(mydll, 'pfunc')

    sol_address = mydll.minimize(pfunc, ivlp, 20, len(ivls))
    sol_c_array = cast(sol_address, POINTER(c_double * 3))
    
    solution = [0 for i in range(3)]
    
    for i in range(3):
        solution[i] = sol_c_array.contents[i]
    
    return solution

def _f_test(x): return 2.0 * x[0]**2 + x[1]**2 + 3.0

_intvls = [
    [-10.0, 10.0],
    [-10.0, 10.0]]
    
def main():
    sol = minimize(_f_test, _intvls)
    print "\n [",
    for i in sol:
        print " %.9f" % i,
    print "]\n"

if __name__ == "__main__":
    main()
