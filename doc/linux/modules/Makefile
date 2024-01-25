obj-m := gpt-dump.o
PWD := $(shell pwd)
KDIR := /lib/modules/$(shell uname -r)/build

all:
	make -C $(KDIR) M=$(PWD)
clean:
	make -C $(KDIR) M=$(PWD) clean