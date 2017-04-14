CC = gcc
CFLAGS = -std='c99' -g -Wall
WIN_DETAILS = windres

DLL  = add
PROG = add_test
DETAILS = details


all: $(DLL).c
	$(WIN_DETAILS) -i $(DETAILS).rc -o $(DETAILS).o
	$(CC) -c -o $(DLL).o $(DLL).c -D ADD_EXPORTS
	$(CC) -o $(DLL).dll $(DLL).o $(DETAILS).o -s -shared -Wl,--subsystem,windows,--out-implib,lib$(DLL).a
	$(CC) -c -o $(PROG).o $(PROG).c
	$(CC) -o $(PROG).exe -s $(PROG).o -L. -l$(DLL)


.PHONY: clean
clean:
	del *.o
	del *.exe
	del *.dll
	del *.a