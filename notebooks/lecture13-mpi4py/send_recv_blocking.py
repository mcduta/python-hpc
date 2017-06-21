"""A simple blocking Send/Recv pair"""

from mpi4py import MPI
import numpy
import sys

def main (comm):
    """Send a message between ranks 0 and 1"""

    if comm.size != 2:
        sys.stdout.write ("Only two processes allowed\n")
        comm.Abort(1)

    # buffer length
    blen = 4
    # process rank
    rank = comm.Get_rank()

    if rank == 0:
        # create send buffer
        buf = numpy.ones (blen, numpy.double)
        # send buffer
        comm.Send ( [buf, blen, MPI.DOUBLE], dest = 1, tag = 999 )
    elif rank == 1:
        # allocate space for recv buffer
        buf = numpy.empty (blen, numpy.double)
        # receive buffer
        comm.Recv ( [buf, blen, MPI.DOUBLE], source = 0, tag = 999 )
        print " rank 1 received: %s" % (buf)

if __name__ == "__main__":
    main (MPI.COMM_WORLD)
