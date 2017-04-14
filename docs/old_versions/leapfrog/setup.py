#!/usr/bin/python
# -*- coding: utf-8 -*-

# For information about this, see this tutorial:
# https://python-packaging.readthedocs.org/en/latest/minimal.html

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My Project',
    'author': 'Mark Redd',
    'url': 'r3eda.com',
    'download_url': 'https://sourceforge.net/projects/leapfrog-optimizer/',
    'author_email': 'redddogjr@gmail.com',
    'version': '0.5',
    'install_requires': ['nose', 'numpy', 'ctypes', 'warnings'],
    'packages': ['LeapFrog'],
    'scripts': [],
    'name': 'projectname'
    }

setup(**config)
