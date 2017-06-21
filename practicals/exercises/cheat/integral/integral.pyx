# always import cython
import cython
# import modules for multithreading
from cython.parallel import prange, parallel
cimport openmp
# import external C mathematical functions
from libc.math cimport sin

# eliminate Python checks
@cython.cdivision(True)


#
# ----- function to integrate
#
cdef double func (double x) nogil:
    """Function to integrate"""
    return x * sin (x*x)


#
# ----- integrator
#
cpdef double trapint (double a, double b, int N, int nt=2):
    """Compute a definite integral using the trapezium rule and pure Python"""

    # variables
    cdef:
        int n
        double x, h, v

    # set number of threads
    openmp.omp_set_num_threads(nt)

    # interval length (N intervals = N+1 nodes)
    h = (b - a) / float (N)

    # initial and final point only count with weight half
    v = (func (a) + func (b)) / 2.0

    # add the interior points
    #   * thread-locality and reductions are automatically inferred for variables
    with nogil:
        for n in prange(1,N):
            x = a + n*h
            # NB reductions are recognised from "+=" only
            v +=  func (x)

    # scale by the interval width
    return v*h
