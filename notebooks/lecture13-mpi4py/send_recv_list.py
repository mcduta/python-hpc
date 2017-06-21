from mpi4py import MPI
import sys

def main (comm):
    """Send a list from rank 0 to rank 1"""

    if comm.size != 2:
        sys.stdout.write ("Only two processes allowed\n")
        comm.Abort(1)

    if comm.rank == 0:
        msg = ["Any", "old", "thing", comm.rank, {"size" : comm.size}]
        comm.send (msg, dest=1, tag = 999)
    elif comm.rank == 1:
        msg = comm.recv (source=0, tag = 999)
        print " rank 1 received: %s" % (msg)


if __name__ == "__main__":
    main(MPI.COMM_WORLD)
