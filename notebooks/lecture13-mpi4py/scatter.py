from mpi4py import MPI
import numpy

def main (comm):
    if comm.rank == 0:
        # rank 0 has ndarray data
        sendBuf = numpy.empty ([comm.size, 8], dtype=int)
        sendBuf.T[:,:] = range(comm.size)
        # and list data
        obj = [(i+1)**2 for i in range(comm.size)]
    else:
        # all other ranks have an empty send buffer
        sendBuf = None
        # and a place-holder
        obj = None

    # all ranks have a receiving buffer 
    recvBuf = numpy.empty (8, dtype=int)

    # broadcast from rank 0 to everybody
    comm.Scatter (sendBuf, recvBuf, root=0)
    obj = comm.scatter ( obj, root=0 )

    # check: all processes verify data
    print "[%d] %s %s" % (comm.rank, recvBuf, obj)
    # check: cleverer way is to use assert
#   assert numpy.allclose (recvBuf, comm.rank)
#   assert obj == (comm.rank+1)**2

if __name__ == "__main__":
    main (MPI.COMM_WORLD)
