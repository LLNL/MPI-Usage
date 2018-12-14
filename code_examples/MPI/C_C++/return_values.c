

int foo()
{

    int ret = MPI_Bcast( (void *)buffer, 
                    1, MPI_INT, 0, 
                    MPI_COMM_WORLD);
    
ret = MPI_Bcast( (void *)buffer, 
                        1, MPI_INT, 0, 
                        MPI_COMM_WORLD);

   MPI_Bcast( (void *)buffer, 
                        1, MPI_INT, 0, 
                        MPI_COMM_WORLD);

    MPI_Bcast( (void *)buffer,1, MPI_INT, 0, MPI_COMM_WORLD);
}
