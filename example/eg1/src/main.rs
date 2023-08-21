extern crate kvm_ioctls;
extern crate kvm_bindings;

use std::io::Write;
use std::ptr::null_mut;
use std::slice;

use kvm_ioctls::VcpuExit;
use kvm_ioctls::{Kvm, VcpuFd, VmFd};

use kvm_bindings::kvm_userspace_memory_region;
use kvm_bindings::KVM_MEM_LOG_DIRTY_PAGES;

fn main() {
    let mem_size = 0x4000;
    let guest_addr = 0x1000;
    let asm_code: &[u8];

    // for x86_64 architecture
    asm_code = &[
        0xba, 0xf8, 0x03, /* mov $0x3f8, %dx */
        0x00, 0xd8, /* add %bl, %al */
        0x04, b'0', /* add $'0', %al */
        0xee, /* out %al, %dx */
        0xec, /* in %dx, %al */
        0xc6, 0x06, 0x00, 0x80,
        0x00, /* movl $0, (0x8000); This generates a MMIO Write. */
        0x8a, 0x16, 0x00, 0x80, /* movl (0x8000), %dl; This generates a MMIO Read. */
        0xf4, /* hlt */
    ];

    // Instantiate KVM
    let kvm = Kvm::new().unwrap();
    // Create a VM
    let vm = kvm.create_vm().unwrap();
}