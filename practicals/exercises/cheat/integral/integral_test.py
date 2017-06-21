#!/usr/bin/env python

import time
import math
import numpy
import integral
import sys
sys.path.append("./lib/python2.7/site-packages")
import cpintegral


def main ():
    """Compute a definite integral using the trapezium rule"""

    # interval ends
    a, b = 0.0, numpy.sqrt(numpy.pi)

    # array with values for number of points
    NVals = numpy.logspace (3, 8, base=10.0, num=6, dtype=numpy.int)

    # compute Pi (as a definite integral) using two methods
    print ("     N    Numpy     Numba  Cython")

    for N in NVals:
        # # pure Python
        # t1 = time.time ()
        # v1 = integral.trapintPython (a, b, N)
        # e1 = math.fabs (v1 - 1.0)
        # t1 = time.time () - t1
        # NumPy implementation
        t2 = time.time ()
        v2 = integral.trapintNumPy (a, b, N)
        e2 = math.fabs (v2 - 1.0)
        t2 = time.time () - t2
        # Numba implementation
        t3 = time.time ()
        v3 = integral.trapintNumba (a, b, N)
        e3 = math.fabs (v3 - 1.0)
        t3 = time.time () - t3
        # Cython implementation
        t4 = time.time ()
        v4 = cpintegral.trapint (a, b, N, 4)
        e4 = math.fabs (v4 - 1.0)
        t4 = time.time () - t4

        # report time and print error
        # print "{:9d} {:6.4e} {:6.4e} {:6.4e} {:6.4e} {:12.8e} {:12.8e} {:12.8e} {:12.8e}".format (N, t1, t2, t3, t4, e1, e2, e3, e4)
        print "{:9d} {:6.4g} {:6.4g} {:6.4g}".format(N, t2, t3, t4)

if __name__ == "__main__":
    main ()
