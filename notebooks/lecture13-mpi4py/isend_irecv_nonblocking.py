from mpi4py import MPI
import numpy

def main (comm):
    """Exchange messages with 'ajoining' ranks"""
    # right-hand adjoining rank (wraparound)
    p1 = comm.rank + 1
    if p1 >= comm.size: p1 = 0
    # left-hand adjoining rank (wraparound)
    m1 = comm.rank - 1
    if m1 < 0: m1 = comm.size - 1

    # send and recv buffers
    smsg = numpy.array ( [comm.rank], numpy.int )
    rmsg = numpy.zeros ( 2, numpy.int )

    # initiate communication
    reqs1 = comm.Isend (smsg, p1)
    reqs2 = comm.Isend (smsg, m1)
    reqr1 = comm.Irecv (rmsg[0:], source = p1)
    reqr2 = comm.Irecv (rmsg[1:], source = m1)

    # receive requests handled by Wait()
    reqr1.Wait()
    reqr2.Wait()

    # all processes print
    # NB: safe to print as messages were received already
    print "[%d] %s %s %s" % (comm.rank, smsg, rmsg[1], rmsg[0])

    # send requests handled by Waitall()
    MPI.Request.Waitall ( [reqs1, reqs2] )


if __name__ == "__main__":

    main(MPI.COMM_WORLD)
