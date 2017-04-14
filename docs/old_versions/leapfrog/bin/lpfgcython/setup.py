from setuptools import setup
from Cython.Build import cythonize

setup(
    name = 'Leapfrog',
    ext_modules = cythonize("lpfg_0_5_2.pyx"),
    )