

/*
* This is a call MPI_Comm_rank()
* in a comment. We should not find this call.
*/


int func()
{

    int x;
    int ret = MPI_Comm_rank( MPI_COMM_WORLD, &x );

}
