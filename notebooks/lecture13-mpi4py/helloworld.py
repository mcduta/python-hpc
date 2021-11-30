"""Hellow world!  Importing and using MPI.COMM_WORLD"""

from mpi4py import MPI

def report (communicator):
    """Report rank and size of this communicator"""
    rank = communicator.rank
    size = communicator.size
    print (F"Hello from rank {rank} of {size}.")

if __name__ == "__main__":
    """Execute in MPI.COMM_WORLD"""
    report (MPI.COMM_WORLD)
