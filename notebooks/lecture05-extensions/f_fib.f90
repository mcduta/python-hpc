subroutine fibonacci (n, a_out)

  implicit none
  integer, intent(in) :: n
  integer, dimension(n), intent(out) :: a_out

  integer :: i

  if (n >= 1) then
     a_out(1) = 1
  end if

  if (n >= 2) then
     a_out(2) = 1
  end if

  do i = 3, n
     a_out(i) = a_out(i-1) + a_out(i-2)
  end do

  return

end subroutine fibonacci
