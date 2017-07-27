#!/bin/bash

set -e

mkdir ~/.lpfgopt
cp liblpfgopt.so ~/.lpfgopt
echo "export LD_LIBRARY_PATH="$HOME"/.lpfgopt" >> $HOME/.bashrc

