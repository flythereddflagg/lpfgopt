#!/bin/bash

set -e

make clean                                # clean up old files
make                                      # Builds with Python options.
python "./cython/csetup.py" build_ext     # Build C extentions from Python source to optimize speed
python "./cython/cysetup.py" build_ext
cp build/lib.linux-x86_64-2.7/* .         # Copy compiled python files to the main directory for use
python "./cython/csetup.py" clean         # Clean up build files
python "./cython/cysetup.py" clean
rm -rf build                              # Delete the rest of the build

