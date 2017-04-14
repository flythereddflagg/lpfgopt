param([string]$p1 = "")   # Get 1 command line parameter

if ($p1 -eq "clean") {    
make clean
clear
} ElseIf ($p1 -eq "test"){ # Clean, compile and run without checking memory
make clean
clear
make
python csetup.py build_ext
python cysetup.py build_ext
Copy-Item ".\build\lib.win-amd64-2.7\lpfgopt\*" ".\"
python csetup.py clean
python cysetup.py clean
echo ""
./lpfgopt_test.exe
python test1.py

} Else {    # clean and compile
make clean
clear
make
python csetup.py build_ext
python cysetup.py build_ext
Copy-Item ".\build\lib.win-amd64-2.7\lpfgopt\*" ".\"
python csetup.py clean
python cysetup.py clean
}
