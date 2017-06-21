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

    # APPLY
    res = [ pool.apply (func, args = (xi, )) for xi in x1 ]
    print "APPLY FINISHED"

    # APPLY_ASYNC
    out = [ pool.apply_async (func, args = (xi, )) for xi in x2 ]
    print "APPLY_ASYNC FINISHED"

    # close
    pool.close ()
    pool.join ()
