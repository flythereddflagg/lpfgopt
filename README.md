# Leap Frog Optimizer Package

<b> 
Author  : Mark Redd  <br/>
Email   : redddogjr@gmail.com <br/>
GitHub  : https://github.com/flythereddflagg <br/>
Website : http://www.r3eda.com/ </b>

### About:

This package is based the 
<em><a href="http://www.r3eda.com/leapfrogging-optimization-algorithm/">Leapfrogging Optimization 
Algorithm</a></em>
published by 
<a href="http://www.r3eda.com/about-russ/">Dr. R. Russell Rhinehart</a>.

The following publications explain the technique and may be found on the website:

  - Rhinehart, R. R., M. Su, and U. Manimegalai-Sridhar,
    “Leapfrogging and Synoptic Leapfrogging: a new optimization approach”,
    Computers & Chemical Engineering, Vol. 40, 11 May 2012, pp. 67-81.

  - Manimegalai-Sridhar, U., A. Govindarajan, and R. R. Rhinehart,
    “Improved Initialization of Players in Leapfrogging Optimization”,
    Computers & Chemical Engineering, Vol. 60, 2014, 426-429.

  - Rhinehart, R. R.,
    “Convergence Criterion in Optimilsation of Stochastic Processes”,
    Computers & Chemical Engineering, Vol. 68, 4 Sept 2014, pp 1-6.

This code is intended for use in Python and C/C++ and has implimentaions in those languages. The Python
implimentation is compiled with Cython and linked with a shared C library to maximize speed of optimization.

## Installation
There are a variety of ways to install the software both for use in Python or 
C/C++ on Windows and Linux. Support for Macintosh will be implimented in future versions. All source 
code has been tested with GCC and Python 2.7. Other compilers and Python 3 will have support in future
versions.

### Python Installation:

#### Via pip

Lpfgopt may be installed and tested on Linux or Windows x86_64 systems with pip using the following commands:
```bash
$ pip install lpfgopt
$ python
```
```python
>>> from lpfgopt import __version__, unit_test
>>> __version__
'X.X.X'
>>> unit_test.main()
 [  3.00000  0.00000  0.00000 ]
>>>
```
If the `unit_test.main()` command produces the above output congratulations! You have successfully installed the package!


<b>System requirements for installation from source using these instructions:</b>
 - Python 2.7

#### Via setup.py
Open the main directory where "setup.py" is located and run the following command"
```bash
$ cd ..
$ python setup.py install     # You may need root priviliges or use the --user tag
```
3. The software should be installed correctly. You may validate the installation by executing the following commands:
```bash
$ python
```
```python
>>> from lpfgopt import __version__, unit_test
>>> __version__
'X.X.X'
>>> unit_test.main()
 [  3.00000  0.00000  0.00000 ]
>>>
```
If the version number appears below, congratulations! You have sucessfully installed the Leap Frog Optimizer package!
## Usage
[Nothing here yet]

## Removal
[Nothing here yet]
