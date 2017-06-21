from mpi4py import MPI
import numpy

def main(comm):

    # ndarray data
    buf  = ( numpy.ones (6, dtype=int) + 1 ) * comm.rank
    buf2 = numpy.empty (6, dtype=int)

    # Python object data
    obj  = [ comm.rank ]

    # reduction on ndarray: buf reduced to buff2
    # comm.Reduce ( buf, buf2, op=MPI.SUM, root=0 ) # <- this works too
    comm.Reduce ( [buf, MPI.INT], [buf2, MPI.INT], op=MPI.SUM, root=0 )

    # reduction of Python object
    obj  = comm.reduce ( [comm.rank], op=MPI.SUM, root=0 )

    # all processes print data
    if comm.rank == 0:
        print "[%d] %s %s <- reduced" % (comm.rank, buf2, obj)
    else:
        print "[%d] %s %s" % (comm.rank, buf, obj)

if __name__ == "__main__":
    main(MPI.COMM_WORLD)
