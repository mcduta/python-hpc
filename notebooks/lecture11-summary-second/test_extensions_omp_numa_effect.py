# -------------------------------------------------------------------- #
#                                                                      #
#     tester_omp.py -- Tester for the Fortran and C python             #
#                      extensions parallelised using OpenMP.           #
#                                                                      #
#                      With a fixed number of OpenMP threads,          #
#                      the test measures time for both Fortran         #
#                      and C extension with                            #
#                                                                      #
#                         * data arrays initialised from Python        #
#                         * data arrays initialised by OpenMP          #
#                           threaded Fortran and C code                #
#                                                                      #
#                      The test illustrates the need to initialise     #
#                      data in a NUMA aware mode in order to           #
#                      obtain good threaded extension performance.     #
#                                                                      #
# -------------------------------------------------------------------- #


# imports
import numpy
import sys
import time
import os


# sizes / parameters
nx = 10000
ny = nx
nu = 0.25

# ancillary vars
xx = numpy.linspace (0.0, 1.0, nx)
yy = numpy.linspace (0.0, 1.0, ny)
x, y = numpy.meshgrid (xx, yy)

# main working 2D arrays
uo = numpy.sin (numpy.pi*x) * numpy.sin (numpy.pi*y)
u  = numpy.zeros(uo.shape)


#
# === number of test repetitions
#
nrep = 5


#
# ===== relative extension path
#
ext_path = "./lib/python2.7/site-packages"


#
# ===== C extension
#
import ctypes
from numpy.ctypeslib import ndpointer

lib = ctypes.cdll.LoadLibrary(ext_path + "/" + "c_stepper.so")

lib.timestep.restype = None
lib.timestep.argtypes = [ctypes.c_double,
                         ctypes.c_int,
                         ctypes.c_int,
                         ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                         ndpointer(ctypes.c_double, flags="C_CONTIGUOUS")]

lib.initialise.restype = None
lib.initialise.argtypes = [ctypes.c_int,
                         ctypes.c_int,
                         ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                         ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                         ctypes.c_double, ctypes.c_double,
                         ctypes.c_double, ctypes.c_double
                         ]

# C extensions, python initialisation
tc1 = time.time ()
for nr in range(nrep):
    lib.timestep (nu, nx,ny, uo,u)
tc1 = time.time () - tc1
tc1/= nrep

# C extensions, C initialisation
lib.initialise (nx,ny, uo,u, 0.0,1.0, 0.0,1.0)

tc2 = time.time ()
for nr in range(nrep):
    lib.timestep (nu, nx,ny, uo,u)
tc2 = time.time () - tc2
tc2/= nrep


#
# ===== Fortran extension
uo =  numpy.array (uo, order="Fortran")
u  =  numpy.array (u, order="Fortran")

import sys
sys.path.append (ext_path)
import fortran_stepper

# Fortran extensions, python initialisation
tf1 = time.time ()
for nr in range(nrep):
    fortran_stepper.timestep (nu, uo,u)
tf1 = time.time () - tf1
tf1/= nrep

# Fortran extensions, Fortran initialisation
fortran_stepper.initialise (0.0,1.0, 0.0,1.0, uo,u)

tf2 = time.time ()
for nr in range(nrep):
    fortran_stepper.timestep (nu, uo,u)
tf2 = time.time () - tf2
tf2/= nrep


#
# ===== report
#
#print '    C         C        Fortran      Fortran'
#print ' (python     (C        (python     (Fortran'
#print '   init)     init)      init)        init)'
#print '     s e c'
#print ' -----------------------------------------'
#print '  %s     %.3f      %.3f      %.3f       %.3f ' % (os.environ['OMP_NUM_THREADS'], tc1, tc2, tf1, tf2)
print '  %s     %.3f      %.3f      %.3f       %.3f ' % (os.environ['OMP_NUM_THREADS'], tc1, tc2, tf1, tf2)



# end
