#!/usr/bin/env python


#
# ===== pure Python implementation
#

# use math.sin -- faster for scalars than numpy.sin
import math

#
# ----- function to integrate
#
def funcPython (x):
    """Function to integrate"""
    return x * math.sin (x*x)

#
# ----- integrator
#
def trapintPython (a, b, N):
    """Compute a definite integral using the trapezium rule and pure Python"""

    # interval length (N intervals = N+1 nodes)
    h = (b - a) / float (N)

    # initial and final point only count with weight half
    v = (funcPython (a) + funcPython (b)) / 2.0

    # add the interior points
    for n in xrange(1,N):
        x = a + n*h
        v = v + funcPython (x)

    # scale by the interval width
    return v*h


#
# ===== pure Python implementation
#

# use numpy.sin, which can work on numpy arrays
import numpy

#
# ----- function to integrate
#
def funcNumpy (x):
    """Function to integrate"""
    return x * numpy.sin (x*x)

#
# ----- integrator
#
def trapintNumPy (a, b, N):
    """Compute a definite integral using the trapezium rule and NumPy arrays"""

    # interval length (N intervals = N+1 nodes)
    h = (b - a) / float (N)

    # initial and final point only count with weight half
    v = (funcNumpy (a) + funcNumpy (b)) / 2.0

    # N+1 nodes
    x = numpy.linspace(a, b, num=N+1)

    # evaluate function at interior nodes
    y = funcNumpy (x[1:-1])

    # add the interior points
    v = v + y.sum()

    # scale by the interval width
    return v*h


#
# ===== Numba implementation
#

#
# ----- integrator
#
from numba import jit
from numba import vectorize

@vectorize("float64 (float64)", nopython=True, target="parallel")
def funcNumba (x):
    """Function to integrate"""
    return x * numpy.sin (x*x)

@jit ("float64 (float64, float64, int64)")
def trapintNumba (a, b, N):
    """Compute a definite integral using the trapezium rule and pure Python"""

    # interval length (N intervals = N+1 nodes)
    h = (b - a) / float (N)

    # initial and final point only count with weight half
    v = (funcNumba (a) + funcNumba (b)) / 2.0

    # N+1 nodes
    x = numpy.linspace(a, b, num=N+1)

    # evaluate function at interior nodes
    y = funcNumba (x[1:-1])

    # add the interior points
    v = v + y.sum()

    # scale by the interval width
    return v*h


#
# ===== importable module: main does nothing
#

if __name__ == "__main__":
    import warnings
    warnings.simplefilter ("ignore")
