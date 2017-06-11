InsideMe [![Build Status](https://travis-ci.org/JulienPeloton/InsideMe.svg?branch=master)](https://travis-ci.org/JulienPeloton/InsideMe)
==

### The package
InsideMe is a simple yet effective python module for monitoring
memory consumption and duration of python codes.
Work for both serial codes and parallel programming (MPI).

### Before starting
This code has the following dependencies (see the travis install section):
* numpy, matplotlib (required)
* mpi4py (optional - for parallel computing)

### Installation
You can easily install the package using pip
```bash
pip install InsideMe
```

Otherwise, you can clone the repo from the github repository and
use the setup.py for the installation. Just run:
```bash
python setup.py install
```
Make sure you have correct permissions (otherwise just add --user).
You can also directly use the code by updating manually your PYTHONPATH.
Just add in your bashrc:
```bash
InsideMePATH=/path/to/the/package
export PYTHONPATH=$PYTHONPATH:$InsideMePATH:$InsideMePATH/InsideMe
```

### How to use it

The profiling of a code is done using decorators.
Typically, if you want to monitor the time spent inside a
function and its memory usage, simply add a decorator
```python
## content of toto.py
from InsideMe import profiler

@profiler.benchmark
def myfunc(args):
    ...
```
The profiler will collect informations during the execution of the program,
and store it on a log file. By default, the profiler will use the name of
the function for future reference. It is often the case that one wants to
group functions under categories. You can specify this by directly passing
category (field) as parameter to the decorator:

```python
## content of toto.py
from InsideMe import profiler

@profiler.benchmark(field='something')
def myfunc1(args):
    ...

@profiler.benchmark(field='something else')
def myfunc2(args):
    ...

@profiler.benchmark(field='something else')
def myfunc3(args):
    ...

@profiler.benchmark(field='something else else')
def myfunc4(args):
    ...
```

Once your run is done, analyze the logs using the analyzer:

```bash
AnalyzeMe --output <folder>
```

The analyzer will create a folder given by the output argument, store the logs in it
and produce a html file with plots showing the duration and memory consumption per processors.

### End-to-end example

Try to run the test script provided on say 4 processors:
```bash
mpirun -n 4 python tests/test.py
```
If necessary, change mpirun with your favourite shell script for running MPI applications.
You should see 4 log files created in your root folder of the form ` logproc_proc#_total.log `
Analyze those outputs using the analyzer:
```bash
AnalyzeMe --output prof/
```
Open the html file produced in your browser, you should see something like (interactive plots)

<img src="tests/summary.png" alt="Drawing" style="width: 600px;"/>
<img src="tests/proc0.png" alt="Drawing" style="width: 600px;"/>
<img src="tests/proc1.png" alt="Drawing" style="width: 600px;"/>
<img src="tests/proc2.png" alt="Drawing" style="width: 600px;"/>
<img src="tests/proc3.png" alt="Drawing" style="width: 600px;"/>

### Future development
* TBD

### Problems known (and hopefully fixed soon!)
* New logs with same output are not analyzed

### License
GNU License (see the LICENSE file for details) covers all files
in AnalyzeMe repository unless stated otherwise.
