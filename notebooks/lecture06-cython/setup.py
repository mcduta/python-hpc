from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy

setup (
    cmdclass = {"build_ext": build_ext},
    ext_modules = [
        Extension("matnorm",
                  ["./src/matnorm.pyx"],
                  extra_compile_args=['-fopenmp'],
                  extra_link_args=['-fopenmp'],
                  include_dirs = [numpy.get_include()])
    ]
)
