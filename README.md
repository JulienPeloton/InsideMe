ProfileIt
==

#### The package
Simple python module for monitoring memory consumption and time spent.
Especially relevant when using MPI.
It does include
* Simple routines that can be used as decorators to monitor memory consumption of functions and classes
*

It does not include
*

### Before starting
This code has the following dependencies (see the travis install section):
* numpy, pylab, scipy, etc (required)
* mpi4py (optional - for parallel computing)

## Installation
We provide a setup.py for the installation. Just run:
```bash
python setup.py install
```
Make sure you have correct permissions (otherwise just add --user).
You can also directly use the code by updating manually your PYTHONPATH.
Just add in your bashrc:
```bash
ProfileItPATH=/path/to/the/package
export PYTHONPATH=$PYTHONPATH:$ProfileItPATH
```

### Usage

```python
Mettre à jour!
```
You should see then


### Problems known
*

### TODO list
* GUI interface! (seems quite tricky though)
* line-by-line (how?)
* json interface: dump everything in log.
Analyze log using counter and then output it (howmanypeoplearound)

### License
GNU License (see the LICENSE file for details) covers all files
in the LaFabrique repository unless stated otherwise.
