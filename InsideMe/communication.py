import os
import sys
import time

verbose = False

try:
    from mpi4py import MPI
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()
    barrier = MPI.COMM_WORLD.Barrier
    Wtime = MPI.Wtime
    bcast = MPI.COMM_WORLD.bcast
    comm = MPI.COMM_WORLD
    if verbose:
        print 'Parallel setup OK, rank %s in %s' % (rank, size)
except:
    # mpi4py not found or serial call
    rank = 0
    size = 1
    barrier = lambda: -1
    Wtime = time.time
    def bcast(data, root):
        return data
    if verbose:
        print 'No mpi4py found - switching to serial mode'

if rank == 0:
    start = Wtime()
else:
    start = None
start = bcast(start, root=0)
fname = 'logproc_%d_%d_%d.log' % (start, rank, size)
