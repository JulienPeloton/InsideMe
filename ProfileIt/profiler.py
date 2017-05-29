import communication as comm
from time import time
from time import localtime
from os import uname
from os import makedirs
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


def benchmark(CONV=None, field=None):
    """
    Record the time in second that a function takes to execute and
    the memory consumption of that function.

    Parameters
    ----------
        * CONV: string, convert units. By default units are second. User can
            specify hour, min, ms, us.
        * field: string, keyword to identify the main purpose of the function
            to be benchmarked: I/O, computation, etc.
    """
    ## accessing and assigning variables with python 2.7...
    ## TODO fix this horrible workaround
    field = [field]
    def outer_wrapper(func):
        """
        Parameters
        ----------
            * func: function, the function to be benchmarked
        """
        if DEBUG is True:
            def inner_wrapper(*args, **kwargs):
                m0 = resource.getrusage(
                    resource.RUSAGE_SELF).ru_maxrss / MEMORY_CONV
                t0 = time()
                res = func(*args, **kwargs)
                t1 = time()
                m1 = resource.getrusage(
                    resource.RUSAGE_SELF).ru_maxrss / MEMORY_CONV
                fname = 'logproc_%d_%d.log' % (comm.rank, comm.size)
                if field[0] is None:
                    name = func.__name__
                else:
                    name = field[0]
                with open(fname, 'a') as f:
                    f.write("{}/{}/@{}/{:0.3f}/{:0.3f}/{:0.3f}/{}\n".format(
                        comm.rank, comm.size,
                        func.__name__,
                        t1 - t0,
                        m0,
                        m1,
                        name))
                return res
        else:
            def inner_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
        return inner_wrapper
    return outer_wrapper
