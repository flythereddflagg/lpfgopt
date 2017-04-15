#!/usr/bin/python
# -*- coding: utf-8 -*-

# For information about this, see this tutorial:
# https://python-packaging.readthedocs.org/en/latest/minimal.html

try:
    from setuptools import setup
except ImportError    :
    from distutils.core import setup

#from os import name as osname
#libname = "./liblpfgopt.so" if osname == "posix" else "./lpfgopt.dll"    

def readme()    :
    with open('README.rst') as f:
        return f.read()

file_include = [
    ('lpfgopt', 
        [
        'lpfgopt/lpfgopt.dll',
        'lpfgopt/copt.pyd',
        'lpfgopt/cyopt.pyd',
        'lpfgopt/lpfgopt_test.exe'
        ]
    )
    ]
        
config = {
    'name'                : 'lpfgopt',
    'description'         : 'Leap Frog Optimizer',
    'version'             : '0.6.2',
    'author'              : 'Mark Redd',
    'author_email'        : 'redddogjr@gmail.com',
    'url'                 : 'http://www.r3eda.com/',
    'download_url'        : 'https://sourceforge.net/projects/leapfrog-optimizer/',
    'install_requires'    : ['nose', 'numpy'],
    'packages'            : ['lpfgopt'],
    'scripts'             : [],
    'data_files'          : file_include,
    'long_description'    : readme(),
    'include_package_data': True
    }

setup(**config)
