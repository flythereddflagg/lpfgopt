#!/bin/bash

set -e

echo "Uninstalling lpfgopt shared object libraries..."

if [ -e /etc/ld.so.conf.d/lpfgopt.conf ] && [ $EUID -eq 0 ]; then
    
    # was installed with root privileges
    rm -f $HOME/.lib/liblpfgopt.so
    sudo rm -f  /etc/ld.so.conf.d/lpfgopt.conf
    sudo ldconfig
    #echo "Successfully uninstalled liblpfgopt.so (root)"

elif [ -e /etc/ld.so.conf.d/lpfgopt.conf ] && [ $EUID -ne 0 ] ; then
    
    # was installed with root privileges but you don't have root privileges
    echo "Root privileges needed to uninstall"

elif [ -e $HOME/.lib/liblpfgopt.so ]; then
    
    # was installed without root privileges
    rm -f $HOME/.lib/liblpfgopt.so
    sed -i "/export LD_LIBRARY_PATH=/d" $HOME/.bashrc
    source $HOME/.profile
    #echo "Successfully uninstalled liblpfgopt.so (no root)"

else
    
    # something went wrong
    echo "Cannot uninstall. Library not found."

fi

echo "DONE."

