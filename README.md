# MPI Usage

`MPI Usage` is a python script that gathers statistics of MPI usage in MPI programs. It reports the MPI routines used in the program among other statistics, such as, the number of lines and languages used in the program (e.g., C, C++, Fortran, CUDA and OpenMP).

## How to Use

**Step 1:** Download `mpiusage.py` and `cloc` in a single location. `mpiusage.py` uses `cloc` to count the number of lines in the program. `mpiusage.py` will look for `cloc` in its root directory.

**Step 2:** Execute `mpiusage.py` using either a file or a directory of the program that you want to analyze as input. For example, if you want to analyze LULESH, which is in the path `/path/to/LULESH-2.0`, you would run:

```sh
$ ./mpiusage.py /path/to/LULESH-2.0
```

You can also provide as input a file:

```sh
$ ./mpiusage.py /path/to/main.c
```

For help you can use the `-h` option:

```sh
$ ./mpiusage.py -h
usage: mpiusage.py [-h] [-o OUTPUT] [-v] path

positional arguments:
  path                  file or directory to analyze

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        name of output file
  -v, --verbose         print what the script does
```

## Output

`MPI Usage` will by default output statistics in a json format in standard output:

```sh
$ ./mpiusage.py /path/lulesh/src/
{
  "MPI_COMM_SIZE": 3,
  "MPI_REDUCE": 3,
  "MPI_WAITALL": 2,
  "MPI_WAIT": 116,
  "MPI_COMM_RANK": 15,
  "MPI_ALLREDUCE": 3,
  "MPI_INIT": 3,
  "MPI_FINALIZE": 3,
  "MPI_ABORT": 12,
  "MPI_WTIME": 3,
  "MPI_IRECV": 26,
  "MPI_ISEND": 52,
  "MPI_BARRIER": 3,
  "OPENMP": 0,
  "OPENACC": 0,
  "CUDA": 168,
  "OPENCL": 0,
  "C_LINES": 0,
  "CPP_LINES": 297,
  "C_CPP_H_LINES": 365,
  "FORTRAN_LINES": 0,
  "LINES_OF_CODE": 14574
}
```

You can specify an output file using the `-o`

## License

MPI Usage is distributed under the terms of GNU General Public License v2.0 license.

See LICENSE and NOTICE for details.

LLNL-CODE-770417
