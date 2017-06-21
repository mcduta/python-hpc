#!/usr/bin/env python

import numpy
import sys
sys.path.append("./lib/python2.7/site-packages")
import matnorm as mn
import time

if __name__ == '__main__':

    #
    # --- test accuracy
    #
    # create matrix for tests
    n = 1024
    u = numpy.random.rand (n)
    # compute norm from linalg
    nrm0 = numpy.linalg.norm (u, 3)
    # compute norms using extension functions
    nrm1 = mn.p_norm (u, 3)
    nrm2 = mn.p_norm_types (u, n, 3)
    nrm3 = mn.p_norm_openmp (u, n, 3)
    nrm4 = mn.p_norm_openmp_better (u, n, 3)
    # check results
    print "norm is ", nrm0
    print "relative errors [%]", ([nrm1, nrm2, nrm3, nrm4] - nrm0) / nrm0*100.


    #
    # --- test speed
    #
    n = 25000000
    u = numpy.random.rand (n)

    print "\n performance ..."
    t = time.time(); numpy.linalg.norm (u, 3); t = time.time() - t;
    print "%50s %f" % ("linalg.norm: ", t)
    t = time.time(); mn.p_norm (u, 3); t = time.time() - t;
    print "%50s %f" % ("pure python code cythonized", t)
    t = time.time(); mn.p_norm_types (u, n, 3); t = time.time() - t;
    print "%50s %f" % ("adding C types", t)
    t = time.time(); mn.p_norm_types_better (u, n, 3); t = time.time() - t;
    print "%50s %f" % ("adding C functions", t)
    t = time.time(); mn.p_norm_openmp (u, n, 3, 1); t = time.time() - t;
    print "%50s %f" % ("using types + OpenMP (1 thread)", t)
    t = time.time(); mn.p_norm_openmp (u, n, 3, 2); t = time.time() - t;
    print "%50s %f" % ("using types + OpenMP (2 threads)", t)
    t = time.time(); mn.p_norm_openmp (u, n, 3, 4); t = time.time() - t;
    print "%50s %f" % ("using types + OpenMP (4 threads)", t)
    t = time.time(); mn.p_norm_openmp_better (u, n, 3, 4); t = time.time() - t;
    print "%50s %f" % ("using types + OpenMP + no checks (4 threads)", t)
