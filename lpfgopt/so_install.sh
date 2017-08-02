#!/bin/bash

set -e

echo "Installing lpfgopt shared object libraries..."

if [[ $EUID -eq 0 ]]; then
    # avoid installing to /root directory with sudo
    USER_HOME=$(getent passwd $SUDO_USER | cut -d: -f6)
else
    USER_HOME=$HOME
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LIB_DIR=$USER_HOME/.lib


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
    
    if [ -e $USER_HOME/.lib/liblpfgopt.so ] && [ -e /etc/ld.so.conf.d/lpfgopt.conf ]; then
        echo "Library install with root successful"
    else
        echo "It didn't work (with root!)"
    fi
    
else

    # install without root privileges
    echo "export LD_LIBRARY_PATH="$USER_HOME"/.lib" >> $USER_HOME/.bashrc
    
    if [ -e $LIB_DIR/liblpfgopt.so ]; then
        echo "Library install successful"
    else
        echo "It didn't work (no root!)"
    fi
    
fi

echo "DONE."

