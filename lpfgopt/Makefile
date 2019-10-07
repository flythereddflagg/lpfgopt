# For windows and linux

ifeq ($(OS), Windows_NT)
	CLEANER = clean-windows
	DLL = .dll
	LDL =
else
	CLEANER = clean-linux
	DLL = .so
	LDL = -ldl
endif

CC = gcc
CPP = g++
CPPFLAGS = -g -Wall
CFLAGS = -g -Wall -std=c99
DLLFLAGS = -shared -fPIC

SRC = leapfrog use_lib
OUT = out.exe
EXTRA = -I./include
EXE = -D OUT_EXE

all:
	$(CC) $(CFLAGS) $(DLLFLAGS) ./csrc/leapfrog.c -o leapfrog$(DLL) $(EXTRA)


.PHONY: ctest
ctest:
	$(CC) $(CFLAGS) $(foreach var,$(SRC), ./csrc/$(var).c)\
	 -o $(OUT) $(EXTRA) $(EXE)


.PHONY: cpptest
cpptest: all
	$(CPP) $(CPPFLAGS) ./csrc/use_dll.cpp -o $(OUT) $(LDL)


.PHONY: clean-linux
clean-linux:
	rm -f *.exe *.so *.dll

.PHONY: clean-windows
clean-windows:
	del *.exe
	del *.dll
	del *.so


.PHONY: clean
clean: $(CLEANER)
