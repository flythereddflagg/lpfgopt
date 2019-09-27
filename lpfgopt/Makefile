# For windows and linux

ifeq ($(OS), Windows_NT)
	CLEANER = clean-windows
	DLL = .dll
else
	CLEANER = clean-linux
	DLL = .so
endif

CC = gcc
CFLAGS = -g -Wall -std=c99
DLLFLAGS = -shared -fPIC

SRC = lpfgopt main
OUT = out.exe
EXTRA = -I./include
EXE = -D OUT_EXE

all:
	$(CC) $(CFLAGS) $(DLLFLAGS) ./csrc/lpfgopt.c -o  leapfrog$(DLL) $(EXTRA)


.PHONY: ctest
ctest:
	$(CC) $(CFLAGS) $(foreach var,$(SRC), ./csrc/$(var).c)\
	 -o $(OUT) $(EXTRA) $(EXE)

.PHONY: clean-linux
clean-linux:
	rm -f ./obj/*.o *.exe *.so *.dll

.PHONY: clean-windows
clean-windows:
	del *.exe
	del *.dll
	del .\obj\*.o
	del *.so


.PHONY: clean
clean: $(CLEANER)
