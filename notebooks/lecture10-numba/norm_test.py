import math
import numpy
import time

from numba import jit
from numba import vectorize


# --- first take
@jit ("float64 (float64[:], int64)", nopython=True)
def p_norm_JIT (u, p):
    n = u.size
    s = 0.0
    for i in xrange (n):
        s += math.pow (math.fabs(u[i]), p)

    return math.pow (s, 1.0 / float(p))


# --- second take
@vectorize ("float64 (float64, int64)", nopython=True, target="parallel")
def funcNumbaVec (u, p):
    return math.pow (math.fabs(u), p)

#@jit ("float64 (float64[:], int64)", nopython=True)
@jit ("float64 (float64[:], int64)", nogil=True)
def p_norm_JIT_vec (u, p):
    v = funcNumbaVec (u, p)
    return math.pow (v.sum(), 1.0 / float(p))


# --- main
def main ():
    """Time Numba solutions for the p-norm of a vector"""

    # test accuracy
    n = 1024
    u = numpy.random.rand (n)
    # compute norm from linalg
    nrm0 = numpy.linalg.norm (u, 3)
    # compute norm with straight numba
    nrm1 = p_norm_JIT (u, 3)
    # compute norms using extension functions
    nrm2 = p_norm_JIT_vec (u, 3)
    print "relative errors =", math.fabs ( (nrm0 - nrm1) / nrm0 ), math.fabs ( (nrm0 - nrm2) / nrm0 )

    # test performance
    n = 5 * 10**7
    u = numpy.random.rand (n)

    t0 = time.time ()
    nrm0 = numpy.linalg.norm (u, 3)
    t0 = time.time () - t0

    t1 = time.time ()
    nrm1 = p_norm_JIT (u, 3)
    t1 = time.time () - t1

    t2 = time.time ()
    nrm2 = p_norm_JIT_vec (u, 3)
    t2 = time.time () - t2

    print "time linalg = %12.6f" % (t0)
    print "time numba  = %12.6f" % (t1)
    print "time numba  = %12.6f" % (t2)


if __name__ == "__main__":
    main()
