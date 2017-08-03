#!/usr/bin/python
# -*- coding: utf-8 -*-

# For information about this, see this tutorial:
# https://python-packaging.readthedocs.org/en/latest/minimal.html

try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup

from os import name as osname
import lpfgopt


if osname == "posix":
    file_include = {
        'lpfgopt': [
            'lpfgopt/copt.so',
            'lpfgopt/cyopt.so',
            'lpfgopt/liblpfgopt.so'
            'lpfgopt/lpfgopt_test.exe'
            ]
        }

elif osname == "nt":
    file_include = {
        'lpfgopt': [
            'lpfgopt/lpfgopt.dll',
            'lpfgopt/copt.pyd',
            'lpfgopt/cyopt.pyd',
            'lpfgopt/lpfgopt_test.exe'
            ]
        }

else:
    raise OSError("This operating system is not supported under the current "\
        "version of lpfgopt.")


def readme():
    with open('README.md') as f:
        return f.read()

config = {
    'name'                : 'lpfgopt',
    'description'         : 'Leap Frog Optimizer',
    'version'             : lpfgopt.__version__,
    'author'              : 'Mark E. Redd',
    'author_email'        : 'redddogjr@gmail.com',
    'url'                 : 'http://www.r3eda.com/',
    'download_url'        : 'https://github.com/flythereddflagg/lpfgopt',
    'install_requires'    : ['nose', 'numpy'],
    'packages'            : ['lpfgopt', 'tests'],
    'scripts'             : [],
    'package_data'        : file_include,
    'long_description'    : readme(),
    'include_package_data': True
    }

setup(**config)
