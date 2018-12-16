#!/usr/bin/env python

import subprocess
import json
import sys

def main():
    sys.stdout.write("Testing return values in C/C++:\t\t")
    inputFile = "../code_examples/MPI/C_C++/return_values.c"
    cmd = ["../mpiusage.py", inputFile]
    cmdOutput = subprocess.check_output(cmd)
    jsonOut = json.loads(cmdOutput)
    
    result = "PASSED"
    if jsonOut['MPI_BCAST'] != 4:
        result = "FAILED"

    sys.stdout.write(result+"\n")
    
main()