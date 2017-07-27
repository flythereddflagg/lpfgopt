#!/bin/bash

set -e

rm -rf $HOME/.lpfgopt
sudo rm -f  /etc/ld.so.conf.d/lpfgopt.conf
sudo ldconfig

