#!/bin/bash

set -e

LIB_DIR=$HOME/.lib
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ ! -d "$LIB_DIR" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  mkdir $LIB_DIR
fi

cp $DIR/liblpfgopt.so $LIB_DIR
echo "$LIB_DIR" > lpfgopt.conf
sudo cp lpfgopt.conf /etc/ld.so.conf.d
sudo ldconfig
