#!/usr/bin/env python

import subprocess
import json
import sys

def main():
    sys.stdout.write("Testing Fortran program:\t\t")
    inputFile = "../code_examples/MPI/Fortran/bt.f"
    cmd = ["../mpiusage.py", inputFile]
    cmdOutput = subprocess.check_output(cmd)
    jsonOut = json.loads(cmdOutput)
    
    result = "FAILED"
    if jsonOut['MPI_REDUCE'] == 5 and jsonOut['MPI_BARRIER'] == 2 and jsonOut['MPI_FINALIZE'] == 1 and jsonOut['MPI_BCAST'] == 6:
        result = "PASSED"

    sys.stdout.write(result+"\n")
    
main()
