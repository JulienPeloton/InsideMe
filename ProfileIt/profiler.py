from os import uname
import resource

import communication as comm

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

def benchmark(field=''):
    """
    Record the time in second that a function takes to execute and
    the memory consumption of that function.

    Parameters
    ----------
        * field: string, keyword to identify the main purpose of the function
            to be benchmarked: I/O, computation, etc. If empty, field will
            be the at symbol followed by the name of the benchmarked function.
    """
    ## accessing and assigning variables with python 2.7...
    ## TODO fix this workaround
    field = [field]
    def outer_wrapper(func):
        """
        Parameters
        ----------
            * func: function, the function to be benchmarked
        """
        def inner_wrapper(*args, **kwargs):
            m0 = resource.getrusage(
                resource.RUSAGE_SELF).ru_maxrss / MEMORY_CONV
            t0 = comm.Wtime()
            res = func(*args, **kwargs)
            t1 = comm.Wtime()
            m1 = resource.getrusage(
                resource.RUSAGE_SELF).ru_maxrss / MEMORY_CONV
            fname = 'logproc_%d_%d.log' % (comm.rank, comm.size)
            if field[0] == '':
                name = '@' + func.__name__
            else:
                name = field[0]
            with open(fname, 'a') as f:
                f.write(
                    "{}/{}/@{}/{:0.3f}/{:0.3f}/{:0.3f}/{:0.3f}/{}\n".format(
                        comm.rank, comm.size,
                        func.__name__,
                        t0, t1,
                        m0, m1,
                        name))
            return res
        return inner_wrapper
    return outer_wrapper
