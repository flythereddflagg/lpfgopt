# For linux
CC = gcc
CFLAGS = -std='c99' -g -Wall

SO  = lpfg
PROG = lpfg_test
PY_OPT = PY_EXPORTS


all: python-so exe


python-so: src/$(SO).c include/$(SO).h
	$(CC) $(CFLAGS) -c -o obj/$(SO).o -fPIC src/$(SO).c -D $(PY_OPT) -I./include
	$(CC) -o lib$(SO).so obj/$(SO).o -s -shared
	export LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH


so: src/$(SO).c include/$(SO).h
	$(CC) $(CFLAGS) -c -o obj/$(SO).o -fPIC src/$(SO).c -I./include
	$(CC) -o lib$(SO).so obj/$(SO).o -s -shared
	export LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH


exe: src/$(SO).c include/$(SO).h lib$(SO).so
	$(CC) -c -o obj/$(PROG).o src/$(PROG).c -I./include 
	$(CC) -o $(PROG).exe -s obj/$(PROG).o -lm -L. -l$(SO)


.PHONY: clean
clean:
	rm -f obj/*.o *.exe *.so lib/*.a

