
param([string]$p1 = "")   # Get 1 command line parameter

# Clean DrMemory files and execuatble

echo "Cleaning DrMemory files..."
Remove-Item DrMemory-* -recurse
Remove-Item symcache -recurse
Remove-Item dynamorio -recurse
clear

if ($p1 -eq "clean") {    
make clean
} ElseIf ($p1 -eq "run"){ # Clean, compile and run without checking memory

make
echo ""
./lpfg.exe

} ElseIf ($p1 -eq "clean_mem"){ # Clean memory checking
echo "Memory files cleaned..."
} Else {                  # Clean, compile and run then check memory

make
echo ""
./lpfg.exe
echo ""
drmemory -logdir ./ lpfg.exe
}

