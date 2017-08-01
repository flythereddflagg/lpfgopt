#!/usr/bin/python
# -*- coding: utf-8 -*-

# For information about this, see this tutorial:
# https://python-packaging.readthedocs.org/en/latest/minimal.html

from os import name as osname
import lpfgopt


if osname == "posix":
    file_include = {
        'lpfgopt': [
            'lpfgopt/copt.so',
            'lpfgopt/cyopt.so',
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


try:
    from setuptools import setup
    
    if osname == "posix":
        from setuptools.command.install import install
        from os import path
        import subprocess
        
        class PostInstallCommand(install):
            """Post-installation for installation mode."""
            def run(self):
                path1 = path.dirname(path.abspath( __file__ ))
                script_path = path1 + "/lpfgopt/so_install.sh"
                subprocess.call(script_path)
                install.run(self)

except ImportError:
    from distutils.core import setup
    
    if osname == "posix":
        class PostInstallCommand():
            def run(self):
                pass


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
    'download_url'        : 'https://sourceforge.net/projects/leapfrog-optimizer/',
    'install_requires'    : ['nose', 'numpy'],
    'packages'            : ['lpfgopt', 'tests'],
    'scripts'             : [],
    'package_data'        : file_include,
    'long_description'    : readme(),
    'cmdclass'            : {'install': PostInstallCommand},
    'include_package_data': True
    }

setup(**config)
