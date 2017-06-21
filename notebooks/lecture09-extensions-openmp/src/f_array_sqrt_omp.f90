subroutine array_sqrt (n, a_in, a_out, nt)
  use omp_lib

  implicit none
  integer, intent(in) :: n
  real(kind=8), dimension(n), intent(in)  :: a_in
  real(kind=8), dimension(n), intent(out) :: a_out
  integer, intent(in) :: nt

  integer :: i

  !! set the number of threads to input nt
  call omp_set_num_threads (nt)

  !! schedule a parallel loop
  !$omp parallel do default(none) shared(a_in,a_out) firstprivate(n) private(i)
  do i = 1, n
     a_out(i) = sqrt (a_in(i))
  end do
  !$omp end parallel do

  return

end subroutine array_sqrt
