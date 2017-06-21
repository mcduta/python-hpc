from mpi4py import MPI
import numpy

def main (comm):
    if comm.rank == 0:
        # rank 0 has ndarray data
        buf = numpy.arange (6, dtype=numpy.float64)
        # and dict data
        obj = {"x": 1, "y": 3.14, "z": 1-2j}
    else:
        # all other have an empty array
        buf = numpy.empty (6, dtype=numpy.float64)
        # and a place-holder
        obj = None

    # broadcast from rank 0 to everybody
    comm.Bcast ( [buf, MPI.DOUBLE] , root=0 )
    obj = comm.bcast ( obj, root=0 )

    # check: all processes print data
    print "[%d] %s %s" % (comm.rank, buf, obj["y"])


if __name__ == "__main__":
    main (MPI.COMM_WORLD)
