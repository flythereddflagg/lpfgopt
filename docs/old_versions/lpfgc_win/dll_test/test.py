from ctypes import *

mydll = windll.LoadLibrary("./add.dll")

print mydll.Add(6,23)