
param([string]$p1 = "")   # Get 1 command line parameter

# Clean DrMemory files and execuatble

echo "Cleaning DrMemory files..."
Remove-Item DrMemory-* -recurse
Remove-Item symcache -recurse
Remove-Item dynamorio -recurse


if ($p1 -eq "clean") {    
make clean
clear
} ElseIf ($p1 -eq "run"){ # Clean, compile and run without checking memory
make clean
clear
make
echo ""
./lpfgopt_test.exe

drmemory -logdir ./ lpfgopt_test.exe

} ElseIf ($p1 -eq "clean_mem"){ # Clean memory checking
clear
echo "Memory files cleaned..."
} Else {                  # Clean, compile and run then check memory
make clean
clear
make
echo ""
python test.py
echo ""
#drmemory -logdir ./ lpfg.exe
}

