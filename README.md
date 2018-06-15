# Leap Frog Optimizer Package - Lite Edition

<b> 
Author  : Mark Redd <br/>
Email   : redddogjr@gmail.com  <br/>
GitHub  : https://github.com/flythereddflagg <br/>
Website : http://www.r3eda.com/ <br/>

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
 - Python 2.7 or 3.6
 - Numpy
 - Nose

### Python Installation:

#### Via pip

Lpfgopt may be installed with pip using the following commands:
```bash
$ pip install lpfgopt-lite # You may need root privileges or the --user tag
```

#### Via setup.py
Download the 'lite' branch and unzip the archive or clone it with git.

Open the main directory where "setup.py" is located and run the following command:
```bash
$ python setup.py install     # You may need root priviliges or use the --user tag
```
The software should be installed correctly. You may validate the installation by executing the following commands:
```bash
$ python
```
```python
>>> import lpfgopt
>>> lpfgopt.__version__
'X.X.X'
>>> lpfgopt.unit_test()

opt best: [  3.00000000e+00  -1.01889931e-07   2.48474385e-07]


opb best: [  3.00000000e+00   5.42088925e-08  -3.95903947e-07]
Number of calls: 406


opf best: [  3.00000000e+00   1.97715430e-07   6.38317654e-08]
Number of calls: 414

>>>
```
If the `lpfgopt.unit_test()` command produces the above output congratulations! You have successfully installed the package!

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
Best Solution [  3.00000000e+00   1.37749213e-07   1.87748157e-08]
Best [  3.00000000e+00   5.28168200e-08  -3.45605614e-07]
Worst [  3.00000000e+00   4.06218529e-07   1.51397317e-07]
Final Error 9.85836684782e-06
Number of iterations 354
Final Point set
[[  3.00000000e+00   1.57868094e-06   7.66937258e-07]
 [  3.00000000e+00   4.06218529e-07   1.51397317e-07]
 [  3.00000000e+00   5.28168200e-08  -3.45605614e-07]
 [  3.00000000e+00  -3.97630722e-07  -7.12064238e-07]
 [  3.00000000e+00  -2.04532346e-08  -1.28154364e-06]
 [  3.00000000e+00  -1.63480318e-06  -6.72669205e-07]
 [  3.00000000e+00   9.72430342e-07  -6.68945778e-07]
 [  3.00000000e+00   1.04107370e-06  -7.66470995e-07]
 [  3.00000000e+00   1.89352591e-06  -9.51089092e-07]
 [  3.00000000e+00   1.02503206e-07   6.62107972e-07]
 [  3.00000000e+00   7.44700974e-07  -2.24116728e-07]
 [  3.00000000e+00   3.60869437e-07  -6.66090227e-07]
 [  3.00000000e+00  -7.83721935e-07  -6.67303139e-07]
 [  3.00000000e+00  -1.41274123e-06  -1.11464592e-06]
 [  3.00000000e+00   1.42466667e-06  -1.03165734e-06]
 [  3.00000000e+00   7.81033720e-07  -3.85818548e-07]
 [  3.00000000e+00  -8.51362974e-07   6.78705726e-07]
 [  3.00000000e+00   1.51469283e-06   1.56529366e-07]
 [  3.00000000e+00   9.68223470e-07   1.25689063e-06]
 [  3.00000000e+00   1.04756433e-08   1.63039424e-06]]
```
## Removal
[Nothing here yet]
