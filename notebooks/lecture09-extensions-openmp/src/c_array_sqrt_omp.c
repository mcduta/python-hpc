# include <math.h>
# ifdef _OPENMP
# include <omp.h>
# endif

void array_sqrt (const int n,
                 double *restrict a_in,
                 double *restrict a_out,
                 const int nt)
{

  int i;

# ifdef _OPENMP
  // set the number of threads to input nt
  omp_set_num_threads(nt);
  // schedule a parallel loop
  # pragma omp parallel for \
    default (none)          \
    shared (a_in,a_out)     \
    firstprivate (n)        \
    private (i)
# endif
  for (i = 0; i < n; i++) {
    a_out[i] = sqrt (a_in[i]);
  }
}
