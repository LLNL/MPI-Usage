#!/usr/bin/env python

import sys
import os
import re
import argparse
import subprocess


###############################################################################
# Output Format
###############################################################################
#
# The output is in json format:
#
#{
#  "MPI_COMM_SIZE": 3,
#  "MPI_REDUCE": 3,
#  "MPI_WAITALL": 2,
#  "MPI_WAIT": 116,
#  "MPI_COMM_RANK": 15,
#  "MPI_ALLREDUCE": 3,
#  "MPI_INIT": 3,
#  "MPI_FINALIZE": 3,
#  "MPI_ABORT": 12,
#  "MPI_IRECV": 26,
#  "MPI_ISEND": 52,
#  "OPENMP": 0,
#  "OPENACC": 0,
#  "CUDA": 168,
#  "OPENCL": 0,
#  "C_LINES": 0,
#  "CPP_LINES": 297,
#  "C_CPP_H_LINES": 365,
#  "FORTRAN_LINES": 0,
#  "LINES_OF_CODE": 14574
#}
#
#
# Attributes use all characters in upper case. Values are integers.

###############################################################################
# Global variables
###############################################################################

# Dictionary of mpi calls
# keys: MPI call names, e.g., 'MPI_Bcast' or 'mpi_reduce'
# value: integer representing number of times seen
MPI_CALLS_TABLE = {}

openMPPragmas = 0
openACCPragmas = 0
CUDASymbols = 0
OpenCLSymbols = 0

c_lines = 0
cpp_lines = 0
c_cpp_header_lines = 0
fortran_lines = 0
total_lines_of_code = 0

########################
### Regexp for C/C++ ###
########################

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

# Matches MPI symbol macro definition: "#define MPI_Send  hypre_MPI_Send"
mpi_macro_re = re.compile(r"(?P<no_ret_value>^[\s]*)"
                         r"(?P<macro>#define[\s]+)"
                         r"(?P<mpi_symbol>MPI\_[a-zA-Z_]+)"
                         r"(?P<space>[\s]+)")

# This case is found in an application that makes calls to MPI using macros:
#
# #define HEMELB_MPI_CALL( mpiFunc, args ) \
# { \
# int _check_result = mpiFunc args; \
# if (_check_result != MPI_SUCCESS) \
# throw ::hemelb::net::MpiError(#mpiFunc, _check_result, __FILE__, __LINE__); \
# }
#
mpi_macro_wrapper_re = re.compile(r"(?P<no_ret_value>^[\s]*)"
                          r"(?P<mpi_symbol>MPI\_[a-zA-Z_]+)"
                          r"(?P<comma>[\s]*[,][\s]*)")

# Matches OpenMP in C
openmp_c_re = re.compile(r"(?P<openmp>^[\s]*(\#pragma)[\s]+(omp))")

# Matches OpenACC in C
openacc_c_re = re.compile(r"(?P<openacc>^[\s]*(\#pragma)[\s]+(acc))")

# Matches CUDA __global__ kernel
cuda_global_kernel_re = re.compile(r"(?P<cuda_kernel>(__global__)[\s]+)")
# Matches CUDA __device__ kernel
cuda_device_kernel_re = re.compile(r"(?P<cuda_kernel>(__device__)[\s]+)")

# Matches OpenCL __global
opencl_global_re = re.compile(r"(?P<opencl_global>(__global)[\s]+)")
# Matches OpenCL __kernel
opencl_kernel_re = re.compile(r"(?P<cuda_kernel>(__kernel)[\s]+)")

##########################
### Regexp for Fortran ###
##########################

fmpi_name_re = re.compile(r"(?P<mpi_name>(mpi|MPI)\_[a-zA-Z_]+)")

# Matches MPI call in Fortran
fmpi_call_re = re.compile(r"(?P<call>^[\s]*(call|CALL)[\s]+)"
                                 r"(?P<mpi_call>(mpi|MPI)\_[a-zA-Z_]+)"
                                 r"(?P<mpi_params>\((.)*\))")

# Matches OpenMP in Fortran
openmp_fortran_re = re.compile(r"(?P<openmp>^[\s]*(\!\$(OMP|omp)))")

# Matches OpenACC in Fortran
openacc_fortran_re = re.compile(r"(?P<openacc>^[\s]*(\!\$(ACC|acc)))")

#######################
### Regexp for Cloc ###
#######################

cloc_c_re = re.compile(r"(^C[\s]+[0-9]+[\s]+[0-9]+[\s]+[0-9]+[\s]+[0-9]+)")
cloc_cpp_re = re.compile(r"(^C\+\+[\s]+[0-9]+[\s]+[0-9]+[\s]+[0-9]+[\s]+[0-9]+)")
cloc_c_cpp_header_re = re.compile(r"(^(C\/C\+\+ Header)[\s]+[0-9]+[\s]+[0-9]+[\s]+[0-9]+[\s]+[0-9]+)")
cloc_fortran_re = re.compile(r"(^(Fortran [0-9]+)[\s]+[0-9]+[\s]+[0-9]+[\s]+[0-9]+[\s]+[0-9]+)")



###########################
#### Control variables ####
###########################

outputFileName = None
inputPath = "./"
verbose = False
# Max size of an MPI Call in terms of lines
maxBufferSize = 10

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

    # cloc statistics
    getClocStatistics(input)

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
        
        # Check for languages
        checkOpenMP(fileLines[i])
        checkOpenACC(fileLines[i])
        checkCUDA(fileLines[i])
        checkOpenCL(fileLines[i])
        
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
    
    # Matching macro definitions
    result5 = mpi_macro_re.search(line)
    result6 = mpi_macro_wrapper_re.search(line)
    
    mpi_call = None
    if result1 != None:
        mpi_call = result1.group('mpi_call')
    elif result2 != None:
        mpi_call = result2.group('mpi_call')
    elif result3 != None:
        mpi_call = result3.group('mpi_call')
    elif result4 != None:
        mpi_call = result4.group('mpi_call')
    elif result5 != None:
        mpi_call = "X_" + result5.group('mpi_symbol')
    elif result6 != None:
        mpi_call = "X_" + result6.group('mpi_symbol')

    return mpi_call

# Print results to stdout
def printResults():
    global MPI_CALLS_TABLE, outputFileName, openMPPragmas, openACCPragmas, CUDAkernels, c_lines, cpp_lines, c_cpp_header_lines, fortran_lines, total_lines_of_code
    printOut(["*** MPI Usage ***"])
    
    # We save output into a string
    out = "{\n"
    for k in MPI_CALLS_TABLE.keys():
        line = "  " + "\"" + k + "\"" + ": " + str(MPI_CALLS_TABLE[k]) + ",\n"
        out = out + line

    out = out + '  "OPENMP": ' + str(openMPPragmas) + ',\n'
    out = out + '  "OPENACC": ' + str(openACCPragmas) + ',\n'
    out = out + '  "CUDA": ' + str(CUDASymbols) + ',\n'
    out = out + '  "OPENCL": ' + str(OpenCLSymbols) + ',\n'
    
    out = out + '  "C_LINES": ' + str(c_lines) + ',\n'
    out = out + '  "CPP_LINES": ' + str(cpp_lines) + ',\n'
    out = out + '  "C_CPP_H_LINES": ' + str(c_cpp_header_lines) + ',\n'
    out = out + '  "FORTRAN_LINES": ' + str(fortran_lines) + ',\n'
    
    # For consistency, let's make LINES_OF_CODE the last one 
    out = out + '  "LINES_OF_CODE": ' + str(total_lines_of_code) + '\n'
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
# Language detection
###############################################################################

def checkOpenMP(line):
    global openMPPragmas
    
    # Matching C OpenMP
    result1 = openmp_c_re.search(line)
    # Matching Fortran OpenMP
    result2 = openmp_fortran_re.search(line)
    
    if result1 != None or result2 != None:
        openMPPragmas = openMPPragmas + 1

def checkOpenACC(line):
    global openACCPragmas
    
    # Matching C OpenACC
    result1 = openacc_c_re.search(line)
    # Matching Fortran OpenACC
    result2 = openacc_fortran_re.search(line)
    
    if result1 != None or result2 != None:
        openACCPragmas = openACCPragmas + 1

def checkCUDA(line):
    global CUDASymbols

    result1 = cuda_global_kernel_re.search(line)
    result2 = cuda_device_kernel_re.search(line)

    if result1 != None or result2 != None:
        CUDASymbols = CUDASymbols + 1

def checkOpenCL(line):
    global OpenCLSymbols
    
    result1 = opencl_global_re.search(line)
    result2 = opencl_kernel_re.search(line)
    
    if result1 != None or result2 != None:
        OpenCLSymbols = OpenCLSymbols + 1

###############################################################################
# Cloc calling and parsing
###############################################################################

def getClocStatistics(input):
    global c_lines, cpp_lines, c_cpp_header_lines, fortran_lines, total_lines_of_code
    
    printOut(["Calling cloc..."])
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cmd = [dir_path+"/cloc", input]
    cmdOutput = subprocess.check_output(cmd)
    
    for line in cmdOutput.split("\n"):
        test_c = cloc_c_re.search(line)
        test_cpp = cloc_cpp_re.search(line)
        test_c_cpp_header = cloc_c_cpp_header_re.search(line)
        test_fortran = cloc_fortran_re.search(line)
    
        if test_c != None:
            c_lines = int(line.split()[-1:][0])
        elif test_cpp != None:
            cpp_lines = int(line.split()[-1:][0])
        elif test_c_cpp_header != None:
            c_cpp_header_lines = int(line.split()[-1:][0])
        elif test_fortran != None:
            fortran_lines = fortran_lines + int(line.split()[-1:][0])
        elif "SUM:" in line:
            total_lines_of_code = int(line.split()[-1:][0])

###############################################################################

main()
