from ctypes import *

mydll = cdll.LoadLibrary("./libadd.so")

print mydll.Add(6,23)
