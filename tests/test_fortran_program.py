#!/usr/bin/env python

import test_config
import subprocess
import json
import sys

def main():
    t = "Testing Fortran program:"
    testTarget = test_config.textWidth.format(t)
    sys.stdout.write(testTarget)
    inputFile = "../code_examples/MPI/Fortran/simple_fortran.f"
    cmd = ["../mpiusage.py", inputFile]
    cmdOutput = subprocess.check_output(cmd)
    jsonOut = json.loads(cmdOutput)
    
    result = test_config.failed
    if jsonOut['MPI_REDUCE'] == 3 and jsonOut['MPI_BCAST'] == 6:
        result = test_config.passed

    sys.stdout.write(result+"\n")
    
main()
