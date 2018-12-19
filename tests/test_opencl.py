#!/usr/bin/env python

import test_config
import subprocess
import json
import sys

def main():
    t = "Testing OpenCL:"
    testTarget = test_config.textWidth.format(t)
    sys.stdout.write(testTarget)
    inputFile = "../code_examples/OpenCL/simple_kernel.c"
    cmd = ["../mpiusage.py", inputFile]
    cmdOutput = subprocess.check_output(cmd)
    jsonOut = json.loads(cmdOutput)
    
    result = test_config.passed
    if jsonOut['OPENCL'] != 1:
        result = test_config.failed
    
    inputFile = "../code_examples/OpenCL/simple_global.c"
    cmd = ["../mpiusage.py", inputFile]
    cmdOutput = subprocess.check_output(cmd)
    jsonOut = json.loads(cmdOutput)
    
    if jsonOut['OPENCL'] != 2:
        result = test_config.failed

    sys.stdout.write(result+"\n")
    
main()
