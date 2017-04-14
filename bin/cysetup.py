from setuptools import setup
from Cython.Build import cythonize

setup(
    name = 'cylpfgopt',
    ext_modules = cythonize("cylpfgopt.pyx"),
    )
