from setuptools import setup
from Cython.Build import cythonize

setup(
    name = 'cyopt',
    ext_modules = cythonize("./cython/cyopt.pyx"),
    )
