from InsideMe import profiler
from InsideMe import communication as comm
import numpy as np
import os

@profiler.benchmark(field='Generate data set')
def generate_data(nmc, rank):
    """
    Generate fake data set

    Parameters
    -----------
        * nmc: int, number of MC simulations
        * rank: int, the rank of the processor
    """
    rand_vec = np.zeros((nmc, nmc * (rank + 1)))

    for mc in range(nmc):
        rand_vec[mc] = np.random.rand(nmc * (rank + 1))

    return rand_vec

@profiler.benchmark(field='Computation')
def accumulate_data(dataset, rank):
    """
    Accumulate random vectors into a matrix

    Parameters
    -----------
        * dataset: 2D array, (nmc, nmc * (rank + 1)) array containing your
            measurements.
        * rank: int, the rank of the processor
    """
    nmc = dataset.shape[0]
    mat = np.zeros((nmc * (rank + 1), nmc * (rank + 1)))

    for mc in range(nmc):
        mat += np.outer(dataset[mc], dataset[mc])

    return mat

@profiler.benchmark(field='I/O')
def write_on_disk(mat, fname):
    """
    Write and delete files on disk

    Parameters
    -----------
        * mat: 2D array, (nmc * (rank + 1), nmc * (rank + 1)) array
            containing the accumulated measurements.
        * fname: string, name of the output file where mat will be saved.
    """
    np.save(fname ,mat)
    os.remove(fname)

if __name__ == "__main__":
    for trial in range(20):
        dataset = generate_data(nmc=10*trial, rank=comm.rank)
        mat = accumulate_data(dataset, rank=comm.rank)
        write_on_disk(mat, 'test_proc%d.npy' % (comm.rank))
    comm.barrier()
