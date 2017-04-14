CC = gcc
CFLAGS = -std='c99' -g -Wall

SO  = add
PROG = add_test
DETAILS = details


all: $(SO).c
	$(CC) -c -o $(SO).o -fPIC $(SO).c
	$(CC) -o lib$(SO).so $(SO).o -shared
	$(CC) -o lib$(SO).a $(SO).o -shared
	$(CC) -c -o $(PROG).o $(PROG).c
	$(CC) -o $(PROG).exe -s $(PROG).o -L. -l$(SO)
	export LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH



.PHONY: clean
clean:
	rm -f *.o *.so *.a *.exe
