use kvm_bindings::{
    kvm_userspace_memory_region, KVM_MAX_CPUID_ENTRIES, KVM_MEM_LOG_DIRTY_PAGES,
};
use kvm_ioctls::Kvm;
use vm_memory::{GuestAddress, GuestMemoryMmap};

const MEMORY_SIZE: usize = 0x4000;

fn main() {
    // create vm
    let kvm = Kvm::new().expect("failed to create kvm");
    let vm = kvm.create_vm().expect("failed to create vm");

    // create memory
    let guest_addr = GuestAddress(0x0);
    let guest_mem = GuestMemoryMmap::<()>::from_ranges(&[(guest_addr, MEMORY_SIZE)])
        .expect("failed to create guest memory");
    let host_addr = guest_mem.get_host_address(guest_addr).unwrap();
    let mem_region = kvm_userspace_memory_region {
        slot: 0,
        guest_phys_addr: 0,
        memory_size: MEMORY_SIZE as u64,
        userspace_addr: host_addr as u64,
        flags: KVM_MEM_LOG_DIRTY_PAGES,
    };

    unsafe {
        vm.set_user_memory_region(mem_region)
            .expect("failed to set user memory region");
    };

    // create vcpu and set cpuid
    let vcpu = vm.create_vcpu(0).expect("failed to create vcpu");
    let kvm_cpuid = kvm.get_supported_cpuid(KVM_MAX_CPUID_ENTRIES).unwrap();
    vcpu.set_cpuid2(&kvm_cpuid).unwrap();

    // set regs
    let mut regs = vcpu.get_regs().unwrap();
    regs.rip = 0;
    regs.rflags = 2;
    vcpu.set_regs(&regs).unwrap();

    // set sregs
    let mut sregs = vcpu.get_sregs().unwrap();
    sregs.cs.selector = 0;
    sregs.cs.base = 0;
    vcpu.set_sregs(&sregs).unwrap();

    // copy code
    // B84200            mov ax,0x42
    // 3EA30010          mov [ds:0x1000],ax
    // F4                hlt
    let code = [0xb8, 0x42, 0x00, 0x3e, 0xa3, 0x00, 0x10, 0xf4];
    guest_mem.write_sclie(&code, GuestAddress(0x0)).unwrap();
    let reason = vcpu.run().unwrap();
    let regs = vcpu.get_regs().unwrap();
    println!("exit reason: {:?}", reason);
    println!("rax: {:x}, rip: {:X?}", regs.rax, regs.rip);
    println!(
        "memory at 0x10000: 0x{:X}",
        guest_mem.read_obj::<u16>(GuestAddress(0x1000)).unwrap()
    );
}
