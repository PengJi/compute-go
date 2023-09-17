BIN := kernel.bin
ELF := kernel.elf
OBJ := kernel.o

all: $(BIN) kvm run

.PHONY: kvm
kvm:
	gcc kvm.c -o kvm

$(BIN): $(ELF)
	objcopy -O binary $< $@

$(ELF): $(OBJ)
	$(LD) -Ttext 0x00 -nostdlib -static $< -o $@

%.o: %.S
	$(CC) -nostdinc -c $< -o $@

.PHONY: run
run:
	./kvm

.PHONY: clean
clean:
	rm -f kvm $(BIN) $(ELF) $(OBJ)
