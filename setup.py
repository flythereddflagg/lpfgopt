
"""
Setup script for the lpfgopt package
"""
try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup

import lpfgopt


def readme():
    with open('README.md', encoding='utf8') as f:
        return f.read()

config = {
    'name'                 : 'lpfgopt-lite',
    'description'          : 'Leap Frog Optimizer - Lite Edition',
    'version'              : lpfgopt.__version__,
    'author'               : 'Mark E. Redd',
    'author_email'         : 'redddogjr@gmail.com',
    'url'                  : 'http://www.r3eda.com/',
    'download_url'         : 'https://github.com/flythereddflagg/lpfgopt',
    'python_requires'      : '>=3.6',
    'install_requires'     : ['nose', 'numpy', 'scipy'],
    'packages'             : ['lpfgopt'],
    'scripts'              : [],
    'long_description'     : readme(),
    'long_description_'\
        'content_type'     : 'text/markdown',
    'include_package_data' : True,
    'license'              : 'MIT',
    "keywords"             : 'optimization direct-search gradient-free',
    'classifiers'          : [
                                'Development Status :: 4 - Beta',
                                'Intended Audience :: Science/Research',
                                'Intended Audience :: Manufacturing',
                                'Intended Audience :: Education',
                                'Intended Audience :: End Users/Desktop',
                                'License :: OSI Approved :: MIT License',
                             ],
    }

setup(**config)
