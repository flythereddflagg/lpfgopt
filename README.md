# Leap Frog Optimizer Package

version        : 0.7.0 - ALPHA <br/>
last modified  : 26 July 2017 <br/>
author         : Mark Redd <br/>
email          : redddogjr@gmail.com <br/>

#### optimizer algorithm website: http://www.r3eda.com/

### about:

This optimizer was written based on the algorithm published by
Dr. R. Russell Rhinehart.

A full explanation of the algorithm can be found at the following URL:

http://www.r3eda.com/leapfrogging-optimization-algorithm/

The following are "key references" published on the optimization website 
explaining the technique:

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

There are a variety of ways to install the software both for use in Python or 
C/C++ on Windows and Linux.
All source code has been tested with GCC and Python 2.7. Other compilers and
Python 3 will have support in future versions.

#### From Source (Windows (7, 8, 10), MinGW, Python 2.7):
1. If you can run Powershell scripts the ".\lpfgopt\windows_setup.ps1" script 
will do all the work for you.
Otherwise, run the follwing commands from Powershell in the ".\lpfgopt\" path:
```bash
> make clean                                    # clean up old files
> make                                          # Builds with Python options. See below for more 'make' options.
> python ".\cython\csetup.py" build_ext         # Build C extentions from Python source to optimize speed
> python ".\cython\cysetup.py" build_ext
> Copy-Item ".\build\lib.win-amd64-2.7\*" ".\"  # Copy compiled python files to the main directory for use
> python ".\cython\csetup.py" clean             # Clean up build files
> python ".\cython\cysetup.py" clean
> rm -r build                                   # Delete the rest of the build
```
2. Return to the main directory where "setup.py" is located and run the following command"
```bash
> cd ..
> python setup.py install
```
The software should install correctly. You may validate the installation by executing the following commands:
```python
> python
>>> import lpfgopt
>>> lpfgopt.__version__
'X.X.X'
```
If the version number appears below, congratulations! You have sucessfully installed the Leap Frog Optimizer package on your windows machine!

<b>MinGW/GCC make options:</b><br/>
The following are the 'GNU make' commands that will make the needed files in 
the './lpfgopt' folder
```bash
make            # make all execuatble with python option
make dll        # make the dll files and nothing else
make python-dll # make the dll files with the python option and nothing else
make exe        # make the execuatble; only works with make dll first
make clean      # erase all files made
```

 - NOTE: Support for Macintosh will be added in future versions. For dylibs on 
mac use the following gcc commands found on:
http://stackoverflow.com/questions/3532589/how-to-build-a-dylib-from-several-o-in-mac-os-x-using-gcc

`g++ -dynamiclib -undefined suppress -flat_namespace *.o -o something.dylib`


## Usage
[Nothing here yet]