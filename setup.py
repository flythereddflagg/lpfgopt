#!/usr/bin/python
# -*- coding: utf-8 -*-

# For information about this, see this tutorial:
# https://python-packaging.readthedocs.org/en/latest/minimal.html

try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup

import lpfgopt


def readme():
    with open('README.md', encoding='utf8') as f:
        return f.read()

config = {
    'name'                : 'lpfgopt-lite',
    'description'         : 'Leap Frog Optimizer - Lite Edition',
    'version'             : lpfgopt.__version__,
    'author'              : 'Mark E. Redd',
    'author_email'        : 'redddogjr@gmail.com',
    'url'                 : 'http://www.r3eda.com/',
    'download_url'        : 'https://github.com/flythereddflagg/lpfgopt',
    'install_requires'    : ['nose', 'numpy'],
    'packages'            : ['lpfgopt'],
    'scripts'             : [],
    'long_description'    : readme(),
    'include_package_data': True,
    'license'             : 'MIT',
    'classifiers'         : ['Development Status :: 3 - Alpha'],
    }

setup(**config)
