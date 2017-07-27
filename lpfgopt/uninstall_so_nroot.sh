#!/bin/bash

set -e

rm -rf $HOME/.lpfgopt
sed -i "/export LD_LIBRARY_PATH=/d" $HOME/.bashrc
source $HOME/.profile

