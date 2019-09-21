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

SRC = lpfgopt main
OUT = out.exe
EXTRA = -I./include

all:
	$(CC) $(CFLAGS) $(foreach var,$(SRC), ./csrc/$(var).c) -o $(OUT) $(EXTRA)


.PHONY: clean-linux
clean-linux:
	rm -f *.o *.exe *.so *.dll

.PHONY: clean-windows
clean-windows:
	del *.exe
	del *.dll
	del *.o
	del *.so


.PHONY: clean
clean: $(CLEANER)
