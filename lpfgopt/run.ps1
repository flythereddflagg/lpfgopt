##

#set -e

clear
make clean
make
echo ""
echo "running out.exe..."
./out.exe
#valgrind ./out.exe
