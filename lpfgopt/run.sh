#!/bin/bash

set -e

clear
make clean
make cpptest
./out.exe
#valgrind ./out.exe
