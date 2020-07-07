# Leapfrog Optimizer Package

- Author  : Mark Redd
- Email   : redddogjr@gmail.com
- GitHub  : https://github.com/flythereddflagg
- Website : http://www.r3eda.com/

## About

This package is based the [*Leapfrogging Optimization Algorithm*](http://www.r3eda.com/leapfrogging-optimization-algorithm/) published by [Dr. R. Russell Rhinehart](http://www.r3eda.com/about-russ/). The following publications explain the technique:

- Rhinehart, R. R., M. Su, and U. Manimegalai-Sridhar, “Leapfrogging and Synoptic Leapfrogging: a new optimization approach”, Computers & Chemical Engineering, Vol. 40, 11 May 2012, pp. 67-81.

- Manimegalai-Sridhar, U., A. Govindarajan, and R. R. Rhinehart, “Improved Initialization of Players in Leapfrogging Optimization”, Computers & Chemical Engineering, Vol. 60, 2014, 426-429.

- Rhinehart, R. R., “Convergence Criterion in Optimilsation of Stochastic Processes”, Computers & Chemical Engineering, Vol. 68, 4 Sept 2014, pp 1-6.

## Installation 

You can install the lite versions via pip or using the setup.py script in the source code. Instructions are shown below.

#### Minimum system Requirements for Installation

 - Python >= 3.6

#### Recommended System Requirements for Installation

- Windows or Linux
- x86 processor with a 64-bit architecture
- Additional Python Packages:
  - scipy
  - numpy
  - pytest

### Via pip

The `lpfgopt` package may be installed with `pip` using the following command:

```bash
$ pip install lpfgopt # You may need root privileges or the --user tag
```

If you wish to install locally with `pip` you may do the following:
- Download and unzip the archive or clone it with git.
- Open the main directory where `setup.py` is located and run the following command:
  ```bash
  $ pip install .
  ```
### Via setup.py

- Download the 'lite' branch and unzip the archive or clone it with git.
- Open the main directory where "setup.py" is located and run the following command:
  ```bash
  $ python setup.py install     # You may need root priviliges or use the --user tag
  ```
The software should be installed correctly. You may validate the installation by executing the following commands:
```python
$ python
>>> import lpfgopt
>>> lpfgopt.__version__
'X.X.X'
>>> lpfgopt.minimize(lambda x: x[0]**2 + 10, [[-10, 10]])['x']
[<approximately 0.0>]
>>>
```
If the above commands produce the output congratulations! You have successfully installed the package!
## Usage
Use the `lpfgopt.minimize` function to solve optimization problems of the form:

$minimize$ $f(x)$
$s.t.:$

- $g(x) \le 0$

- $bound_{1,1} \le x[1] \le bound_{1,2}$

  $bound_{2,1} \le x[2] \le bound_{2,2}$

  $...$

  $bound_{n,1} \le x[n] \le bound_{n,2}$

where $n$ is the number of decision variables and $bound$ is an array-like with shape $(n, 2)$. $bound$ may be a list of lists or a `numpy` `ndarray`.

### Example Usage
The following is a simple optimization where the minimum value of the following equation is found:  
 - $f(x) = x^2+y^2$

 - Subject to: 

   $g(x) = -x^2 - y + 10 \le 0$ **or** g(x) = -x^2 - y + 10 <= 0

   $$x, y \in [-5, 5]$$
```python
# test_lpfgopt.py
from lpfgopt import minimize
import matplotlib.pyplot as plt

# set up the objective funciton, 
# constraint fuction and bounds
f = lambda x: sum([i**2 for i in x])
g = lambda x: -x[0]**2 + 10 - x[1] 
bounds = [[-5,5] for i in range(2)]

# run the optimization
sol = minimize(f, bounds, fconstraint=g)['x']
print(f"Solution is: {sol}")

# plot the results on a contour plot
gg = lambda x: -x**2 + 10 # for plotting purposes

plt.figure(figsize=(8,8))
x, y = np.linspace(-5,5,1000), np.linspace(-5,5,1000)
X, Y = np.meshgrid(x,y)
Z = f([X,Y])

plt.contourf(X,Y,Z)
plt.plot(x, gg(x), "r", label="constraint")
plt.plot(*sol, 'x', 
         markersize=14, 
         markeredgewidth=4, 
         color="lime", 
         label="optimum")
plt.ylim(-5,5)
plt.xlim(-5,5)
plt.legend()
plt.show()
```
This code will produce the following output:
```bash
Solution is: [-3.0958051486911997, 0.4159905027317925]
```
As well as a plot that should look similar to the following image:

![](./docs/media/sample_opt.png)
