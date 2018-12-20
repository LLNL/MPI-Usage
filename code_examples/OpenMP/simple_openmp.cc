

static inline
void simple(domain,
                             float *x, float *y, float *z,
                             int numElem)
{
   //
   // comment here
   //

#pragma omp parallel for firstprivate(numElem)
   for (Index_t i = 0 ; i < numElem ; ++i){
      x[i] = y[i] = z[i] =  - domain.p(i) - domain.q(i) ;
   }
}
