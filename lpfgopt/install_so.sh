#!/bin/bash

set -e

mkdir ~/.lpfgopt
cp liblpfgopt.so ~/.lpfgopt
echo $HOME"/.lpfgopt" > lpfgopt.conf
sudo cp lpfgopt.conf /etc/ld.so.conf.d
sudo ldconfig

