#!/usr/bin/env python

import test_config
import subprocess
import json
import sys

def main():
    t = 'Testing return values in C/C++:'
    testTarget = test_config.textWidth.format(t)
    sys.stdout.write(testTarget)
    inputFile = "../code_examples/MPI/C_C++/return_values.c"
    cmd = ["../mpiusage.py", inputFile]
    cmdOutput = subprocess.check_output(cmd)
    jsonOut = json.loads(cmdOutput)
    
    result = test_config.passed
    if jsonOut['MPI_BCAST'] != 4:
        result = test_config.failed

    sys.stdout.write(result+"\n")
    
main()
