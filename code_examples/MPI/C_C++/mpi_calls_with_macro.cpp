

#define HEMELB_MPI_CALL( mpiFunc, args ) \
{ \
  int _check_result = mpiFunc args; \
  if (_check_result != MPI_SUCCESS) \
    throw ::hemelb::net::MpiError(#mpiFunc, _check_result, __FILE__, __LINE__); \
}


void func()
{
  HEMELB_MPI_CALL( 
	MPI_Barrier , 
		comm);

}
