#!/usr/bin/python
# -*- coding: utf-8 -*-

# For information about this, see this tutorial:
# https://python-packaging.readthedocs.org/en/latest/minimal.html

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def readme():
    with open('README.rst') as f:
        return f.read()

config = {
    'name'            : 'lpfgopt',
    'description'     : 'Leap Frog Optimizer',
    'version'         : '0.6.2',
    'author'          : 'Mark Redd',
    'author_email'    : 'redddogjr@gmail.com',
    'url'             : 'http://www.r3eda.com/',
    'download_url'    : 'https://sourceforge.net/projects/leapfrog-optimizer/',
    'install_requires': ['nose', 'numpy', 'ctypes', 'warnings'],
    'packages'        : ['lpfgopt'],
    'scripts'         : [],
    'long_description': readme()
    }

setup(**config)
