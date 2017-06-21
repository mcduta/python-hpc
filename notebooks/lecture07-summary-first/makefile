#======================================================================#
#                                                                      #
#      Makefile -- manages the building process of the                 #
#                  Python extension modules                            #
#                                                                      #
#======================================================================#

#
# ----- compiler options
#
# Fortran
F2PY     = f2py
FFLAGS   = -O2 -mavx -fPIC

# C
CC       = gcc
FC       = gfortran
CFLAGS   = -O2 -mavx -fPIC -std=c99

# library directory (mimics distutils installation)
LIBDIR   = $(PWD)/lib/python2.7/site-packages

#
# ----- rules for building the extension modules
#
default:		all

all:			c_stepper.so fortran_stepper.so

libdir:
			/bin/mkdir -p $(LIBDIR)

c_stepper.so:		src/c_stepper.c libdir
			$(CC) $(CFLAGS) -c src/c_stepper.c
			$(CC) -shared c_stepper.o -o $(LIBDIR)/c_stepper.so
			/bin/rm -f c_stepper.o

fortran_stepper.so:	src/fortran_stepper.f90 libdir
			$(F2PY)    src/fortran_stepper.f90 -h fortran_stepper.pyf
			$(F2PY) -c src/fortran_stepper.f90 -m fortran_stepper
			/bin/rm -f fortran_stepper.pyf
			/bin/mv fortran_stepper.so* $(LIBDIR)

clean:
			rm -f *_stepper*.so *_stepper*.pyf
			rm -fr *_stepper*.so.dSYM
			rm -f c_stepper.*
			rm -fr lib/

# end
