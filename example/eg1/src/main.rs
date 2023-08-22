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
        0xc6, 0x06, 0x00, 0x80, 0x00, /* movl $0, (0x8000); This generates a MMIO Write. */
        0x8a, 0x16, 0x00, 0x80, /* movl (0x8000), %dl; This generates a MMIO Read. */
        0xf4, /* hlt */
    ];

    // 1. Instantiate KVM
    let kvm: Kvm = Kvm::new().unwrap();

    // 2. Create a VM
    let vm: VmFd = kvm.create_vm().unwrap();

    // 3. Initialize guest memory
    let load_addr = unsafe {
        libc::mmap(
            null_mut(),
            mem_size,
            libc::PROT_READ | libc::PROT_WRITE,
            libc::MAP_ANONYMOUS | libc::MAP_SHARED | libc::MAP_NORESERVE,
            -1,
            0,
        )
    } as *mut u8;

    let slot = 0;
    // When initializing the guest memory slot specify the
    // `KVM_MEM_LOG_DIRTY_PAGES` to enable the dirty log.
    let mem_region = kvm_userspace_memory_region {
        slot,
        guest_phys_addr: guest_addr as u64,
        memory_size: mem_size as u64,
        userspace_addr: load_addr as u64,
        flags: KVM_MEM_LOG_DIRTY_PAGES,
    };
    unsafe {
        vm.set_user_memory_region(mem_region).unwrap();
    }

    // Write the code in the guest memory. This will generate a dirty page.
    unsafe {
        let mut slice = slice::from_raw_parts_mut(load_addr, mem_size);
        slice.write(&asm_code).unwrap();
    }

    // 4. Create a VCPU
    let vcpu_fd: VcpuFd = vm.create_vcpu(0).unwrap();

    // 5. Initialize general purpose and special registers.
    // x86_64 specific registers
    let mut vcpu_sregs = vcpu_fd.get_sregs().unwrap();
    vcpu_sregs.cs.base = 0;
    vcpu_sregs.cs.selector = 0;
    vcpu_fd.set_sregs(&vcpu_sregs).unwrap();

    let mut vcpu_regs = vcpu_fd.get_regs().unwrap();
    vcpu_regs.rip = guest_addr;
    vcpu_regs.rax = 2;
    vcpu_regs.rbx = 3;
    vcpu_regs.rflags = 2;
    vcpu_fd.set_regs(&vcpu_regs).unwrap();

    // 6. Run code on the vCPU
    loop {
        match vcpu_fd.run().expect("run failed") {
            VcpuExit::IoIn(addr, data) => {
                println!(
                    "Received an I/O in exit. Address: {:#x}. Data: {:#x}",
                    addr, data[0]
                );
            }
            VcpuExit::IoOut(addr, data) => {
                println!(
                    "Received an I/O out exit. Address: {:#x}. Data: {:#x}",
                    addr, data[0]
                );
            }
            VcpuExit::MmioRead(addr, data) => {
                println!(
                    "Received an MMIO read request for the Address: {:#x}.",
                    addr
                );
            }
            VcpuExit::MmioWrite(addr, adta) => {
                println!("Received an MMIO Write Request to the address {:#x}.", addr,);
                // The code snippet dirties 1 page when it is loaded in memory
                let dirty_pages_bitmap = vm.get_dirty_log(slot, mem_size).unwrap();
                let dirty_pages = dirty_pages_bitmap
                    .into_iter()
                    .map(|page| page.count_ones())
                    .fold(0, |dirty_page_count, i| dirty_page_count + i);
                assert_eq!(dirty_pages, 1);
                // Since on aarch64 there is not halt instruction,
                // we break immediately after the last known instruction
                // of the asm code example so that we avoid an infinite loop.
            }
            VcpuExit::Hlt => {
                println!("Received a HLT exit. Breaking out of the loop.");
                break;
            }
            r => panic!("Unexpected exit reason: {:?}", r),
        }
    }
}
