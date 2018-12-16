#!/usr/bin/env python

import subprocess
import json
import sys

def main():
    sys.stdout.write("Testing long MPI function:\t\t")
    inputFile = "../code_examples/MPI/C_C++/lulesh_function.cpp"
    cmd = ["../mpiusage.py", inputFile]
    cmdOutput = subprocess.check_output(cmd)
    jsonOut = json.loads(cmdOutput)
    
    result = "FAILED"
    if jsonOut['MPI_IRECV'] == 26 and jsonOut['MPI_COMM_RANK'] == 1:
        result = "PASSED"

    sys.stdout.write(result+"\n")
    
main()
