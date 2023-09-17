use std::path::PathBuf;

use kvm_bindings::kvm_userspace_memory_region;
use kvm_ioctls::{Kvm, VcpuFd, VmFd};
use libc::{c_void, mmap, MAP_ANONYMOUS, MAP_SHARED, PROT_READ, PROT_WRITE};

struct Vm {
    kvm: Kvm,
    vm: VmFd,
    hva_ram_start: usize,
    vcpu: Option<VcpuFd>,
}

impl Vm {
    pub fn new() -> Self {
        let kvm = Kvm::new().unwrap();
        let vm = kvm.create_vm().unwrap();
        Vm {
            kvm: kvm,
            vm: vm,
            hva_ram_start: 0,
            vcpu: None,
        }
    }

    fn setup_memroy(&mut self, ram_size: usize) {
        // 大小按照 4096 对齐
        let ram_size = (ram_size + 0xfff) & !0xfff;

        // 分配内存
        let ptr = unsafe {
            mmap(
                0 as *mut c_void,
                ram_size,
                PROT_READ | PROT_WRITE,
                MAP_SHARED | MAP_ANONYMOUS,
                -1,
                0,
            )
        };
        if ptr == libc::MAP_FAILED {
            panic!("mmap failed");
        }

        self.hva_ram_start = ptr as usize;
        let mem_region = kvm_userspace_memory_region {
            slot: 0,
            guest_phys_addr: 0 as u64,
            memory_size: ram_size as u64,
            userspace_addr: ptr as u64,
            flags: 0,
        };
        unsafe {
            self.vm.set_user_memory_region(mem_region).unwrap();
        }
    }

    fn setup_cpu(&mut self) {
        let vcpu = self.vm.create_vcpu(0).unwrap();
        self.vcpu = Some(vcpu);

        let mut vcpu_sregs = self
            .vcpu
            .as_ref()
            .unwrap()
            .get_sregs()
            .expect("get sregs failed");
        vcpu_sregs.cs.base = 0;
        vcpu_sregs.cs.selector = 0;
        self.vcpu
            .as_ref()
            .unwrap()
            .set_sregs(&vcpu_sregs)
            .expect("set sregs failed");
        let mut vcpu_regs = self
            .vcpu
            .as_ref()
            .unwrap()
            .get_regs()
            .expect("get regs failed");
        vcpu_regs.rax = 0;
        vcpu_regs.rbx = 0;
        vcpu_regs.rip = 0;
        self.vcpu
            .as_ref()
            .unwrap()
            .set_regs(&vcpu_regs)
            .expect("set regs failed");
    }

    fn load_image(&mut self, image: PathBuf) {
        let kernel = std::fs::read(image).unwrap();
        println!("kernel size: {:?}", kernel);
        let ptr = (self.hva_ram_start) as *mut u8;
        println!(
            "self.hva_ram_start: {:p}, ptr={ptr:?}",
            self.hva_ram_start as *mut u8
        );
        unsafe {
            std::ptr::copy_nonoverlapping(kernel.as_ptr(), ptr, kernel.len());
        }
    }

    fn run(&mut self) {
        let vcpu = self.vcpu.as_mut().unwrap();
        loop {
            match vcpu.run().expect("run failed") {
                kvm_ioctls::VcpuExit::Hlt => {
                    println!("Hlt");
                    std::thread::sleep(std::time::Duration::from_millis(1000));
                }
                kvm_ioctls::VcpuExit::IoOut(port, data) => {
                    println!("IoOut: port={:?}, data={:?}", port, data);
                }
                kvm_ioctls::VcpuExit::FailEntry(reason, vcpu) => {
                    println!("FailEntry: reason={:?}, vcpu={:?}", reason, vcpu);
                    break;
                }
                _ => {
                    print!("other exit");
                    break;
                }
            }
        }
    }
}

fn main() {
    let image = PathBuf::from("kernel.bin");
    let mut vm = Vm::new();
    let mem_size = 0x1000;
    vm.setup_memroy(mem_size);
    vm.setup_cpu();
    vm.load_image(image);
    vm.run();
}
