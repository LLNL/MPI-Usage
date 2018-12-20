

__global__ 
void force_thread_atom2(sim, list)
{
  int tid = blockIdx.x * blockDim.x + threadIdx.x;
  if (tid >= list.n) return;

  int iAtom = list.atoms[tid];
  int iBox = list.cells[tid];

  int iOff = iBox * MAXATOMS + iAtom;
}
