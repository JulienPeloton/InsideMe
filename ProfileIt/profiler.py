import communication as comm
from time import time
from os import uname
import resource

## Should be replace by automatic versioning
VERSION = 'ProfileIt v0.1.0'

## True is good
DEBUG = True

## The conversion factor used for the memory
## consumption depends on the machine.
## resource.getrusage().ru_maxrss can be either in kB or Bytes.
if 'Darwin' in uname():
    MEMORY_CONV = 1024.**2
elif 'Linux' in uname():
    MEMORY_CONV = 1024.
else:
    print('Not tested yet on Windows!\n')
    print('Check the conversion factor for ru_maxrss.\n')
    print('Set by default to 1024 (kB to Mb).\n')
    MEMORY_CONV = 1024.

def time_benchmark(func):
    """
    Print the time in second that a function takes to execute.

    Parameters
    ----------
        * func: function, the function to be benchmarked
    """
    if DEBUG is True:
        def wrapper(*args, **kwargs):
            t0 = time()
            res = func(*args, **kwargs)
            print("{} -- [{}/{}] @{} took {:0.3f} seconds\n".format(
                VERSION,
                comm.rank,
                comm.size,
                func.__name__,
                time() - t0))
            return res
    else:
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
    return wrapper

def memory_benchmark(func):
    """
    Print the memory used by a function.

    Parameters
    ----------
        * func: function, the function to be benchmarked
    """
    if DEBUG is True:
        def wrapper(*args, **kwargs):
            m0 = resource.getrusage(
                resource.RUSAGE_SELF).ru_maxrss / MEMORY_CONV
            res = func(*args, **kwargs)
            m1 = resource.getrusage(
                resource.RUSAGE_SELF).ru_maxrss / MEMORY_CONV
            print("{} -- [{}/{}] @{} took {:0.3f} MB ({:0.3f} -> {:0.3f})\n".format(
                VERSION,
                comm.rank,
                comm.size,
                func.__name__,
                m1 - m0,
                m0,
                m1))
            return res
    else:
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
    return wrapper
