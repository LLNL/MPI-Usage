

void __device__ kernel(float* odata, int height, int width)
{
   unsigned int x = blockIdx.x*blockDim.x + threadIdx.x;
   unsigned int y = blockIdx.y*blockDim.y + threadIdx.y;
   if (x < width && y < height) {
      float c = tex2D(tex, x, y);
      odata[y*width+x] = c;
   }
}
