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
  for (i=1; i<nx-1; i++) {
    for (j=1; j<ny-1; j++) {
      u[i][j] = uo[i][j]
              + nu * ( uo [i-1][j] + uo [i+1][j]
                     + uo [i][j-1] + uo [i][j+1]
                     - 4.0 * uo [i][j] );
	}
  }
}
