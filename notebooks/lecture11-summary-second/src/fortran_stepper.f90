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
  use omp_lib

  implicit none

  integer, parameter :: dp = selected_real_kind (15, 307)

  integer,                                   intent (in)    :: nx,ny
  real (kind=dp), dimension (0:nx-1,0:ny-1), intent (inout) :: u
  real (kind=dp), dimension (0:nx-1,0:ny-1), intent (in)    :: uo
  real (kind=dp),                            intent (in)    :: nu

  integer :: i,j

  !$omp parallel do default(none) &
  !$omp&            private(i,j) shared(u,uo) &
  !$omp&            firstprivate(nx,ny, nu) collapse(2) &
  !$omp&            schedule(static)
  do j = 1, ny-2
     do i = 1, nx-2
        u(i,j) = uo(i,j)                        &
               + nu * ( uo (i-1,j) + uo (i+1,j) &
                      + uo (i,j-1) + uo (i,j+1) &
                      - 4.0_dp * uo (i,j) )
     end do
  end do
  !$omp end parallel do

end subroutine timestep


! -------------------------------------------------------------------- !
!                                                                      !
! -------------------------------------------------------------------- !
subroutine initialise (xmin,xmax, ymin,ymax, uo,u, nx,ny)

  use omp_lib
  implicit none

  integer, parameter       :: dp = selected_real_kind (15, 307)
  real(kind=dp), parameter :: PI = 3.141592653589793

  integer,                                   intent (in)    :: nx,ny
  real (kind=dp), dimension (0:nx-1,0:ny-1), intent (inout) :: u
  real (kind=dp), dimension (0:nx-1,0:ny-1), intent (inout) :: uo
  real (kind=dp),                            intent (in)    :: xmin,xmax, ymin,ymax

  integer        :: i,j
  real (kind=dp) :: dx,dy

  !interval spacing
  dx = (xmax - xmin) / real (nx-1, dp)
  dy = (ymax - ymin) / real (ny-1, dp)

  !$omp parallel do default(none) &
  !$omp&            private(i,j) shared(u,uo) &
  !$omp&            firstprivate(nx,ny, dx,dy) collapse(2) &
  !$omp&            schedule(static)
  do j = 0, ny-1
     do i = 0, nx-1
        uo(i,j) = sin ( real (i, dp) * dx * PI ) * sin ( real (j, dp) * dy * PI )
        u(i,j)  = 0.0_dp
     end do
  end do
  !$omp end parallel do


end subroutine initialise
