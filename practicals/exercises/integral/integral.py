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
# ===== importable module: main does nothing
#

if __name__ == "__main__":
    import warnings
    warnings.simplefilter ("ignore")
