#!/usr/bin/env python

import sys
import os
import re
import argparse

###############################################################################
# Output Format
###############################################################################
#
# The output is a json file of the form:
#
# {
#    "LINES": 523,
#    "OPEN_MP": 7,
#    "MPI_BCAST": 3,
#    "MPI_REDUCE": 10,
# }
#
# Attributes use all characters in upper case. Values are integers.
# By default the output is printed and saved in a file 'output.json'.

###############################################################################
# Global variables
###############################################################################

# Dictionary of mpi calls
# keys: MPI call names, e.g., 'MPI_Bcast' or 'mpi_reduce'
# value: integer representing number of times seen
MPI_CALLS_TABLE = {}

### Regexp for C/C++ ###

mpi_name_re = re.compile(r"(?P<mpi_name>MPI\_[a-zA-Z_]+)")

# Matches MPI call with return code definition "int value = MPI_..."
mpi_call_ret_def_re = re.compile(r"(?P<ret_value>^[\s]*(int)[\s]+[_a-zA-Z][_a-zA-Z0-9]+[\s]+\=[\s]+)"
                         r"(?P<mpi_call>MPI\_[a-zA-Z_]+)"
                         r"(?P<mpi_params>\((.)*\)[\s]*\;)")

# Matches MPI call with return code "value = MPI_..."
mpi_call_ret_re = re.compile(r"(?P<ret_value>^[\s]*[_a-zA-Z][_a-zA-Z0-9]+[\s]+\=[\s]+)"
                                 r"(?P<mpi_call>MPI\_[a-zA-Z_]+)"
                                 r"(?P<mpi_params>\((.)*\)[\s]*\;)")

# Matches MPI call without return code "MPI_..."
mpi_call_re = re.compile(r"(?P<no_ret_value>^[\s]*)"
                             r"(?P<mpi_call>MPI\_[a-zA-Z_]+)"
                             r"(?P<mpi_params>\((.)*\)[\s]*\;)")

### Regexp for Fortran ###

fmpi_name_re = re.compile(r"(?P<mpi_name>(mpi|MPI)\_[a-zA-Z_]+)")

# Matches MPI call in Fortran
fmpi_call_re = re.compile(r"(?P<call>^[\s]*(call|CALL)[\s]+)"
                                 r"(?P<mpi_call>(mpi|MPI)\_[a-zA-Z_]+)"
                                 r"(?P<mpi_params>\((.)*\))")

# Max size of an MPI Call in terms of lines
maxBufferSize = 10

#### Control variables ####
outputFileName = None
inputPath = "./"
verbose = False

###############################################################################
# Main
###############################################################################

def main():
    parseArgs()
    #input = sys.argv[1]
    input = inputPath
    printOut(["Analyzing", input, "..."])
    
    # Check if input exist
    if os.path.exists(input):
        
        # Traver tree if input is a directory
        if os.path.isdir(input):
            
            # This loop traverses the entire directory tree
            rootDir = input
            for dirName, subdirList, fileList in os.walk(rootDir):
                for fname in fileList:
                    # Full path of the file
                    filePath = dirName + "/" + fname
                    printOut([filePath])
                    analyzeFile(filePath)
        
        else: ## this is a file
            #print input
            analyzeFile(input)
    else:
        print "Error:", input, "does not exist"
        exit()

    # Print results
    printResults()

###############################################################################
# Helper Functions
###############################################################################

def parseArgs():
    global inputPath, outputFileName, verbose
    
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str,
                        help="file or directory to analyze")
    parser.add_argument("-o", "--output", help="name of output file", type=str)
    parser.add_argument("-v", "--verbose", help="print what the script does", action="store_true")
    args = parser.parse_args()

    inputPath = args.path

    if args.output:
        outputFileName = args.output
    if args.verbose:
        verbose = True

# Wrapper of print function
# out: a list of strings, e.g., ["hello", "world"]
def printOut(outList):
    global verbose
    if verbose:
        print " ".join(outList)

# This is the main function to analyze a file
def analyzeFile(filePath):
    fd = open(filePath, 'r')
    fileLines = fd.readlines()
    for i in range(len(fileLines)):
        name = matchMPIName(fileLines[i])
        if name != None:
            # We know this is an MPI name.
            # Now let's try to match a function call.
            n = 0
            while (n < maxBufferSize):
                longLine = concatenateInSingleLine(fileLines, i, i+n)
                mpi_call = matchMPICall(longLine)
                if mpi_call != None:
                    # We found an MPI call
                    printOut(["Call:", mpi_call+"()", "@ line", str(i+1)])
                    
                    # Increase count in table
                    # We store MPI call names in upper case
                    mpi_call = mpi_call.upper()
                    if mpi_call in MPI_CALLS_TABLE.keys():
                        MPI_CALLS_TABLE[mpi_call] = MPI_CALLS_TABLE[mpi_call] + 1
                    else:
                        MPI_CALLS_TABLE[mpi_call] = 1
                    
                    i = n
                    break
                n = n + 1
    fd.close()

# This function concatenates all lines in the range (x, y)
# from the linesArray into a single line.
# x must be <= y
def concatenateInSingleLine(linesArray, x, y):
    if x > y:
        print "Error in concatenateInSingleLine", x, y
        exit()
    ret = ""
    for i in range(x, y+1):
        if i >= len(linesArray):
            break
        ret = ret + linesArray[i][:-1]
    return ret

# This matches an MPI name and returns the name.
# Example: MPI_Bcast(...  returns "MPI_Bcast"
# Note that this will also match MPI_COMM_WORLD
def matchMPIName(line):
    result_c = mpi_name_re.search(line)
    result_f = fmpi_name_re.search(line)
    mpi_name = None
    if result_c != None:
        mpi_name = result_c.group('mpi_name')
    elif result_f != None:
        mpi_name = result_f.group('mpi_name')
    return mpi_name

# This matches an MPI call of the form: "MPI_Bcast(a, b, c,...);"
def matchMPICall(line):
    
    # Matching for C/C++ calls
    result1 = mpi_call_re.search(line)
    result2 = mpi_call_ret_re.search(line)
    result3 = mpi_call_ret_def_re.search(line)
    
    # Matching for Fortran calls
    result4 = fmpi_call_re.search(line)
    
    mpi_call = None
    if result1 != None:
        mpi_call = result1.group('mpi_call')
    elif result2 != None:
        mpi_call = result2.group('mpi_call')
    elif result3 != None:
        mpi_call = result3.group('mpi_call')
    elif result4 != None:
        mpi_call = result4.group('mpi_call')

    return mpi_call

# Print results to stdout
def printResults():
    printOut(["*** MPI Usage ***"])
    
    # We save output into a string first
    out = "{\n"
    for k in MPI_CALLS_TABLE.keys():
        line = "  " + "\"" + k + "\"" + ": " + str(MPI_CALLS_TABLE[k]) + ",\n"
        out = out + line    
    out = out + "}"
    
    print out
    if outputFileName != None:
        saveResults(out)

# Save results into a file
def saveResults(out):
    fd = open(outputFileName, 'w')
    fd.write(out)
    fd.close()


###############################################################################

main()
