# MPI Usage

This script analyzes MPI programs and reports MPI usage among other features, such as, number of lines and languages used in the program (C, C++, Fortran, etc.).

## How to Use

Download `mpiusage.py` and `cloc` in a single location. `mpiusage.py` uses `cloc` to count the number of lines in the program. `mpiusage.py` will look for `cloc` in its root directory.

Execute `mpiusage.py` using either a file or a directory of the program that you want to analyze as input. For example, if you want to analyze LULESH, which is in the path `/path/to/LULESH-2.0`, you would run:

```sh
$ ./mpiusage.py /path/to/LULESH-2.0
```

You can also provide as input a file:

```sh
$ ./mpiusage.py /path/to/main.c
```

## Output
