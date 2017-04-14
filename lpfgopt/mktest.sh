set -e

make clean
clear
make
./lpfgopt.exe

valgrind ./lpfgopt.exe

