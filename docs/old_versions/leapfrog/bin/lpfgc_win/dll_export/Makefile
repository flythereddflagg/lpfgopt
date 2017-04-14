# For windows
CC = gcc
CFLAGS = -std='c99' -g -Wall
WIN_DETAILS = windres

DLL  = lpfg
PROG = lpfg_test
DETAILS = details
EXPORT_CALL = LPFG_EXPORTS
PY_OPT = PY_EXPORTS


all: python-dll exe


python-dll: src/$(DLL).c include/$(DLL).h
	$(WIN_DETAILS) -i res/$(DETAILS).rc -o obj/$(DETAILS).o
	$(CC) $(CFLAGS) -c -o obj/$(DLL).o src/$(DLL).c -D $(EXPORT_CALL) -D $(PY_OPT) -I.\include
	$(CC) -o $(DLL).dll obj/$(DLL).o obj/$(DETAILS).o -s -shared -Wl,--subsystem,windows,--out-implib,lib\lib$(DLL).a

dll: src/$(DLL).c include/$(DLL).h
	$(WIN_DETAILS) -i res/$(DETAILS).rc -o obj/$(DETAILS).o
	$(CC) $(CFLAGS) -c -o obj/$(DLL).o src/$(DLL).c -D $(EXPORT_CALL) -D -I.\include
	$(CC) -o $(DLL).dll obj/$(DLL).o obj/$(DETAILS).o -s -shared -Wl,--subsystem,windows,--out-implib,lib\lib$(DLL).a


exe: src/$(DLL).c include/$(DLL).h $(DLL).dll
	$(CC) -c -o obj/$(PROG).o src/$(PROG).c -I.\include 
	$(CC) -o $(PROG).exe -s obj/$(PROG).o -L. -l$(DLL)


.PHONY: clean
clean:
	del obj\*.o
	del *.exe
	del *.dll
	del lib\*.a