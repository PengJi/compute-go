all: bin kvm run

.PHONY: bin
bin:
	@echo "====== Compile the test.S ======"
	as -32 test.S -o test.o
	objcopy -O binary test.o test.bin
	@echo "====== end ======"

.PHONY: kvm
kvm: kvm.o
	@echo "====== Compile the kvm.c ======"
	$(CC) $(CFLAGS) -o $@ $^
	@echo "====== end ======"

.PHONY: run
run:
	@echo "====== Run the kvm ======"
	./kvm
	@echo "====== end ======"

.PHONY: clean
clean:
	@echo "====== Clean the files ======"
	rm -rf *.o kvm test.bin
	@echo "====== end ======"
