import cython
cimport cython
import math


#
# === simplest function definition (pure Python)
#
def p_norm (u, p):
    n = u.size
    s = 0.0
    for i in range (n):
        s += math.pow (math.fabs(u[i]), p)

    return math.pow (s, 1.0 / float(p))


#
# === better function definition
#     * C types
#
cpdef double p_norm_types (double [:] u, int n, int p):
    cdef:
        int i
        double s

    s = 0.0
    for i in range (n):
        s += math.pow (math.fabs(u[i]), p)

    return math.pow (s, 1.0 / float (p))


#
# === everything is typed
#     * C types
#     * C external functions
#
from libc.math cimport pow, fabs
#cdef extern from "math.h" nogil:
#    double pow (double x, double y)
#    double fabs (double x)

cpdef double p_norm_types_better (double [:] u, int n, int p):
    cdef:
        int i
        double s

    s = 0.0

    for i in range (n):
        s += pow (fabs(u[i]), p)

    return pow (s, 1.0 / float (p))


#
# === OpenMP function definitions
#     * C types
#     * C functions
#     * add parallel range
#     * remove the GIL
#     * extra compiler directives: no bound check, no wraparound, etc.
#
from libc.math cimport pow, fabs
from cython.parallel import prange, parallel
cimport openmp

cpdef double p_norm_openmp (double [:] u, int n, int p, int nt=2):
    cdef:
        int i
        double s

    s = 0.0

    openmp.omp_set_num_threads (nt)

    with nogil:
        for i in prange (n):
            s += pow (fabs (u[i]), p)

    return pow (s, 1.0 / float (p))


#
# === OpenMP function definition plus external function
#     * C types
#     * C functions
#     * add parallel range
#     * remove the GIL
#     * extra compiler directives: no bound check, no wraparound, etc.
#
from libc.math cimport pow, fabs
from cython.parallel import prange, parallel
cimport openmp

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef double p_norm_openmp_better (double [:] u, int n, int p, int nt=2):

    cdef:
        int i
        double s

    s = 0.0

    openmp.omp_set_num_threads (nt)

    with nogil:
        for i in prange (n):
            s += pow (fabs (u[i]), p)

    return pow (s, 1.0 / float (p))
