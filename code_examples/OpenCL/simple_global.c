

__kernel void fft (__global float2 *in, __global float2 *out,
                          __local float *x, __local float *y) {
    int tid = get_local_id(0);
    int blockIdx = get_group_id(0) * 1024 + tid;
    float2 data[16];

    __global float const *A = &B[i*ncols];
    
    in = in + blockIdx;  out = out + blockIdx;
}
