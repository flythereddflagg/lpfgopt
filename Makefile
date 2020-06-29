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
CFLAGS = -g -Wall -std=c11
DLLFLAGS = -shared -fPIC

SRC = leapfrog use_lib
OUT = out.exe
EXTRA = -I./include
EXE = -D OUT_EXE

.PHONY: ctest cpptest clean-linux clean-windows clean

all:
	$(CC) $(CFLAGS) $(DLLFLAGS) ./csrc/leapfrog.c -o ./lpfgopt/leapfrog_c$(DLL) $(EXTRA)

ctest:
	$(CC) $(CFLAGS) $(foreach var,$(SRC), ./csrc/$(var).c)\
	 -o $(OUT) $(EXTRA) $(EXE)

cpptest: all
	$(CPP) $(CPPFLAGS) ./csrc/use_dll.cpp -o $(OUT) $(LDL)

clean-linux:
	rm -f *.exe ./lpfgopt/*.so ./lpfgopt/*.dll

clean-windows:
	del *.exe
	del .\lpfgopt\*.dll
	del .\lpfgopt\*.so

clean: $(CLEANER)
