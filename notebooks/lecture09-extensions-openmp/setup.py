#
# purpose: setup file to install the compiled-language python libraries
# usage:   python setup.py config_fc --f90flags="-O2 -fopenmp" install --prefix=$PWD
#

from numpy.distutils.core import Extension

c_array_sqrt = Extension (name = "c_array_sqrt_omp",
                          sources = ["./src/c_array_sqrt_omp.c"],
                          extra_compile_args = ["-O2 -ffast-math -std=c99 -fopenmp"],
                          extra_link_args = ["-lgomp"])

f_array_sqrt = Extension (name = "f_array_sqrt_omp",
                          sources = ["./src/f_array_sqrt_omp.f90"],
                          extra_compile_args = ["-O2 -ffast-math -fopenmp"],
                          extra_link_args = ["-lgomp"])

if __name__ == "__main__":
    from numpy.distutils.core import setup
    setup ( name = "array-sqrt-openmp",
            description  = "Illustration of Python extensions using OpenMP",
            author       = "Mihai Duta",
            author_email = "mihai.duta@it.ox.ac.uk",
            ext_modules  = [c_array_sqrt, f_array_sqrt]
          )

# end
