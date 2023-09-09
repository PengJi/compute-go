#include <linux/kvm.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/mman.h>

struct vm {
    int vm_fd;
    __u64 ram_size;
    __u64 ram_start;
    struct kvm_userspace_memory_region mem;
    struct vcpu *vcpus[1];
};

struct vcpu {
    int id;
    int fd;
    struct kvm_run *run;
    struct kvm_regs regs;  // 通用寄存器，标志寄存器，包括：RAX, RBX, RCX, RDX, RSI, RDI, RSP, RBP, R8-R15, RIP, RFLAGS
    struct kvm_sregs sregs;  // special registers，包括段寄存器、控制寄存器等
};

int g_dev_fd;

int main(int argc, char **argv) {
    if((g_dev_fd = open("/dev/kvm", O_RDWR)) < 0) {
        fprintf(stderr, "Could not open /dev/kvm.\n");
        exit(1);
    }

    struct vm *vm = malloc(sizeof(struct vm));
    struct vcpu *vcpu = malloc(sizeof(struct vcpu));
    vcpu->id = 0;
    vm->vcpus[0] = vcpu;

    setup_vm(vm, 64*1024*1024);
    load_image(vm);
    run_vm(vm);

    return 0;
}

int setup_vm(struct vm *vm, int ram_size) {
    int ret = 0;

    // 创建虚拟机实例
    if((vm->vm_fd = ioctl(g_dev_fd, KVM_CREATE_VM, 0)) < 0) {
        fprintf(stderr, "Could not create vm.\n");
        ret = -1;
        goto err;
    }

    // 创建内存
    vm->ram_size = ram_size;
    // 使用 mmap 分配一段按照页面尺寸对齐的 64MB 的内存作为虚拟机的物理内存
    vm->ram_start = (__u64) mmap(NULL, vm->ram_size, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_NORESERVE, -1, 0);
    if((void *)vm->ram_start == MAP_FAILED) {
        fprintf(stderr, "Could not mmap ram.\n");
        ret = -1;
        goto err;
    }

    vm->mem.slot = 0;
    vm->mem.guest_phys_addr = 0;
    vm->mem.memory_size = vm->ram_size;
    vm->mem.userspace_addr = vm->ram_start;

    if(ioctl(vm->vm_fd, KVM_SET_USER_MEMORY_REGION, &(vm->mem)) < 0) {
        fprintf(stderr, "Could not set user memory region.\n");
        ret = -1;
        goto err;
    }

    // 创建处理器
    struct vcpu *vcpu = vm->vcpus[0];
    vcpu->fd = ioctl(vm->vm_fd, KVM_CREATE_VCPU, vcpu->id);
    if(vcpu->fd < 0) {
        fprintf(stderr, "Could not create vcpu.\n");
        ret = -1;
        goto err;
    }

    // 设置 sregs
    if(ioctl(vcpu->fd, KVM_GET_SREGS, &(vcpu->sregs)) < 0) {
        fprintf(stderr, "Could not get sregs.\n");
        ret = -1;
        goto err;
    }

    vcpu->sregs.cs.selector = 0x1000;  // 代码段选择子，将 guest 加载到段地址为 0x10000 的内存中
    vcpu->sregs.cs.base = 0x1000 << 4;
    if(ioctl(vcpu->fd, KVM_SET_SREGS, &(vcpu->sregs)) < 0) {
        fprintf(stderr, "Could not set sregs.\n");
        ret = -1;
        goto err;
    }

    // 设置 regs
    if(ioctl(vcpu->fd, KVM_GET_REGS, &(vcpu->regs)) < 0) {
        fprintf(stderr, "Could not get regs.\n");
        ret = -1;
        goto err;
    }
    vcpu->regs.rflags = 0x2;
    vcpu->regs.rip = 0x0;
    if(ioctl(vcpu->fd, KVM_SET_REGS, &(vcpu->regs)) < 0) {
        fprintf(stderr, "Could not set regs.\n");
        ret = -1;
        goto err;
    }

err:
    return ret;
}

// 将 guest 的代码加载到 guest 的内存地址 (0x1000 << 4) + 0x0 处
void load_image(struct vm *vm) {
    int res = 0;
    int fd = open("kernel.bin", O_RDONLY);
    if(fd < 0) {
        fprintf(stderr, "Could not open kernel.bin.\n");
        exit(1);
    }

    char *p = (char *)vm->ram_start + (0x1000 << 4) + 0x0;

    while(1) {
        if((res = read(fd, p, 4096)) < 0) break;
        p += res;
    }
}

// 运行虚拟机
void run_vm(struct vm *vm) {
    int res = 0;
    while(1) {
        if(ioctl(vm->vcpus[0]->fd, KVM_RUN, NULL) < 0) {
            fprintf(stderr, "Could not run vm.\n");
            exit(1);
        }
    }
}
