#!/usr/bin/env python

import test_config
import subprocess
import json
import sys

def main():
    t = "Testing MPI function macro wrapper:"
    testTarget = test_config.textWidth.format(t)
    sys.stdout.write(testTarget)
    inputFile = "../code_examples/MPI/C_C++/mpi_calls_with_macro.cpp"
    cmd = ["../mpiusage.py", inputFile]
    cmdOutput = subprocess.check_output(cmd)
    jsonOut = json.loads(cmdOutput)
    
    result = test_config.failed
    if jsonOut['X_MPI_BARRIER'] == 1:
        result = test_config.passed

    sys.stdout.write(result+"\n")
    
main()
