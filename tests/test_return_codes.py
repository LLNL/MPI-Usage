#!/usr/bin/env python

import subprocess

def main():
    print "Testing return values in C/C++..."
    inputFile = "../code_examples/MPI/C_C++/return_values.c"
    cmd = ["../mpiusage.py", inputFile, "-o", "test.json"]
    cmdOutput = subprocess.check_output(cmd)
    

main()
