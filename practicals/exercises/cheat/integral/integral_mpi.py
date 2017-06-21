#!/usr/bin/env python

from mpi4py import MPI
import math
import numpy
import integral

def main (comm):
    """Compute a definite integral using the trapezium rule"""

    # size and rank of communicator
    size = comm.Get_size()
    rank = comm.Get_rank()

    # interval ends
    a, b = 0.0, numpy.sqrt(numpy.pi)

    # array with values for number of points
    NVals = numpy.logspace (1, 8, base=10.0, num=6, dtype=numpy.int)

    # compute Pi (as a definite integral) using two methods
    for N in NVals:

        # use Wtime to time processing
        wt = MPI.Wtime()

        # calculate local integration limits
        h = (b - a) / float (N)
        N1 = (N* rank)   / size
        N2 =  N*(rank+1) / size
        aProc = a + N1 * h
        bProc = a + N2 * h

        # local integral value
        valProc = integral.trapintNumPy (aProc, bProc, N2-N1)

        # reduce values
        valProcVec = numpy.array ([valProc])
        valVec     = numpy.zeros (1, dtype=float)
        comm.Reduce (valProcVec, valVec, op=MPI.SUM, root=0)

        # use Wtime to time processing
        wt = MPI.Wtime() - wt

        # root process prints result
        if rank == 0:
            print "{:9d} {:6.4e} {:10.8f}".format (N, wt, math.fabs(valVec[0] - 1.0))



if __name__ == "__main__":
    """Run with a large number of points"""
    main (MPI.COMM_WORLD)
