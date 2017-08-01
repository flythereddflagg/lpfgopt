#!/bin/bash

set -e

echo ""
echo "Installing lpfgopt shared object libraries..."
echo ""

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LIB_DIR=$HOME/.lib

if [ ! -d "$LIB_DIR" ]; then
  # Control will enter here if $LIB_DIR doesn't exist.
  mkdir $LIB_DIR
fi

cp $DIR/liblpfgopt.so $LIB_DIR


if [[ $EUID -eq 0 ]]; then
    
    # install with root privileges
    echo "$LIB_DIR" > $DIR/lpfgopt.conf
    sudo cp $DIR/lpfgopt.conf /etc/ld.so.conf.d
    sudo ldconfig
    
    if [ -e $HOME/.lib/liblpfgopt.so ] && [ -e /etc/ld.so.conf.d/lpfgopt.conf ]; then
        echo "It worked (with root!)"
    else
        echo "It didn't work (with root!)"
    fi
    
else

    # install without root privileges
    echo "export LD_LIBRARY_PATH="$HOME"/.lib" >> $HOME/.bashrc
    
    if [ -e $HOME/.lib/liblpfgopt.so ]; then
        echo "It worked (no root!)"
    else
        echo "It didn't work (no root!)"
    fi
    
fi

echo "DONE."

