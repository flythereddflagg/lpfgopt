from setuptools import setup
from Cython.Build import cythonize

setup(
    name = 'copt',
    ext_modules = cythonize("./cython/copt.pyx"),
    )
