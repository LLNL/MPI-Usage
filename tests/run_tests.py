#!/usr/bin/env python

import subprocess

subprocess.call("./test_return_codes.py")
subprocess.call("./test_fortran_program.py")
subprocess.call("./test_long_mpi_func.py")
subprocess.call("./test_comments.py")
subprocess.call("./test_openmp_c.py")
subprocess.call("./test_openmp_fortran.py")
subprocess.call("./test_openacc_c.py")
subprocess.call("./test_openacc_fortran.py")
subprocess.call("./test_cuda.py")
subprocess.call("./test_opencl.py")
subprocess.call("./test_calls_with_macro.py")
