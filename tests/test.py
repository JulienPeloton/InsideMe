## Example script
from InsideMe import profiler
from InsideMe import communication as comm
import numpy as np
import os
import string
import random

@profiler.benchmark(field='Computation')
def generate_data(nmc, size):
    """
    Generate fake data set.

    Parameters
    -----------
        * nmc: int, number of MC simulations
        * size: int, boost factor to expand the size of our vector
    """
    rand_vec = np.zeros((nmc, nmc * (size + 1)))

    for mc in range(nmc):
        rand_vec[mc] = np.random.rand(nmc * (size + 1))

    return rand_vec

@profiler.benchmark(field='Computation')
def accumulate_data(dataset, size):
    """
    Accumulate random vectors into a matrix.

    Parameters
    -----------
        * dataset: 2D array, (nmc, nmc * (size + 1)) array
            containing your measurements.
        * size: int, boost factor to expand the size of our vector
    """
    nmc = dataset.shape[0]
    mat = np.zeros((nmc * (size + 1), nmc * (size + 1)))

    for mc in range(nmc):
        mat += np.outer(dataset[mc], dataset[mc])

    return mat

@profiler.benchmark(field='I/O')
def write_on_disk(mat, fname):
    """
    Write and delete files on disk.

    Parameters
    -----------
        * mat: 2D array, (nmc * (rank + 1), nmc * (rank + 1)) array
            containing the accumulated measurements.
        * fname: string, name of the output file where mat will be saved.
    """
    np.save(fname ,mat)
    os.remove(fname)

@profiler.benchmark(field='Communication')
def Reduce(mat, root):
    """
    Wrapper around reduce function.

    Parameters
    -----------
        * mat: 2D array, the matrix that has to be sent to root
        * root: int, rogue leader.
    """
    out = comm.comm.reduce(mat, op=comm.MPI.SUM, root=root)
    return out

## We decide to not monitor this one for example
## It will be categorized in the <Others> field in plots.
def random_generator(
    size=6, chars=string.ascii_uppercase + string.digits):
    """
    Just for the fun.
    """
    return ''.join(random.choice(chars) for x in range(size))

if __name__ == "__main__":
    for trial in range(20):
        dataset = generate_data(nmc=10*trial, size=comm.size)
        mat = accumulate_data(dataset, size=comm.size)
        mat = Reduce(mat, root=0)
        if comm.rank == 0:
            write_on_disk(mat, '%s.npy' % random_generator())
    comm.barrier()
