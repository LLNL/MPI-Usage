#!/usr/bin/env python

import test_config
import subprocess
import json
import sys

def main():
    t = "Testing long MPI function:"
    testTarget = test_config.textWidth.format(t)
    sys.stdout.write(testTarget)
    inputFile = "../code_examples/MPI/C_C++/many_mpi_calls.cpp"
    cmd = ["../mpiusage.py", inputFile]
    cmdOutput = subprocess.check_output(cmd)
    jsonOut = json.loads(cmdOutput)
    
    result = test_config.failed
    if jsonOut['MPI_IRECV'] == 11 and jsonOut['MPI_COMM_RANK'] == 1:
        result = test_config.passed

    sys.stdout.write(result+"\n")
    
main()
