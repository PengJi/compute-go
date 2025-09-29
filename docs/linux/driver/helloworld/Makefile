# 当执行 make 的时候会执行两次下面的代码，第一次是 else 部分的代码，第二次是 if 部分代码
# 最终生成一个 .ko 的配置文件

# 内核中定义了 KERNELRELEASE
ifneq ($(KERNELRELEASE),)
# 把 helloworld_dev.c 编译成 helloworld_dev.c
obj-m := helloworld_dev.o
else
PWD := $(shell pwd)
# 内核头文件的目录
# KDIR:= /lib/modules/4.4.0-31-generic/build
KDIR := /lib/modules/`uname -r`/build

all:
# -C 表示进入内核目录
	make -C $(KDIR) M=$(PWD)

clean:	
	rm -rf *.o *.ko *.mod.c *.symvers *.c~ *~

endif
