"""
filename: opt_result.py
Package: lpfgopt
author: Travis E. Oliphant, modified by Mark Redd
email: redddogjr@gmail.com
website: http://www.r3eda.com/
about:
This is a modified copy of the OptimizeResult class in the scipy.optimize
package. It has been modified to fit the needs of the lpfgopt package.
The following notice occurs in the original:
********NOTICE***************
* optimize.py module by Travis E. Oliphant
*
* You may copy and use this module as you see fit with no
* guarantee implied provided you keep this notice in all copies.
*******END NOTICE************
"""

class OptimizeResult(dict):
    """ Represents the optimization result.
    Attributes
    ----------
    x : array-like
        The solution of the optimization.
    success : bool
        Whether or not the optimizer exited successfully.
    status : int
        Termination status of the optimizer. Its value depends on the
        underlying solver. Refer to `message` for details.
    message : str
        Description of the cause of the termination.
    fun : float
        Value of objective function at x.
    nfev: int
        Number of evaluations of the objective functions.
    nit : int
        Number of iterations performed by the optimizer.
    maxcv : float
        The maximum constraint violation.
    best : array-like
        Array of the form [fun(x), x[0], x[1]...x[len(x) - 1]]
    worst : array-like
        Array of the form [fun(w), w[0], w[1]...w[len(w) - 1]] 
        where 'w' is the array of optimization values that 
        produced the worst objective fucntion value upon 
        termination.
    final_error : float
        The value of the error upon termination. If the optimization
        was successful error should be less than the tolerance.
    pointset : 2-d array-like
        Array-like with shape = (n_points, len(x) + 1) where n_points
        is the number of players used in optimization.
    Notes
    -----
    Since this class is essentially a subclass of dict
    with attribute accessors, one can see which attributes are available
    using the `keys()` method.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        if self.keys():
            m = max(map(len, list(self.keys()))) + 1
            return '\n'.join([k.rjust(m) + ': ' + repr(v)
                              for k, v in sorted(self.items())])
        else:
            return self.__class__.__name__ + "()"

    def __dir__(self):
        return list(self.keys())
