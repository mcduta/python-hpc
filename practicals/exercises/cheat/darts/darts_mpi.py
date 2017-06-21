"""
   Exercise: use Monte-Carlo integration on the unit circle to compute Pi
   Notes:    this version uses Send()/Recv() and numpy arrays
"""

import darts
import math
import numpy
from mpi4py import MPI


def main (comm):
    """Compute Pi using Monte-Carlo integration"""

    # the size of the communicator and the rank of this process
    size = comm.Get_size()
    rank = comm.Get_rank()

    # compute Pi with different number of points
    numPointsVals = numpy.logspace (4, 8, base=10.0, num=6, dtype=numpy.int)

    for numPoints in numPointsVals:
        # use Wtime to time processing
        wt = MPI.Wtime()
        # N_tot is the number of random points each process deals with
        numPointsProc = numPoints / size
        # initialise RNG using rank
        numpy.random.seed (rank)
        # put valuew in vector
        numHitsProc = numpy.zeros (1, dtype=int)
        numHits     = numpy.zeros (1, dtype=int)
        # each process counts
        numHitsProc[0] = darts.numQuadrantHitsNumpy (numPointsProc)
        # reduce value
        comm.Reduce ([numHitsProc, 1, MPI.INT], numHits, op=MPI.SUM, root=0)
        # use Wtime to time processing
        wt = MPI.Wtime() - wt
        # root process prints result
        if rank == 0:
            pi  = 4.0 * float (numHits[0]) / float (numPoints)
            err = math.fabs (pi - math.pi)
            print "{:9d} {:6.4e} {:10.8f}".format (numPoints, wt, err)


if __name__ == "__main__":
    """Run with a large number of points"""
    main (MPI.COMM_WORLD)
