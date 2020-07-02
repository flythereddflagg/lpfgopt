# For windows and linux

ifeq ($(OS), Windows_NT)
	EXECLEAN = execlean-windows
	CLEANER = clean-windows
	DLL = .dll
	LDL =
else
	EXECLEAN = execlean-linux
	CLEANER = clean-linux
	DLL = .so
	LDL = -ldl
endif

CC = gcc
CPP = g++
CPPFLAGS = -g -Wall
CFLAGS = -g -Wall -std=c11
DLLFLAGS = -shared -fPIC

SRC = leapfrog use_lib
OUT = out.exe
EXTRA = -I./include
EXE = -D OUT_EXE

.PHONY: ctest cpptest clean-linux clean-windows clean cleanall execlean-linux execlean-windows

all:
	$(CC) $(CFLAGS) $(DLLFLAGS) ./csrc/leapfrog.c -o ./lpfgopt/leapfrog_c$(DLL) $(EXTRA)

ctest:
	$(CC) $(CFLAGS) $(foreach var,$(SRC), ./csrc/$(var).c)\
	 -o $(OUT) $(EXTRA) $(EXE)

cpptest: all
	$(CPP) $(CPPFLAGS) ./csrc/use_dll.cpp -o $(OUT) $(LDL)

execlean-linux:
	rm -f *.exe

clean-linux: execlean-linux
	rm -f ./lpfgopt/*.so ./lpfgopt/*.dll

execlean-windows:
	del *.exe

clean-windows: execlean-windows
	del .\lpfgopt\*.dll
	del .\lpfgopt\*.so

cleanall: $(CLEANER)

clean: $(EXECLEAN)

