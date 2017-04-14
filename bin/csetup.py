from setuptools import setup
from Cython.Build import cythonize

setup(
    name = 'clpfgopt',
    ext_modules = cythonize("clpfgopt.pyx"),
    )
