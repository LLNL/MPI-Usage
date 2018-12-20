#!/usr/bin/env python

import test_config
import subprocess
import json
import sys

def main():
    t = "Testing CUDA:"
    testTarget = test_config.textWidth.format(t)
    sys.stdout.write(testTarget)
    inputFile = "../code_examples/CUDA/device_kernel.c"
    cmd = ["../mpiusage.py", inputFile]
    cmdOutput = subprocess.check_output(cmd)
    jsonOut = json.loads(cmdOutput)
    
    result = test_config.passed
    if jsonOut['CUDA'] != 1:
        result = test_config.failed
    
    inputFile = "../code_examples/CUDA/small_cuda_kernel.h"
    cmd = ["../mpiusage.py", inputFile]
    cmdOutput = subprocess.check_output(cmd)
    jsonOut = json.loads(cmdOutput)
    
    if jsonOut['CUDA'] != 1:
        result = test_config.failed

    sys.stdout.write(result+"\n")
    
main()
