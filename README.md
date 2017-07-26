# title          : Leap Frog Optimizer Package
### version        : 0.6.2 ALPHA
### last modified  : 11 April 2017 
### author         : Mark Redd
### email          : redddogjr@gmail.com


optimizer algorithm website: http://www.r3eda.com/

about:

This optimizer was written based on the algorithm published by
Dr. R. Russell Rhinehart.

A full explanation of the algorithm can be found at the following URL:

http://www.r3eda.com/leapfrogging-optimization-algorithm/

The following are "key references" published on the optimization website explaining the technique:

  - Rhinehart, R. R., M. Su, and U. Manimegalai-Sridhar,
    “Leapfrogging and Synoptic Leapfrogging: a new optimization approach”,
    Computers & Chemical Engineering, Vol. 40, 11 May 2012, pp. 67-81.

  - Manimegalai-Sridhar, U., A. Govindarajan, and R. R. Rhinehart,
    “Improved Initialization of Players in Leapfrogging Optimization”,
    Computers & Chemical Engineering, Vol. 60, 2014, 426-429.

  - Rhinehart, R. R.,
    “Convergence Criterion in Optimilsation of Stochastic Processes”,
    Computers & Chemical Engineering, Vol. 68, 4 Sept 2014, pp 1-6.


## installation:

# lpfgopt
Leap Frog Optimizer

See README.rst
 - NOTE: for dylibs on mac use the following gcc commands found on
http://stackoverflow.com/questions/3532589/how-to-build-a-dylib-from-several-o-in-mac-os-x-using-gcc

"g++ -dynamiclib -undefined suppress -flat_namespace *.o -o something.dylib"

### Compile with minGW gcc:
    make: make all execuatble with python option
    make dll: make the dll files and nothing else
    make python-dll: make the dll files with the python option 
                     and nothing else
    make exe: make the execuatble; only works with make dll first
    make clean: erase all files made