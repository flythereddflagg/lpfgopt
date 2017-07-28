#!/bin/bash

set -e

LIB_DIR = $HOME/.lib

if [ ! -d "$LIB_DIR" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  mkdir $LIB_DIR
fi

cp liblpfgopt.so $HOME/.lib
echo "export LD_LIBRARY_PATH="$HOME"/.lib" >> $HOME/.bashrc
