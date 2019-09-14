CC = gcc
CFLAGS = -g -Wall -std=c99

SRC = lpfgopt main
OUT = out.exe
EXTRA = -I./include

all:
	$(CC) $(CFLAGS) $(foreach var,$(SRC), ./csrc/$(var).c) -o $(OUT) $(EXTRA)

.PHONY: clean
clean:
	rm -f *.exe *.o *.so *.dll
