#!/usr/bin/env python


"""Advanced Research Computing -- Python for High Performance Computing

This script illustrates the use of the multiprocessing python package
to parallelise the computational workload in the case of trivially
parallel tasks.  The workload in this case is a Monte -- Carlo type
simulation.


The Code
--------
This code provides an example of approaching trivial parallelism in
python using the multiprocessing python package.  The workload is to
compute a large number of numerical solutions, each of which depends
on a random parameter that is described by a probability distribution.
This large number of solutions are divided into independent groups
(tasks) that are carried out concurrently by different processes.


The Maths
---------

The result sought solved is finding a statistical distribution for the
terminal velocity of a free-falling object subject only to gravity and
air resistance.

The equation to solve is

m*a = m*g - c*v

where

     * m is the constant mass of the object
     * a is acceleration
     * v is velocity
     * c is a constant describing the air resistance
       (proportional to velocity)

c is dependant on air properties (such as air density) and its values
are described by a probability distribution.

Taking height y as the variable, then
         .     ..
     v = y, a = y 

and the boundary conditions are
     .
     y(0) = y(0) = 0

(body falls from rest).


Numerical Solution
------------------
The 2nd order ODE is recast as the 1st order system of ODEs

     dy
     -- = v
     dt

     dv
     -- = -c/m*v + g
     dt

with initial conditions y(0) = v(0) = 0.



History
-------
Sep 2016: created and developed by Mihai Duta


License
-------
BSD
Creative Commons(?)

Last modified: Dec, 2016

"""


# ======================================================================
#
# ----- using numpy and scipy
#
# ======================================================================
#
import numpy
import multiprocessing
import time
from scipy.integrate import odeint
import sys


# ======================================================================
#
# ----- workaround for pickled methods (thanks to stackoverflow.com)
#
# ======================================================================
#
# * problem 1: multiprocessing must pickle objects to pass them among processes
# * problem 2: bound methods are not picklable
# * workaround: add the infrastructure to allow such methods to be pickled,
#               by registering it with the copy_reg standard library method
#
import copy_reg
import types

def _pickle_method (m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle (types.MethodType, _pickle_method)


# ======================================================================
#
# ----- ODE problem class
#
# ======================================================================
#
class fallingBodyProblem:
    """
    fallingBodyProblem -- class to store data and define a solution method
                          for the problem of a falling object subject to
                          gravity and air resistance
    """
    def __init__ (self, mass, gravity, resistance):
        self.mass       = mass
        self.gravity    = gravity
        self.resistance = resistance

    def ode (self, stateVector, time):
        mass       = self.mass
        gravity    = self.gravity
        resistance = self.resistance

        position, velocity = stateVector

        stateVectorTimeDerivative = [ velocity, - resistance / mass * velocity + gravity ]

        return stateVectorTimeDerivative

    def solution (self, initPosition=0.0, initVelocity=0.0, initTime=0.0, finalTime=100.0, numTimePoints=1000):
        initialStateVector = [initPosition, initVelocity]
        timePoints         = numpy.linspace (initTime, finalTime, numTimePoints)
        stateVectorHistory = odeint (self.ode, initialStateVector, timePoints, args=(), atol = 1.0e-8, rtol = 1.0e-6)
        return timePoints, stateVectorHistory


# ======================================================================
#
# ----- ODE problem class
#
# ======================================================================
#
class fallingBodyStats:
    """
    fallingBodyStats -- class to generate statistics on the solution
                        to the falling body problem with air resistance
                        defined by a normal random variable
    """
    def __init__ (self, mass, gravity, initPosition, initVelocity, initTime, finalTime, numTimePoints, resistanceMean, resistanceVar, sampleSize):
        # store values
        self.mass           = mass
        self.gravity        = gravity
        self.initPosition   = initPosition
        self.initVelocity   = initVelocity
        self.initTime       = initTime
        self.finalTime      = finalTime
        self.numTimePoints  = numTimePoints
        self.resistanceMean = resistanceMean
        self.resistanceVar  = resistanceVar
        self.sampleSize     = sampleSize


    def solutionWrapper (self, resistance):
        """
        solutionWrapper -- generates a single terminal velocity solution
                           from an input single air resistance value
        """
        # set problem
        body = fallingBodyProblem (self.mass, self.gravity, resistance)
        # solve
        timePoints, stateVectorHistory = body.solution (self.initPosition, self.initVelocity, self.initTime, self.finalTime, self.numTimePoints)
        # return final (last) solution value
        return stateVectorHistory [-1,1]


    def solutionStats (self):
        """
        solutionStats -- generates terminal velocity statistics from a
                         distribution of air resistance values
        """
        # sample of air resistance values
        resistanceValues = self.resistanceMean + self.resistanceVar * numpy.random.randn (self.sampleSize)

        # vector to store final velocities
        finalVelocities = numpy.zeros (self.sampleSize)
        counterVelocities = 0

        # run across the entire sample
        for resistance in resistanceValues:
            # set problem
            finalVelocities [counterVelocities] = self.solutionWrapper (resistance)
            counterVelocities += 1

        return finalVelocities


    def solutionStatsMultiProcessing (self, numProcs=2):
        """
        solutionStatsMultiProcessing -- generates terminal velocity statistics from a
                                        distribution of air resistance values
                                        (parallel processing using the multiprocessing module)
        """
        # sample of air resistance values
        resistanceValues = self.resistanceMean + self.resistanceVar * numpy.random.randn (self.sampleSize)

        # vector to store final velocities
        finalVelocities = numpy.zeros (self.sampleSize)
        counterVelocities = 0

        # open a pool
        procPool = multiprocessing.Pool (numProcs)

        rawResults = procPool.map_async( self.solutionWrapper, resistanceValues )
        rawResults.wait () # not really needed
        finalVelocities = rawResults.get () # get() is blocking

        # clean up pool
        procPool.close () # close task pool (cannot submit new tasks from here on)
        procPool.join ()  # __main__ must wait for all tasks to complete

        return finalVelocities


# ======================================================================
#
# ----- main
#
# ======================================================================
#
if __name__ == "__main__":

    # default number of processors (on this machine)
    numProcsDefault = multiprocessing.cpu_count()

    # parse arguments
    import argparse
    parser = argparse.ArgumentParser (description="demonstrator of python multiprocessing package")
    parser.add_argument ("resistanceMean", metavar="resistanceMean", type=float, default=0.1,   help="mean value of air resistance coefficient")
    parser.add_argument ("resistanceVar",  metavar="resistanceVar",  type=float, default=0.01,  help="variance of air resistance coefficient")
    parser.add_argument ("finalTime",      metavar="finalTime",      type=float, default=100.0, help="final time")
    parser.add_argument ("numTimePoints",  metavar="numTimePoints",  type=int,   default=1000,  help="number of time points")
    parser.add_argument ("sampleSize",     metavar="sampleSize",     type=int,   default=1000,  help="number of values in the sample")
    parser.add_argument ("numProcs",       metavar="numProcs",       type=int,   default=numProcsDefault, help="number of cores to use, default is " + str(numProcsDefault) )
    args = parser.parse_args ()

    if args.resistanceMean < 0.0 or args.resistanceVar < 0.0:
        sys.exit(" *** error: air resistance mean and variance must be positive")

    if args.finalTime < 0.0:
        sys.exit(" *** error: final time must be positive")


    #
    # --- generate statistics in serial
    #

    # generate body stats object
    bodyStats = fallingBodyStats (mass           = 1.02,
                                  gravity        = 9.81,
                                  initPosition   = 0.0,
                                  initVelocity   = 0.0,
                                  initTime       = 0.0,
                                  finalTime      = args.finalTime,
                                  numTimePoints  = args.numTimePoints,
                                  resistanceMean = args.resistanceMean,
                                  resistanceVar  = args.resistanceVar,
                                  sampleSize     = args.sampleSize)

    # generate stats
    print " serial implementation"
    tSerial = time.time ()
    finalVelocities = bodyStats.solutionStats ()
    tSerial = time.time () - tSerial
    print " serial stats time = %f" % (tSerial)

    # generate stats in parallel
    print " multiprocessing implementation using %i processes" % (args.numProcs)
    tPar = time.time ()
    finalVelocitiesPar = bodyStats.solutionStatsMultiProcessing (args.numProcs)
    tPar = time.time () - tPar
    print " parallel stats time = %f" % (tPar)


    #
    # --- build a histogram of results
    #
    import matplotlib.mlab as mlab
    import matplotlib.pyplot as plt

    # histogram
    plt.figure (1)

    #
    # ... histogram of MC data in serial
    plt.subplot (211)
    numBins    = max(10, args.sampleSize / 100)
    n, bins, patches = plt.hist (finalVelocities, numBins, normed='false', facecolor='lightBlue', alpha=0.75)
    plt.xlabel ("Terminal Velocities")
    plt.ylabel ("Probability")
    plt.title ("Serial MC")
    plt.grid (True)
    # velocities min/max
    finalVelocitiesMin = finalVelocities.min ()
    finalVelocitiesMax = finalVelocities.max ()

    #
    # ... histogram of MC data in parallel
    plt.subplot (212)
    numBinsPar = max(10, args.sampleSize / 100)
    n, bins, patches = plt.hist (finalVelocitiesPar, numBinsPar, normed='false', facecolor='lightBlue', alpha=0.75)
    plt.xlabel ("Terminal Velocities")
    plt.ylabel ("Probability")
    plt.title ("Parallel MC")
    plt.grid (True)

    # velocities min/max
    finalVelocitiesMin = min (finalVelocitiesMin, finalVelocities.min ())
    finalVelocitiesMax = max (finalVelocitiesMax, finalVelocities.max ())

    #
    # ... make sure the histograms have the same x-axis
    plt.subplot (211)
    axes = plt.gca()
    axes.set_xlim ([ finalVelocitiesMin, finalVelocitiesMax])
    axes.set_ylim ([ 0.0, 0.02])
    plt.subplot (212)
    axes = plt.gca()
    axes.set_xlim ([ finalVelocitiesMin, finalVelocitiesMax])
    axes.set_ylim ([ 0.0, 0.02])

    plt.show ()
