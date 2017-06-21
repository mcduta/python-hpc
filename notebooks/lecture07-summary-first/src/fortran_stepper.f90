!
! file:       fortran_stepper.f90
! purpose:    create python library
! implements: a time step for the explicit FTCS scheme to solve
!             the time-dependent heat equation
! author:     Mihai Duta,
!             Advanced Research Computing,
!             University of Oxford
!


subroutine timestep (nu, uo,u, nx,ny)

  implicit none

  integer, parameter :: dp = selected_real_kind (15, 307)

  integer,                                   intent (in)    :: nx,ny
  real (kind=dp), dimension (0:nx-1,0:ny-1), intent (inout) :: u
  real (kind=dp), dimension (0:nx-1,0:ny-1), intent (in)    :: uo
  real (kind=dp),                            intent (in)    :: nu

  u(1:nx-2, 1:ny-2) = uo(1:nx-2, 1:ny-2)                               &
                    + nu * ( uo (0:nx-3, 1:ny-2) + uo (2:nx-1, 1:ny-2) &
                           + uo (1:nx-2, 0:ny-3) + uo (1:nx-2, 2:ny-1) &
                           - 4.0_dp * uo (1:nx-2, 1:ny-2) )

end subroutine timestep
