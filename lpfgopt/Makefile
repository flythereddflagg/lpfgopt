# For windows and linux

ifeq ($(OS), Windows_NT)
	TARGETS = windows
	CLEANER = clean-windows
else
	TARGETS = linux
	CLEANER = clean-linux
endif

CC = gcc
CFLAGS = -std='c99' -g -Wall
WIN_DETAILS = windres

DLL  = lpfgopt
SO   = lpfgopt
PROG = lpfgopt_test
DETAILS = details
EXPORT_CALL = LPFGOPT_EXPORTS
PY_OPT = PY_EXPORTS


all: $(TARGETS)

windows: python-dll exe-win
linux: python-so exe-lin

python-dll: src/$(DLL).c include/$(DLL).h
	$(WIN_DETAILS) -i res/$(DETAILS).rc -o obj/$(DETAILS).o
	$(CC) $(CFLAGS) -c -o obj/$(DLL).o src/$(DLL).c -D $(EXPORT_CALL) -D $(PY_OPT) -I ./include
	$(CC) -o $(DLL).dll obj/$(DLL).o obj/$(DETAILS).o -s -shared -Wl,--subsystem,windows,--out-implib,lib\lib$(DLL).a

python-so: src/$(SO).c include/$(SO).h
	$(CC) $(CFLAGS) -c -o obj/$(SO).o -fPIC src/$(SO).c -D $(PY_OPT) -I./include
	$(CC) -o lib$(SO).so obj/$(SO).o -s -shared
	export LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH

dll: src/$(DLL).c include/$(DLL).h
	$(WIN_DETAILS) -i res/$(DETAILS).rc -o obj/$(DETAILS).o
	$(CC) $(CFLAGS) -c -o obj/$(DLL).o src/$(DLL).c -D $(EXPORT_CALL) -D -I.\include
	$(CC) -o $(DLL).dll obj/$(DLL).o obj/$(DETAILS).o -s -shared -Wl,--subsystem,windows,--out-implib,lib\lib$(DLL).a

so: src/$(SO).c include/$(SO).h
	$(CC) $(CFLAGS) -c -o obj/$(SO).o -fPIC src/$(SO).c -I./include
	$(CC) -o lib$(SO).so obj/$(SO).o -s -shared
	export LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH

exe-win: src/$(DLL).c include/$(DLL).h $(DLL).dll
	$(CC) -c -o obj/$(PROG).o src/$(PROG).c -I.\include 
	$(CC) -o $(PROG).exe -s obj/$(PROG).o -L. -l$(DLL)

exe-lin: src/$(SO).c include/$(SO).h lib$(SO).so
	$(CC) -c -o obj/$(PROG).o src/$(PROG).c -I./include 
	$(CC) -o $(PROG).exe -s obj/$(PROG).o -lm -L. -l$(SO)


.PHONY: clean-linux
clean-linux:
	rm -f obj/*.o *.exe *.so lib/*.a *.c
	rm -rf build

.PHONY: clean-windows
clean-windows:
	del *.exe
	del *.dll
	del *.pyd
	del *.pyc
	del obj\*.o
	del cython\*.c
	del lib\*.a

.PHONY: clean
clean: $(CLEANER)

