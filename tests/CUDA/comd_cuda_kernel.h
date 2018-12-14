

// compute embedding energy
__global__ 
void EAM_Force_thread_atom2(SimGpu sim, AtomListGpu list)
{
  int tid = blockIdx.x * blockDim.x + threadIdx.x;
  if (tid >= list.n) return;

  // compute box ID and local atom ID
  int iAtom = list.atoms[tid];
  assert(iAtom < MAXATOMS);
  int iBox = list.cells[tid];
  assert(iBox < sim.boxes.nLocalBoxes);

  int iOff = iBox * MAXATOMS + iAtom;

  real_t fEmbed, dfEmbed;
  interpolate(sim.eam_pot.f, sim.eam_pot.rhobar[iOff], fEmbed, dfEmbed);
  sim.eam_pot.dfEmbed[iOff] = dfEmbed; // save derivative for halo exchange
  sim.atoms.e[iOff] += fEmbed;
}
