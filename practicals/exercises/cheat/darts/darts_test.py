#!/usr/bin/env python

import darts
import time
import numpy
import math
import sys
sys.path.append("./lib/python2.7/site-packages")
import cdarts

def main ():
    """Time result of Monte--Carlo calculations for a number of sample sizes (log spacing)"""

    # generate values for number of tries
    nVals = numpy.logspace (1, 8, base=10.0, num=6, dtype=numpy.int)

    print "     Ntot Python     NumPy      Numba      Cython     multiprocessing"
    for numPoints in nVals:
        # pure Python
        t1 = time.time ()
        n1 = darts.numQuadrantHitsPython (numPoints)
        e1 = math.fabs (4.0 * float (n1) / float (numPoints) - math.pi)
        t1 = time.time () - t1
        # NumPy implementation
        t2 = time.time ()
        n2 = darts.numQuadrantHitsNumpy (numPoints)
        e2 = math.fabs (4.0 * float (n2) / float (numPoints) - math.pi)
        t2 = time.time () - t2
        # Numba implementation
        t3 = time.time ()
        n3 = darts.numQuadrantHitsNumba (numPoints)
        e3 = math.fabs (4.0 * float (n3) / float (numPoints) - math.pi)
        t3 = time.time () - t3
        # Cython implementation
        t4 = time.time ()
        n4 = cdarts.numQuadrantHits (numPoints, 4)
        e4 = math.fabs (4.0 * float (n4) / float (numPoints) - math.pi)
        t4 = time.time () - t4
        # multiprocessing implementation
        t5 = time.time ()
        n5 = darts.numQuadrantHitsMP (numPoints, 4)
        e5 = math.fabs (4.0 * float (n5) / float (numPoints) - math.pi)
        t5 = time.time () - t5

        # report time and print error
        print "{:9d} {:6.4e} {:6.4e} {:6.4e} {:6.4e} {:6.4e} {:12.8e} {:12.8e} {:12.8e} {:12.8e} {:12.8e}".format (numPoints, t1, t2, t3, t4, t5, e1, e2, e3, e4, e5)


if __name__ == "__main__":
    main()
