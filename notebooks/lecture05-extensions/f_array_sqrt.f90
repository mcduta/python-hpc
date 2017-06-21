subroutine array_sqrt (n, a_in, a_out)

  implicit none
  integer, intent(in) :: n
  real, dimension(n), intent(in)  :: a_in
  real, dimension(n), intent(out) :: a_out

  integer :: i

  do i = 1, n
     a_out(i) = sqrt(a_in(i))
  end do

  return

end subroutine array_sqrt
