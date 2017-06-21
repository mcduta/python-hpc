# always import cython
import cython
# import modules for multithreading
from cython.parallel import prange, parallel
cimport openmp
# import external C random number generator
from libc.stdlib cimport rand, RAND_MAX
## # import printf (in order to print from nogil region)
## from libc.stdio cimport printf


#
# ===== simple Python implementation
#
cpdef int numQuadrantHits (int numPoints, int nt=2):
    """Compute the number of hits in a unit circle quadrant"""

    cdef:
        # counter for the number of hits
        int nhits = 0
        # iteration
        int n
        # coordinates of random point
        double x, y

    # the inverse of RAND_MAX (avoid expensive divisions)
    randMaxInv = 1.0 / float(RAND_MAX)

    # set number of threads
    openmp.omp_set_num_threads(nt)

    # count darts that fall inside the circle
    with nogil:
        for n in prange(numPoints):
            # generate random point inside the unit square (0,0), (0,1), (1,1), (1,0)
            x = rand() * randMaxInv
            y = rand() * randMaxInv
 ##         # print to check threads do generate different random numbers
 ##         printf("%d %f %f\n", openmp.omp_get_thread_num(), x, y)
             # if inside unit circle, count a hit
            if (x*x + y*y) <= 1.0:
                nhits += 1

    return nhits
