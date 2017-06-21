#!/usr/bin/env python

import time
import math
import numpy
import integral


def main ():
    """Compute a definite integral using the trapezium rule"""

    # interval ends
    a, b = 0.0, numpy.sqrt(numpy.pi)

    # array with values for number of points
    NVals = numpy.logspace (1, 8, base=10.0, num=6, dtype=numpy.int)

    # compute Pi (as a definite integral) using two methods
    for N in NVals:
        # pure Python
        t1 = time.time ()
        v1 = integral.trapintPython (a, b, N)
        e1 = math.fabs (v1 - 1.0)
        t1 = time.time () - t1

        # report time and print error
        print "{:9d} {:6.4e} {:12.8e}".format (N, t1, e1)


if __name__ == "__main__":
    main ()
