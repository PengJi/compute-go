all: kvm test.bin run

.PHONY: kvm
kvm: main.o
	gcc main.c -o kvm -lpthread

test.bin: test.o
	ld -m elf_i386 --oformat binary -N -e _start -Ttext 0x10000 -o test.bin test.o

test.o: test.S
	as -32 test.S -o test.o

.PHONY: run
run:
	./kvm

.PHONY: clean
clean:
	rm -rf *.o kvm test.bin
