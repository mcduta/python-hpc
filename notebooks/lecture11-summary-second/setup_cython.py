#
# purpose: setup file to install the cython libraries
# usage:   python setup_cython.py install --prefix=$PWD
#

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup (
    name         = "heat_cython_stepper",
    description  = "Solution of 2D time-dependent heat equation",
    author       = "Mihai Duta",
    author_email = "mihai.duta@it.ox.ac.uk",
    cmdclass     = {"build_ext": build_ext},
    ext_modules  = [
        Extension ( "cython_stepper",
                    ["src/cython_stepper.pyx"],
                    extra_compile_args = ["-O3", "-mavx", "-fopenmp"],
                    extra_link_args = ["-fopenmp"] )
    ]
)

# end
