use std::path::PathBuf;

use kvm_bindings::{kvm_regs, kvm_sregs, kvm_userspace_memory_region};
use kvm_ioctls::{Kvm, VcpuFd, VmFd};
use libc::{c_void, mmap, MAP_ANONYMOUS, MAP_NORESERVE, MAP_SHARED, PROT_READ, PROT_WRITE};

extern crate kvm_bindings;
extern crate kvm_ioctls;
extern crate libc;

struct Vm {
    kvm: Kvm,
    vm: VmFd,
    hva_ram_start: usize;
    vcpu: Option<Vcpu>,
}
