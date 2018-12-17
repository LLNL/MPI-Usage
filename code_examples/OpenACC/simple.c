

  // Compute matrix multiplication.
#pragma acc kernels copyin(a,b) copy(c)
  for (i = 0; i < SIZE; ++i) {
    for (j = 0; j < SIZE; ++j) {
      for (k = 0; k < SIZE; ++k) {
    c[i][j] += a[i][k] * b[k][j];
      }
    }
  }
