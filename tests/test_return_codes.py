#!/usr/bin/env python

import os

def main():
    print "Testing return values in C/C++..."
    file = "../code_examples/MPI/C_C++/return_values.c"
    cmd = "../mpiusage.py " + file + " -o " + "test.json"
    os.system(cmd)

main()
