#!/bin/bash

set -e

rm -f $HOME/.lib/liblpfgopt.so
sed -i "/export LD_LIBRARY_PATH=/d" $HOME/.bashrc
source $HOME/.profile

