BIN := kernel.bin
ELF := kernel.elf
OBJ := kernel.o

all:
	as -32 kernel.S -o $(OBJ)
	objcopy -O binary $(OBJ) $(BIN)

clean:
	rm -f $(BIN) $(ELF) $(OBJ)
