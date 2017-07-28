#!/bin/bash

set -e

rm -f $HOME/.lib/liblpfgopt.so
sudo rm -f  /etc/ld.so.conf.d/lpfgopt.conf
sudo ldconfig
