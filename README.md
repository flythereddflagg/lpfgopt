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
**System requirements for installation from source using these instructions:**
 - Python 2.7
 - Numpy
 - Nose

### Python Installation:

#### Via pip

Lpfgopt may be installed and tested with pip using the following commands:
```bash
$ pip install lpfgopt-lite # You may need root privileges or the --user tag
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

#### Via setup.py
Download and unzip the archive or clone it with git.

Open the main directory where "setup.py" is located and run the following command:
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
If the `unit_test.main()` command produces the above output congratulations! You have successfully installed the package!
## Usage
The minimize function is the focus of the package. More tools will be added as the package evolves. The documentation for 
the function is given below with an example usage.

#### `minimize(f, intervals, args=(), full_output=False, points=20, constraints=None, tol=1e-5, rel=True, maxit=10000)`
Minimize `f` on the array of intervals for each decision variable.

* *Parameters:*  
  - `f`           - The objective function to be minimized. Will be called as `f(x)` where `x` is an array-like object of decision variables based on the length of `intervals`.
  - `intervals`   - Array-like object with `shape = (num_DV, 2)` (e.g. a list of lists with the sub-lists all having a length of 2)
                  the sub-arrays' first and second elements should hold the lower and upper limits of each decision variable respecively.
  - `args`        - Other arguments to pass into objective function (NOT YET FUNCTIONAL MAY STILL HAVE BUGS)
  - `full_output` - When set to `True` the function returns a dictionary of the
                  pertinent data from the optimization including:

    * `'best'`       : best point in the point set
    * `'worst'`      : worst point in the point set
    * `'final_error'`: final overall error
    * `'iterations'` : iterations to convergence or maxit if convergence was not reached
    * `'point_set'`  : the final state of the point set

  - `points`      - Number of points to be used in the optimization. Default is 20 points.
  - `constraints` - NOT YET FUNCTIONAL
  - `tol`         - Convergence tolerance or maximum error to converge (will be based on relative or absolute error 
                  based on the state of the `rel` parameter)
  - `rel`         - When set to `True`, error/convergence is calculated on a relative basis. When set to `False` 
                  error/convergence is calculated on absolute basis.
  - `maxit`       - Maximum iterations before returning. If maxit is reached, the system returns a runtime warning.

* *Returns:*  
  - `b`           - An array of floats that have the value of the optimized objective function followed by the optimized 
  values of each descision variable (i.e. `[ f(x), x[0], x[1], x[2], ..., x[n-1] ]`)
  - `bdict`       - Returned instead of `b` when `full_output` is set to True. A dictionary of the 
  pertinent data from the optimization including:
    * `'best'`       : best point in the point set
    * `'worst'`      : worst point in the point set
    * `'final_error'`: final overall error
    * `'iterations'` : iterations to convergence or maxit if convergence was not reached
    * `'point_set'`  : the final state of the point set 
#### Example Usage
The following is a simple optimization where the minimum value of the following equation is found:  
 - f(x) = 2x^2 + y^2 + 3
```python
# test_lpfgopt.py
from lpfgopt.opt import minimize

def f_test(x_arr):
  '''
  Returns the value of f(x, y) = 2x^2 + y^2 + 3
  where x and y are expressed as an array x_arr = [x, y]. 
  '''
  return 2.0 * x_arr[0]**2 + x_arr[1]**2 + 3.0

intervals = [
    [-10.0, 10.0], # the lower and upper limits of x respectively
    [-10.0, 10.0]] # the lower and upper limits of y respectively
    
solution = minimize(f_test, intervals)
print 'Best Solution', solution

solution = minimize(f_test, intervals, full_output=True)
print 'Best', solution['best']
print 'Worst', solution['worst']
print 'Final Error', solution['final_error']
print 'Number of iterations', solution['iterations']
print 'Final Point set\n', solution['point_set']
```
This code will produce the following output:
```bash
-bash-4.2$ python test_lpfgopt.py
Best Solution [  3.00000000e+00   2.56993473e-07  -2.09491337e-07]
Best [  3.00000000e+00  -6.28972674e-09  -2.28753688e-08]
Worst [  3.00000000e+00  -1.38087155e-07  -2.10084055e-06]
Final Error 9.96442673929e-06
Number of iterations 379
Final Point set
[[  3.00000000e+00   1.07083751e-07  -2.18870273e-07]
 [  3.00000000e+00   8.32314986e-07  -9.15522240e-07]
 [  3.00000000e+00   7.68957441e-07  -1.04105345e-06]
 [  3.00000000e+00  -4.72479226e-08   1.46408912e-06]
 [  3.00000000e+00   2.94841878e-07   3.94383641e-07]
 [  3.00000000e+00  -6.83697356e-07   1.06155755e-06]
 [  3.00000000e+00  -1.12944536e-06  -7.25128708e-08]
 [  3.00000000e+00  -4.49149018e-07  -7.33239651e-07]
 [  3.00000000e+00  -1.38087155e-07  -2.10084055e-06]
 [  3.00000000e+00   9.89936169e-08   2.13795158e-06]
 [  3.00000000e+00   2.98571550e-08  -9.54511199e-07]
 [  3.00000000e+00   8.59864265e-08  -9.29392680e-07]
 [  3.00000000e+00  -1.52397020e-06  -4.13280929e-08]
 [  3.00000000e+00   8.48590492e-07  -1.65243606e-06]
 [  3.00000000e+00  -1.43216345e-06  -1.41436678e-07]
 [  3.00000000e+00  -9.22183727e-07   1.49457448e-06]
 [  3.00000000e+00  -5.44663193e-07   2.58861735e-07]
 [  3.00000000e+00  -6.44378664e-07  -1.57923094e-06]
 [  3.00000000e+00   1.89972734e-07  -2.09631575e-06]
 [  3.00000000e+00  -6.28972674e-09  -2.28753688e-08]]
```
## Removal
[Nothing here yet]
