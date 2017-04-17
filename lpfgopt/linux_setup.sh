#!/bin/bash

set -e

#if [[ $(/usr/bin/id -u) -ne 0 ]]; then
#    echo "Permission Denied: Are you root?"
#    exit
#fi

make clean
make
#sudo cp liblpfgopt.so /lib

python csetup.py build_ext
python cysetup.py build_ext

cp ./build/lib.linux-x86_64-2.7/lpfgopt/*.so ./

python csetup.py clean
python cysetup.py clean

