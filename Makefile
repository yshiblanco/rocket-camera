# Compiler stuff
CC = gcc
CFLAGS = -I.

# C header and source files
C_FILES = client_socket.c main.c
DEPS = client_socket.h
C_OBJS = $(C_FILES:.c=.o)				# List of .o files converted from the .c files (just for naming)

# Python files
PY_FILES = socketserver_1.py

# Compile .c into .o
%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

# Link object files into executable
build: $(C_OBJS)
	$(CC) -o main $^

# Run C code
run_c: build
	./main

# Run Python code
run_py:
	python3 $(PY_FILES)

clean:
	rm -f *.o main
