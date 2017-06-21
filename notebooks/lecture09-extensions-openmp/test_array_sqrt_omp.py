#!/usr/bin/env python

import numpy
import time
import os


#
# === create array space
#
N = 100000000

a_in  = numpy.random.rand (N)
a_out = numpy.random.rand (N)


#
# === number of repetitions
#
nrep = 5


#
# === relative path to extensions (standard)
#
ext_path = "./lib/python2.7/site-packages"


#
# === test C extension
#
import ctypes
from numpy.ctypeslib import ndpointer

c_array_sqrt_omp = ctypes.cdll.LoadLibrary (ext_path + "/" + "c_array_sqrt_omp.so")
c_array_sqrt_omp.array_sqrt.restype = None
c_array_sqrt_omp.array_sqrt.argtypes = [ ctypes.c_int,
                                         ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                                         ndpointer(ctypes.c_double, flags="C_CONTIGUOUS") ]

print " === C extensions"
for nthreads in [1, 2, 4]:
    times = []
    for irep in range(nrep):
        t = time.time ()
        c_array_sqrt_omp.array_sqrt (N, a_in, a_out, nthreads)
        t = time.time () - t
        times.append(t)

    print " %d threads, %f seconds" % (nthreads, sum(times) / float(nrep))

#
# === test Fortran extension
#
import sys
sys.path.append (ext_path)
import f_array_sqrt_omp

print " === F90 extensions"
for nthreads in [1, 2, 4]:
    times = []
    for irep in range(nrep):
        t = time.time ()
        a_out = f_array_sqrt_omp.array_sqrt (a_in, nthreads)
        t = time.time () - t
        times.append(t)

    print " %d threads, %f seconds" % (nthreads, sum(times) / float(nrep))
