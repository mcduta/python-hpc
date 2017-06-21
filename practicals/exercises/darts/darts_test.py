#!/usr/bin/env python

import darts
import time
import numpy
import math

def main ():
    """Time result of Monte--Carlo calculations for a number of sample sizes (log spacing)"""

    # generate values for number of tries
    nVals = numpy.logspace (1, 8, base=10.0, num=6, dtype=numpy.int)

    for numPoints in nVals:
        # pure Python
        t1 = time.time ()
        n1 = darts.numQuadrantHitsPython (numPoints)
        e1 = math.fabs (4.0 * float (n1) / float (numPoints) - math.pi)
        t1 = time.time () - t1

        # report time and print error
        print "{:9d} {:6.4e} {:12.8e}".format (numPoints, t1, e1)


if __name__ == "__main__":
    main()
