from mpi4py import MPI
import numpy

def main (comm):
    # ndarray data to send
    sendBuf = numpy.zeros(8, dtype=int) + comm.rank
    # ndarray data to receive
    if comm.rank == 0:
        recvBuf = numpy.empty ([comm.size, 8], dtype=int)
    else:
        recvBuf = None
    # Python object
    obj = (comm.rank+1)**2

    # gather ndarray
    comm.Gather (sendBuf, recvBuf, root=0)
    # gather Python objects
    obj = comm.gather(obj, root=0)

    # check: all ranks print verify data
    print "[%d] %s %s" % (comm.rank, recvBuf, obj)


if __name__ == "__main__":
    main (MPI.COMM_WORLD)
