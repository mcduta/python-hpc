#
# purpose: setup file to install the compiled-language python libraries
# usage:   python setup_c_fortran.py config_fc --f90flags="-O3 -mavx -fopenmp" install --prefix=$PWD
#          python setup_c_fortran.py config_fc --fcompiler=intelem --f90flags="-O3 -mavx -fopenmp" install --prefix=$PWD
#

from numpy.distutils.core import Extension

c_stepper = Extension (name = "c_stepper",
                       sources = ["src/c_stepper.c"],
                       extra_compile_args = ["-O3 -mavx -std=c99 -fopenmp"],
                       extra_link_args = ["-fopenmp -lgomp"])

fortran_stepper = Extension (name = "fortran_stepper",
                             sources = ["src/fortran_stepper.f90"],
                             extra_compile_args = ["-O3 -mavx -fopenmp"],
                             extra_link_args = ["-fopenmp -lgomp"])


if __name__ == "__main__":
    from numpy.distutils.core import setup
    setup ( name = "heat_c_fortran_stepper",
            description  = "Solution of 2D time-dependent heat equation",
            author       = "Mihai Duta",
            author_email = "mihai.duta@it.ox.ac.uk",
            ext_modules  = [c_stepper, fortran_stepper]
          )

# end
