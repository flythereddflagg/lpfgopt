from ctypes import *
import numpy as np


mydll = cdll.LoadLibrary("./lpfg.dll")



print "Setting up ctypes...",

class array_2d(Structure):
    pass

array_2d._fields_ = [
    ("rows", c_int),
    ("columns", c_int),
    ("array", POINTER(POINTER(c_double)))
    ]
intvls = [
    [-10.0, 10.0],
    [-10.0, 10.0]]

ivl         = array_2d()
ivl.rows    = 2
ivl.columns = 2

ptr_row = (POINTER(c_double) * ivl.rows)()

for i in range(ivl.rows):
    row1 = (c_double * ivl.columns)()
    for j in range(ivl.columns):
        row1[j] = intvls[i][j]
    cast(row1, POINTER(c_double))
    ptr_row[i] = row1

ivl.array = ptr_row

ivlp = pointer(ivl)
print "DONE."
#print ivlp.contents.array.contents[0] 

#ADDITIONS FROM : (Python extentions)
# http://stackoverflow.com/questions/15160077/assigning-python-function-to-ctypes-pointer-variable
print "Setting up function...",
FUNC = CFUNCTYPE(c_double, POINTER(c_double))

@FUNC
def f1(x): return 2.0 * x[0]**2 + x[1]**2 + 3.0

mydll.set.argtypes = [FUNC]
mydll.set.restypes = None
mydll.set(f1)

pfunc = FUNC.in_dll(mydll, 'pfunc')
print "DONE."
# END ADDITIONS

print "Running optimization... ",
out = mydll.minimize(pfunc,ivlp,20,2)
print "Getting output...\n"
sol = cast(out, POINTER(c_double * 3))
sol1 = np.zeros(3)
for i in range(3):
    sol1[i] = sol.contents[i]
print sol1