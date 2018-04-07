# Leap Frog Optimizer Package - Lite Edition

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

This is the stripped down version of the package with minimal tools. It is written in pure Python to allow compatiblitiy
for the alpha versions until the full version can be released.

## Installation 

You can install the lite versions via pip or using the setup.py in the down load. Instructions are shown below.

### Python Installation:

#### Via pip

Lpfgopt may be installed and tested with pip using the following commands:
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
$ python setup.py install     # You may need root priviliges or use the --user tag
```
The software should be installed correctly. You may validate the installation by executing the following commands:
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
