param([string]$p1 = "")   # Get 1 command line parameter

if ($p1 -eq "clean") {    
make clean
clear
} ElseIf ($p1 -eq "test"){ # Clean, compile and run without checking memory
make clean
clear
make
python ".\cython\csetup.py" build_ext
python ".\cython\cysetup.py" build_ext
Copy-Item ".\build\lib.win-amd64-2.7\*" ".\"
python ".\cython\csetup.py" clean
python ".\cython\cysetup.py" clean
echo ""
./lpfgopt_test.exe
python test1.py

} Else {    # clean and compile
make clean
clear
make
python ".\cython\csetup.py" build_ext
python ".\cython\cysetup.py" build_ext
Copy-Item ".\build\lib.win-amd64-2.7\*" ".\"
python ".\cython\csetup.py" clean
python ".\cython\cysetup.py" clean
rm -r build 
}
