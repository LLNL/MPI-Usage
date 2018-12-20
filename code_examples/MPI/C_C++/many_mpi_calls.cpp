
void communicateAndReceive() {

   if (domain.numRanks() == 1)
      return ;

   /* ....*/
   MPI_Datatype baseType = ((sizeof(Real_t) == 4) ? MPI_FLOAT : MPI_DOUBLE) ;
   bool rowMin, rowMax, colMin, colMax, planeMin, planeMax ;

   /* assume communication to 6 neighbors by default */
   rowMin = rowMax = colMin = colMax = planeMin = planeMax = true ;

   MPI_Comm_rank(MPI_COMM_WORLD, &rank) ;


    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
   if (planeMin && doRecv) {

      MPI_Irecv(&domain.commDataRecv[pmsg * maxPlaneComm],
                recvCount, baseType, fromRank, msgType,
                MPI_COMM_WORLD, &domain.recvRequest[pmsg]) ;

   }
    
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
   if (planeMax) {

      MPI_Irecv(&domain.commDataRecv[pmsg * maxPlaneComm],
                recvCount, baseType, fromRank, msgType,
                MPI_COMM_WORLD, &domain.recvRequest[pmsg]) ;

   }
    
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
   if (rowMin && doRecv) {

      MPI_Irecv(&domain.commDataRecv[pmsg * maxPlaneComm],
                recvCount, baseType, fromRank, msgType,
                MPI_COMM_WORLD, &domain.recvRequest[pmsg]) ;
      ++pmsg ;
   }
    
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
   if (rowMax) {

      MPI_Irecv(&domain.commDataRecv[pmsg * maxPlaneComm],
                recvCount, baseType, fromRank, msgType,
                MPI_COMM_WORLD, &domain.recvRequest[pmsg]) ;
      ++pmsg ;
   }
    
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
   if (colMin && doRecv) {

      MPI_Irecv(&domain.commDataRecv[pmsg * maxPlaneComm],
                recvCount, baseType, fromRank, msgType,
                MPI_COMM_WORLD, &domain.recvRequest[pmsg]) ;
      ++pmsg ;
   }
    
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
   if (colMax) {

      MPI_Irecv(&domain.commDataRecv[pmsg * maxPlaneComm],
                recvCount, baseType, fromRank, msgType,
                MPI_COMM_WORLD, &domain.recvRequest[pmsg]) ;
      ++pmsg ;
   }

    
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
   if (!planeOnly) {

         MPI_Irecv(&domain.commDataRecv[pmsg * maxPlaneComm +
                                         emsg * maxEdgeComm],
                   dz * xferFields, baseType, fromRank, msgType,
                   MPI_COMM_WORLD, &domain.recvRequest[pmsg+emsg]) ;
         ++emsg ;
      }

      if (rowMin && planeMin && doRecv) {

         MPI_Irecv(&domain.commDataRecv[pmsg * maxPlaneComm +
                                         emsg * maxEdgeComm],
                   dx * xferFields, baseType, fromRank, msgType,
                   MPI_COMM_WORLD, &domain.recvRequest[pmsg+emsg]) ;

      }
    
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/

      if (colMin && planeMin && doRecv) {
         int fromRank = myRank - domain.tp()*domain.tp() - 1 ;
         MPI_Irecv(&domain.commDataRecv[pmsg * maxPlaneComm +
                                         emsg * maxEdgeComm],
                   dy * xferFields, baseType, fromRank, msgType,
                   MPI_COMM_WORLD, &domain.recvRequest[pmsg+emsg]) ;
         ++emsg ;
      }
    
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/
    /* COMMENTS COMMENTS  COMMENTS COMMENTS*/

      if (rowMax && colMax) {

         MPI_Irecv(&domain.commDataRecv[pmsg * maxPlaneComm +
                                         emsg * maxEdgeComm],
                   dz * xferFields, baseType, fromRank, msgType,
                   MPI_COMM_WORLD, &domain.recvRequest[pmsg+emsg]) ;
         ++emsg ;
      }

      if (rowMax && planeMax) {

         MPI_Irecv(&domain.commDataRecv[pmsg * maxPlaneComm +
                                         emsg * maxEdgeComm],
                   dx * xferFields, baseType, fromRank, msgType,
                   MPI_COMM_WORLD, &domain.recvRequest[pmsg+emsg]) ;
         ++emsg ;
      }

    }
}
