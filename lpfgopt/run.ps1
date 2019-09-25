##

#set -e

clear
make clean
make
./out.exe
#valgrind ./out.exe
