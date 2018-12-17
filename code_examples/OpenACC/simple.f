subroutine process( a, b, n )
  real :: a(:,:), b(:,:)
  integer :: n, i, j
  !$acc kernels loop gang present(a,b)
  do j = 1, n
    !$acc loop vector
    do i = 1, n
      b(i,j) = exp(sin(a(i,j)))
    enddo
   enddo
end subroutine
