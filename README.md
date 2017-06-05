InsideMe
==

### The package
InsideMe is a simple yet effective python module for monitoring
memory consumption and duration of python codes.
Especially relevant when using MPI, it makes use of decorators.

### Before starting
This code has the following dependencies (see the travis install section):
* numpy, matplotlib (required)
* mpi4py (optional - for parallel computing)

### Installation
We provide a setup.py for the installation. Just run:
```bash
python setup.py install
```
Make sure you have correct permissions (otherwise just add --user).
You can also directly use the code by updating manually your PYTHONPATH.
Just add in your bashrc:
```bash
InsideMePATH=/path/to/the/package
export PYTHONPATH=$PYTHONPATH:$InsideMePATH
```

### How to use it

The profiling of a code is done using decorators.
Typically, if you want to monitor the time spent inside a function and its memory usage,
simply add a decorator
```python
## content of toto.py
from InsideMe import profiler

@profiler.benchmark
def myfunc(args):
    ...
```
The profiler will collect informations during the execution of the program,
and store it on a log file. By default, the profiler will use the name of the function for future reference.
It is often the case that one wants to group functions under categories.
You can specify this in the decorator directly:

```python
## content of toto.py
from InsideMe import profiler

@profiler.benchmark(field='I/O')
def myfunc1(args):
    ...

@profiler.benchmark(field='Core computation')
def myfunc2(args):
    ...

@profiler.benchmark(field='Core computation')
def myfunc3(args):
    ...

@profiler.benchmark(field='Communication')
def myfunc4(args):
    ...
```

### End-to-end example

Try to run the test script provided on 4 processors:
```bash
mpirun -n 4 python tests/test.py
```
If necessary, change mpirun with your favourite shell script for running MPI applications.
You should see 4 log files created in your root folder of the form ` logproc_proc#_total.log `
Analyze those outputs using the analyzer:
```bash
python InsideMe/analyzer.py --output prof/
```
The analyzer will create a folder given by the output argument, store the logs in it
and produce a html file with plots shownig the time spent and memory consumption per processors.
Open the file in your browser, you should see:

![ScreenShot](https://github.com/JulienPeloton/LaFabrique/blob/master/additional_files/outputs.png)
![ScreenShot](https://github.com/JulienPeloton/LaFabrique/blob/master/additional_files/outputs.png)
![ScreenShot](https://github.com/JulienPeloton/LaFabrique/blob/master/additional_files/outputs.png)
![ScreenShot](https://github.com/JulienPeloton/LaFabrique/blob/master/additional_files/outputs.png)
![ScreenShot](https://github.com/JulienPeloton/LaFabrique/blob/master/additional_files/outputs.png)

### Problems known
* TBD

### License
GNU License (see the LICENSE file for details) covers all files
in the LaFabrique repository unless stated otherwise.
