#!/bin/bash

set -e

make clean

clear
make
echo ""
./lpfg.exe
echo ""
valgrind ./lpfg.exe
