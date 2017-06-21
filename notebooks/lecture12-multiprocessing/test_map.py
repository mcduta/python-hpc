#!/usr/bin/env python

import multiprocessing
import numpy

def func (x):
    print x

if __name__ == '__main__':
    
    # some data
    x1 = numpy.arange(8)
    x2 = x1 + 100

    # open pool
    pool = multiprocessing.Pool (2)

    # MAP
    res = pool.map (func, x1)
    print "MAP FINISHED"

    # MAP_ASYNC
    res = pool.map_async (func, x2)
    print "MAP_ASYNC FINISHED"
    res.wait ()

    # close
    pool.close ()
    pool.join ()
