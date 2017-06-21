

#
# ===== simple Python implementation
#
import random
def numQuadrantHitsPython (numPoints):
    nhits = 0
    for n in range(numPoints):
        # generate random point inside the unit square (0,0), (0,1), (1,1), (1,0)
        x = random.random ()
        y = random.random ()
        # if inside unit circle, count a hit
        if (x*x + y*y) <= 1.0:
            nhits += 1
    return nhits


#
# ===== Numpy implementation
#
import numpy
def numQuadrantHitsNumpy (numPoints):

    x = numpy.random.uniform (low=0.0, high=1.0, size=numPoints)
    y = numpy.random.uniform (low=0.0, high=1.0, size=numPoints)
    r = numpy.sqrt (x*x + y*y)
    c = r [ r <= 1.0 ]
    return c.size


#
# ===== Numba implementation
#
from numba import jit
@jit
def numQuadrantHitsNumba (numPoints):
    nhits = 0
    for n in range(numPoints):
        # generate random point inside the unit square (0,0), (0,1), (1,1), (1,0)
        x = random.random ()
        y = random.random ()
        # if inside unit circle, count a hit
        if (x*x + y*y) <= 1.0:
            nhits += 1
    return nhits


#
# ===== Numpy implementation MODIFIED for multiprocessing
#
import numpy
def numQuadrantHitsNumpyMOD ((numPoints, seed)):

    numpy.random.seed (seed)
    x = numpy.random.uniform (low=0.0, high=1.0, size=numPoints)
    y = numpy.random.uniform (low=0.0, high=1.0, size=numPoints)
    r = numpy.sqrt (x*x + y*y)
    c = r [ r <= 1.0 ]
    return c.size


#
# ===== Multi-Processing implementation
#
import multiprocessing
def numQuadrantHitsMP (numPoints, numProcs):

    # number of points dealt with by each process
    numPointsProc = numPoints / numProcs

    # array with values to map to
    numPointsProcVec = [(numPointsProc, sd) for sd in range(numProcs)]

    # open a pool
    procPool = multiprocessing.Pool (numProcs)

    # asynchronous map
    rawNumHitsProc = procPool.map_async (numQuadrantHitsNumpyMOD, numPointsProcVec)
    rawNumHitsProc.wait () # not needed in fact

    # clean up pool
    procPool.close () # close task pool (cannot submit new tasks from here on)
    procPool.join ()  # __main__ must wait for all tasks to complete

    # retrieve results
    numHitsProcVec = rawNumHitsProc.get()

    # return result = sum of the list numHitsProcVec
    return sum(numHitsProcVec)


#
# ===== importable module: main does nothing
#

if __name__ == "__main__":
    import warnings
    warnings.simplefilter ("ignore")
