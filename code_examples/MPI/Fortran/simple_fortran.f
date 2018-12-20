
c--------------------------------
       program SAMPLE_PROGRAM
c--------------------------------

c---- Comments Comments Comments Comments Comments Comments 
       call mpi_bcast(val, val, MPI_INTEGER,
     >                val, comm_setup, error)

c---- Comments Comments Comments Comments Comments Comments 
       call mpi_bcast(val, val, MPI_INTEGER, 
     >                root, comm_setup, error)

c---- Comments Comments Comments Comments Comments Comments 
       call mpi_bcast(val, val, MPI_INTEGER, 
     >                val, comm_setup, error)

c---- Comments Comments Comments Comments Comments Comments 
       call mpi_bcast(val, val, MPI_INTEGER,
     >                val, comm_setup, error)

c---- Comments Comments Comments Comments Comments Comments 
       call mpi_bcast(val, val, MPI_INTEGER,
     >                val, comm_setup, error)

c---- Comments Comments Comments Comments Comments Comments 
       call mpi_bcast(val, val, MPI_INTEGER, 
     >                val, comm_setup, error)


       call MPI_Reduce(t1, val, val, val, val,
     >                 0, comm_setup, error)
       call MPI_Reduce(t1, val, val, val, val,
     >                 0, comm_setup, error)
       call MPI_Reduce(t1, val, val, val, val, 
     >                 0, comm_setup, error)


       end

