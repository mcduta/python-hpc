import cython
from cython.parallel import prange, parallel
cimport openmp

@cython.boundscheck(False)
@cython.wraparound(False)
def timestep (double [:, :] u,
              double [:, :] uo,
              double nu):
    """ time-steps implemented using cython and straight python array indexing"""
    # c-style type definitions
    cdef int nx,ny
    cdef int i, j
    # array size
    nx = u.shape[0]
    ny = u.shape[1]
    # apply numerical scheme (one time-step)
    for i in prange(1, nx-1, nogil=True):
        for j in range(1, ny-1):
            u[i,j] = uo[i,j] + ( nu * ( uo [i-1, j] + uo [i+1, j] +
                                        uo [i, j-1] + uo [i, j+1]
                                        - 4.0 * uo [i,j] ) )
