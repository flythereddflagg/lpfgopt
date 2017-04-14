#!/bin/bash

set -e

if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Permission Denied: Are you root?"
    exit
fi

make clean
make
cp liblpfgopt.so /lib

python csetup.py build_ext --inplace
python cysetup.py build_ext --inplace

python csetup.py clean
python cysetup.py clean

