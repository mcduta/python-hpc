/*
  file:       c_stepper.c
  purpose:    create python library
  implements: a time step for the explicit FTCS scheme to solve
              the time-dependent heat equation
  author:     Mihai Duta,
              Advanced Research Computing,
              University of Oxford
*/

# include <math.h>

void timestep ( const double nu,
                const int nx,const int ny,
                double uo[nx][ny],double u[nx][ny] )
{

  int i,j;

  // finite difference scheme
# ifdef _OPENMP
# pragma omp parallel for      \
  default (none)               \
  shared (u,uo)                \
  private (i,j)                \
  firstprivate (nx,ny, nu)     \
  schedule (static)
# endif
  // finite difference scheme
  for (i=1; i<nx-1; i++) {
    for (j=1; j<ny-1; j++) {
      u[i][j] = uo[i][j]
              + nu * ( uo [i-1][j] + uo [i+1][j]
                     + uo [i][j-1] + uo [i][j+1]
                     - 4.0 * uo [i][j] );
	}
  }
}


// ------------------------------------------------------------------- //
//                                                                     //
// ------------------------------------------------------------------- //
void initialise (const int nx,const int ny,
                 double uo[nx][ny],double u[nx][ny],
                 const double xmin, const double xmax,
                 const double ymin, const double ymax)
{
  int    i,j;
  double dx,dy;

# define PI 3.141592653589793

  // interval spacing
  dx = (xmax - xmin) / ((double) nx-1);
  dy = (ymax - ymin) / ((double) ny-1);

  // finite difference scheme
# ifdef _OPENMP
# pragma omp parallel for     \
  default  (none)             \
  shared (u,uo)               \
  private (i,j)               \
  firstprivate (nx,ny, dx,dy) \
  schedule (static)
# endif
  for (i=0; i<nx; i++) {
    for (j=0; j<ny; j++) {
      uo[i][j] = sin ( ((double) i) * dx * PI ) * sin ( ((double) j) * dy * PI );
      u[i][j]  = 0.0;
    }
  }

}
