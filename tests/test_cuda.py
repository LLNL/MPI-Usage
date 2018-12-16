#!/usr/bin/env python

import subprocess
import json
import sys

def main():
    sys.stdout.write("Testing CUDA:\t\t\t\t")
    inputFile = "../code_examples/CUDA/device_kernel.c"
    cmd = ["../mpiusage.py", inputFile]
    cmdOutput = subprocess.check_output(cmd)
    jsonOut = json.loads(cmdOutput)
    
    result = "PASSED"
    if jsonOut['CUDA'] != 1:
        result = "FAILED"
    
    inputFile = "../code_examples/CUDA/comd_cuda_kernel.h"
    cmd = ["../mpiusage.py", inputFile]
    cmdOutput = subprocess.check_output(cmd)
    jsonOut = json.loads(cmdOutput)
    
    if jsonOut['CUDA'] != 1:
        result = "FAILED"

    sys.stdout.write(result+"\n")
    
main()
