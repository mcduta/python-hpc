#!/usr/bin/env python


"""Advanced Research Computing -- Python for High Performance Computing

This script compares different ways of implementing an iterative
procedure to solve the 2D heat equation. 

The Software
------------
The python code provides a general guideline to using Python for High
Performance Computing and provides a simple means to compare the
computational time taken by the different approaches.

The script compares functions implemented in

     * pure Python
     * NumPy
     * weave.blitz
     * weave.inline
     * numba
     * Fortran (OpenMP)
     * C (OpenMP)
     * Cython

The modules are built (using gcc and gfortran) with the command

     make all



The Maths
---------
The heat equation is the Initial Value Boundary Problem (IVBP)
Partial Differential Equation

      2      2      2
     d u    d u    d u
     ---2 = ---2 + ---2
     d t    d x    d y

whose solution u(x, y, t) is sought.

For this exercise, the problem is defined on the unit square

     0 <= x, y, z <= 1

The boundary conditions are

     u(0, y, t) = 0
     u(x, 0, t) = 0

and the initial value is

     u(x, y, 0) = sin(pi*y) * sin(pi*z)

With the above, the analytic solution is

     u(x, y, t) = sin(pi*y) * sin(pi*z) * exp(-2*pi**2 * t)


History
-------
Sep 2004: original version by Prabhu Ramachandran
          http://scipy-cookbook.readthedocs.io/items/PerformancePython.html
Sep 2016: modifications by Mihai Duta


License
-------
BSD
Creative Commons(?)

Last modified: Feb 2017

"""


# ======================================================================
#
# ----- imports
#
# ======================================================================
#
import numpy
import sys
import time


# ======================================================================
#
# ----- grid class
#
# ======================================================================
#
class grid:
    """
    grid -- class to store the data of the computational grid:
            number of grid points, grid spacing and solution
    """
    def __init__ (self, nx=64, ny=64, xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.0):
        # store parameters
        self.nx, self.ny = nx, ny
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        # grid x, y data
        x, y = self.coords ()
        # uo stores the previous-step solution (including initial values)
        self.uo  = numpy.sin (numpy.pi*x) * numpy.sin (numpy.pi*y)
        # Dirichlet boundary values
        self.uo[0 , :] = 0
        self.uo[-1, :] = 0
        self.uo[: , 0] = 0
        self.uo[: ,-1] = 0
        # u stores current-step solution
        self.u = self.uo.copy ()


    def coords (self):
        """
        computes the coordinates x, y in numpy.meshgrid format starting from self
        """
        nx, ny = self.nx, self.ny
        xx = numpy.linspace (self.xmin, self.xmax, nx)
        yy = numpy.linspace (self.ymin, self.ymax, ny)
        x, y = numpy.meshgrid (xx, yy)
        return x, y


    def error (self, numIters=0, nu=0.25):
        """
        computes L2-norm absolute error for the solution
        (this requires that self.u and self.uo must be appropriately setup)
        """
        # pi
        pi = numpy.pi
        # grid x, y data
        x, y = self.coords ()
        # grid spacing
        dx = float (self.xmax - self.xmin) / (self.nx - 1)
        # time variable
        t = numIters*nu*dx*dx
        # analytic solution at time value
        self.uo = numpy.sin (pi*x) * numpy.sin (pi*y) * numpy.exp(-2.0*pi*pi*t)
        # get difference between analytic and computed solution
        v = ( (self.u - self.uo) / (self.uo + 1.e-14) ).flat
        return numpy.sqrt (numpy.dot (v,v))


    def plot (self):
        """
        produces a 3d plot of the solution
        """
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        x, y = self.coords ()
        fig = plt.figure ()
        ax = fig.gca (projection='3d')
        surf = ax.plot_surface (x, y, self.u)
        plt.show ()
        plt.draw ()


# ======================================================================
#
# ----- solver class
#
# ======================================================================
#
class solution:
    """
    solution -- class to implement an explicit time-stepping solution for
                the time-dependent 2D heat equation
    """
    def __init__ (self, grid, stepper = "numpy", nu=0.25):
        # initialise grid data with argument
        self.grid = grid
        # initialise stepper with argument
        self.setStepper (stepper)
        # scheme parameter (<=0.25 for stability)
        self.nu = nu
        # Fortran trickery (cast solution and copy to Fortran storage)
        if (stepper == "fortran"):
            self.grid.uo =  numpy.array (self.grid.uo, order="Fortran")
            self.grid.u  =  numpy.ndarray (shape=self.grid.uo.shape,
                                           dtype=self.grid.uo.dtype,
                                           order="Fortran")


    def setStepper (self, stepper="numpy"):
        """
        Set stepper used by timeStep()
        """
        if   stepper == "python":
            self.stepper = self.pythonStepper
        elif stepper == "numpy":
            self.stepper = self.numpyStepper
        elif stepper == "fortran":
            self.stepper = self.fortranStepper
        elif stepper == "ctypes":
            self.stepper = self.cStepper
        elif stepper == "numba":
            self.stepper = self.numbaStepper
        elif stepper == "blitz":
            self.stepper = self.blitzStepper
        elif stepper == "inline":
            self.stepper = self.inlineStepper
        elif stepper == "cython":
            self.stepper = self.cythonStepper
        else:
            self.stepper = self.numpyStepper


    def timeStep (self, numIters=0):
        """
        Advances the solution numIters timesteps using stepper set by setStepper()
        """
        # number of grid points in x, y
        nx, ny = self.grid.u.shape
        # solution vectors
        u  = self.grid.u
        uo = self.grid.uo
        # scheme parameter (<=0.25 for stability)
        nu = self.nu
        # time-step numIters times
        for t in range (1, numIters):
            # apply numerical scheme
            self.stepper (nx,ny, u,uo, nu)
            # swap pointers
            u, uo = uo, u


    def pythonStepper (self, nx,ny, u,uo, nu):
        """ time-steps implemented using straight python array indexing"""
        # apply numerical scheme (one time-step)
        for i in range(1, nx-1):
            for j in range(1, ny-1):
                u[i,j] = uo[i,j] + ( nu * ( uo [i-1, j] + uo [i+1, j] +
                                            uo [i, j-1] + uo [i, j+1]
                                            - 4.0 * uo [i,j] ) )


    def numpyStepper (self, nx,ny, u,uo, nu):
        """ time-steps implemented using numpy array indexing"""
        # apply numerical scheme (one time-step)
        u[1:-1, 1:-1] = uo[1:-1, 1:-1] + ( nu * ( uo [0:-2, 1:-1] + uo [2:, 1:-1] +
                                                  uo [1:-1, 0:-2] + uo [1:-1, 2:]
                                                  - 4.0 * uo [1:-1, 1:-1] ) )


    def numbaStepper (self, nx,ny, u,uo, nu):
        """ time-steps implemented using straight python array indexing dispatched via JIT compiling"""
        # apply numerical scheme (one time-step)
        numbaStepperJIT (nx,ny, u,uo, nu)


    def blitzStepper (self, nx,ny, u,uo, nu):
        """ time-steps implemented using numpy expression dispatched via blitz"""
        from scipy import weave
        # define expression (same one as for numpyStepper)
        expr = "u[1:-1, 1:-1] = uo[1:-1, 1:-1] + ( nu * ( uo [0:-2, 1:-1] + uo [2:, 1:-1] + " \
               "                                   uo [1:-1, 0:-2] + uo [1:-1, 2:]" \
               "                                   - 4.0 * uo [1:-1, 1:-1] ) )"
        weave.blitz (expr, check_size=0)


    def inlineStepper (self, nx,ny, u,uo, nu):
        """ time-steps implemented using C code dispatched via weave"""
        from scipy import weave
        from scipy.weave import converters
        # define code (same one as for C code cStepper
        #  * cannot use u[i][j]
        #  * instead use u[k], with k = i*ny + j
        code = """
               int i,j;
               int k,kn,ks,kw,ke;
               for (i=1; i<nx-1; i++) {
                 for (j=1; j<ny-1; j++) {
                   k    = i*ny + j;
                   kn   = k + nx;
                   ks   = k - nx;
                   ke   = k + 1;
                   kw   = k - 1;
                   u[k] = uo[k]
                        + nu * ( uo[kn] + uo[ks]
                               + uo[ke] + uo[kw]
                               - 4.0 * uo[k]);
                 }
               }
               """
        # compiler keyword only needed on windows with MSVC installed
        err = weave.inline (code,
                            ["nx","ny","u","uo","nu"])


    def fortranStepper (self, nx,ny, u,uo, nu):
        """ time-steps implemented using Fortran code"""
        import sys
        sys.path.append("./lib/python2.7/site-packages")

        import fortran_stepper
        # apply numerical scheme (one time-step)
        fortran_stepper.timestep (nu, uo,u)


    def cStepper (self, nx,ny, u,uo, nu):
        """ time-steps implemented using C code"""
        import ctypes
        from numpy.ctypeslib import ndpointer

        c_stepper = ctypes.cdll.LoadLibrary("./lib/python2.7/site-packages/c_stepper.so")
        c_stepper.timestep.restype = None
        c_stepper.timestep.argtypes = [ctypes.c_double,
                                       ctypes.c_int,
                                       ctypes.c_int,
                                       ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                                       ndpointer(ctypes.c_double, flags="C_CONTIGUOUS")]

        # apply numerical scheme (one time-step)
        c_stepper.timestep (nu, nx,ny, uo,u)


    def cythonStepper (self, nx,ny, u,uo, nu):
        """ time-steps implemented using cython"""

        import sys
        sys.path.append("./lib/python2.7/site-packages")

        import cython_stepper
        # apply numerical scheme (one time-step)
        cython_stepper.timestep (uo,u, nu)


# ======================================================================
#
# ----- numba stepper (defined separately)
#
# ======================================================================
#
from numba import jit
# numba / JIT compiler decorator
@jit
def numbaStepperJIT (nx,ny, u,uo, nu):
    # same code as the straight python stepper
    for i in range(1, nx-1):
        for j in range(1, ny-1):
            u[i,j] = uo[i,j] + ( nu * ( uo [i-1, j] + uo [i+1, j] +
                                        uo [i, j-1] + uo [i, j+1]
                                        - 4.0 * uo [i,j] ) )




# ======================================================================
#
# ----- main
#
# ======================================================================
#
def main (numNodes=1000, numIters=100):

    # iterators implementations available
    stepper = "python"

    # message
    print " computing %d iterations on a %dx%d grid"%(numIters, numNodes, numNodes)

    # stepper implementations to try
    stepperTypeList = [
#       "python",
        "numpy",
#        "numba",
#        "blitz",
#        "inline",
        "fortran",
        "ctypes",
        "cython"
    ]

    # try all steppers
    for stepperType in stepperTypeList:
        # initialise grid
        g = grid (numNodes, numNodes)
        # initialise solution
        s = solution (g, stepper=stepperType)
        # solve
        t = time.time ()
        s.timeStep ()
        s.timeStep (numIters=numIters)
        t = time.time () - t
        # compute error
        err = g.error(numIters=numIters, nu=s.nu)
        # report
        print " stepper %s, %d iterations, %f seconds, %f rel error" % (stepperType, numIters, t, err)


if __name__ == "__main__":
    # parse arguments
    import argparse
    parser = argparse.ArgumentParser (description="demonstrator of python performance using compiled languages")
    parser.add_argument ("numNodes", metavar="n", type=int, default=400, help="grid size")
    parser.add_argument ("numIters", metavar="i", type=int, default=100, help="number of iterations")
    args = parser.parse_args ()
    # start main ()
    main (numNodes=args.numNodes, numIters=args.numIters)
