#!/usr/bin/env python
# Copyright (C) 2017 Peloton
"""Distutils based setup script for InsideMe.

For the easiest installation just type the command (you'll probably need
root privileges for that):

    python setup.py install

This will install the library in the default location. For instructions on
how to customize the install procedure read the output of:

    python setup.py --help install

In addition, there are some other commands:

    python setup.py clean -> will clean all trash (*.pyc and stuff)
    python setup.py test  -> will run the complete test suite
    python setup.py bench -> will run the complete benchmark suite
    python setup.py audit -> will run pyflakes checker on source code

To get a full list of avaiable commands, read the output of:

    python setup.py --help-commands
"""
from setuptools import setup

if __name__ == "__main__":
    setup(name='InsideMe',
        version='0.2.1',
        author='Julien Peloton',
        author_email='j.peloton@sussex.ac.uk',
        url='https://github.com/JulienPeloton/InsideMe',
        download_url='https://github.com/JulienPeloton/InsideMe/archive/0.2.1.zip',
        install_requires=['mpi4py'],
        packages=['InsideMe'],
        description='Python module for monitoring memory consumption \
        and duration of python codes. Work for both serial codes and \
        parallel programming (MPI).',
        license='GPL-3.0',
        long_description='See https://github.com/JulienPeloton/InsideMe',
        keywords=['profiling', 'MPI', 'testing'],
        classifiers=[
            "Programming Language :: Python :: 2",
            'Programming Language :: Python :: 2.7'],)
