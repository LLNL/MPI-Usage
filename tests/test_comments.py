#!/usr/bin/env python

import subprocess
import json
import sys

def main():
    sys.stdout.write("Testing functions in comments:\t\t")
    inputFile = "../code_examples/MPI/C_C++/calls_in_comments.c"
    cmd = ["../mpiusage.py", inputFile]
    cmdOutput = subprocess.check_output(cmd)
    jsonOut = json.loads(cmdOutput)
    
    result = "FAILED"
    if jsonOut['MPI_COMM_RANK'] == 1:
        result = "PASSED"

    sys.stdout.write(result+"\n")
    
main()
