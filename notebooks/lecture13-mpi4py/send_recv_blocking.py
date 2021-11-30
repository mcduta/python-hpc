"""A simple blocking Send/Recv pair"""

from mpi4py import MPI
import numpy

def main (comm):
    """Send a message between ranks 0 and 1"""

    if comm.size != 2:
        raise ValueError("only two processes allowed")
        comm.Abort(1)

    # buffer length
    blen = 4
    # process rank
    rank = comm.Get_rank()

    if rank == 0:
        # create send buffer
        buf = numpy.ones (blen, numpy.double)
        # report
        print(F" rank 0 sending: {buf}")
        # send buffer
        comm.Send ( [buf, blen, MPI.DOUBLE], dest = 1, tag = 999 )
        # report
        print(F" rank 0 sent: {buf}")

    elif rank == 1:
        # allocate space for recv buffer
        buf = numpy.empty (blen, numpy.double)
        # report
        print(F" rank 1 receives in: {buf}")
        # receive buffer
        comm.Recv ( [buf, blen, MPI.DOUBLE], source = 0, tag = 999 )
        # report
        print(F" rank 1 received: {buf}")

if __name__ == "__main__":
    main (MPI.COMM_WORLD)
