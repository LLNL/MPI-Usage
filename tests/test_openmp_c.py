#!/usr/bin/env python

import subprocess
import json
import sys

def main():
    sys.stdout.write("Testing OpenMP in C:\t\t\t")
    inputFile = "../code_examples/OpenMP/parallel.c"
    cmd = ["../mpiusage.py", inputFile]
    cmdOutput = subprocess.check_output(cmd)
    jsonOut = json.loads(cmdOutput)
    
    result = "FAILED"
    if jsonOut['OPENMP'] == 1:
        result = "PASSED"

    sys.stdout.write(result+"\n")
    
main()
