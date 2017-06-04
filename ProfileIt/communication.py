import os
import sys
import time

verbose = False

try:
    from mpi4py import MPI
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()
    barrier = MPI.COMM_WORLD.Barrier
    finalize = MPI.Finalize
    Wtime = MPI.Wtime
    if verbose:
        print 'Parallel setup OK, rank %s in %s' % (rank, size)
except:
    # No mpi4py
    rank = 0
    size = 1
    barrier = lambda: -1
    finalize = lambda: -1
    Wtime = time.time
    if verbose:
        print 'No mpi4py found - switching to serial mode'
