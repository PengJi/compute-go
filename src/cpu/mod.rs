// Copyright (c) 2020 Huawei Technologies Co.,Ltd. All rights reserved.
//
// StratoVirt is licensed under Mulan PSL v2.
// You can use this software according to the terms and conditions of the Mulan
// PSL v2.
// You may obtain a copy of Mulan PSL v2 at:
//         http://license.coscl.org.cn/MulanPSL2
// THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY
// KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
// NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
// See the Mulan PSL v2 for more details.

#[cfg(target_arch = "aarch64")]
mod aarch64;
#[cfg(target_arch = "x86_64")]
mod x86_64;

#[cfg(target_arch = "aarch64")]
pub use aarch64::AArch64CPUBootConfig as CPUBootConfig;
#[cfg(target_arch = "x86_64")]
pub use x86_64::X86CPUBootConfig as CPUBootConfig;

use std::sync::{Arc, Mutex};
use std::thread;

use kvm_ioctls::{VcpuExit, VcpuFd, VmFd};

use crate::device::{judge_serial_addr, Serial};
use crate::memory::GuestMemory;
#[cfg(target_arch = "aarch64")]
use aarch64::CPUState;
#[cfg(target_arch = "x86_64")]
use x86_64::CPUState;

pub struct CPU {
    /// ID of this virtual CPU, `0` means this cpu is primary `CPU`.
    pub id: u8,
    /// The file descriptor of this kvm_based vCPU.
    pub fd: VcpuFd,
    /// Registers state for kvm_based vCPU.
    pub state: CPUState,
    /// System memory space.
    sys_mem: Arc<GuestMemory>,
    /// Serial device is used for debugging.
    serial: Option<Arc<Mutex<Serial>>>,
}

impl CPU {
    /// Allocates a new `CPU` for `vm`
    ///
    /// # Arguments
    ///
    /// - `vcpu_id` - vcpu_id for `CPU`, started from `0`.
    #[allow(unused_variables)]
    pub fn new(vm_fd: &Arc<VmFd>, sys_mem: Arc<GuestMemory>, vcpu_id: u32, nr_vcpus: u32) -> Self {
        let vcpu_fd = vm_fd
            .create_vcpu(vcpu_id as u64)
            .expect("Failed to create vCPU");

        Self {
            id: vcpu_id as u8,
            fd: vcpu_fd,
            sys_mem,
            state: CPUState::new(
                vcpu_id,
                #[cfg(target_arch = "x86_64")]
                nr_vcpus,
            ),
            serial: None,
        }
    }

    pub fn set_serial_dev(&mut self, serial: Arc<Mutex<Serial>>) {
        self.serial = Some(serial);
    }

    /// Realize vcpu status.
    /// Get register state from kvm.
    pub fn realize(&mut self, vm_fd: &Arc<VmFd>, bootconfig: CPUBootConfig) {
        self.state.set_boot_config(vm_fd, &self.fd, &bootconfig);
    }

    /// Reset kvm_based vCPU registers state by registers state in `CPU`.
    pub fn reset(&self) {
        self.state.reset_vcpu(&self.fd);
    }

    /// Start run `CPU` in seperate vcpu thread.
    ///
    /// # Arguments
    ///
    /// - `arc_cpu`: `CPU` wrapper in `Arc` to send safely during thread.
    pub fn start(arc_cpu: Arc<CPU>) -> thread::JoinHandle<()> {
        let cpu_id = arc_cpu.id;
        thread::Builder::new()
            .name(format!("CPU {}/KVM", cpu_id))
            .spawn(move || {
                arc_cpu.reset();
                loop {
                    if !arc_cpu.kvm_vcpu_exec() {
                        break;
                    }
                }
            })
            .expect(&format!("Failed to create thread for CPU {}/KVM", cpu_id))
    }

    /// Run kvm vcpu emulation.
    ///
    /// # Return value
    ///
    /// Whether to continue to emulate or not.
    fn kvm_vcpu_exec(&self) -> bool {
        match self.fd.run().expect("Unhandled error in vcpu emulation!") {
            VcpuExit::IoIn(addr, data) => {
                if let Some(offset) = judge_serial_addr(addr as u64) {
                    data[0] = self.serial.as_ref().unwrap().lock().unwrap().read(offset);
                }
            }
            VcpuExit::IoOut(addr, data) => {
                if let Some(offset) = judge_serial_addr(addr as u64) {
                    if self
                        .serial
                        .as_ref()
                        .unwrap()
                        .lock()
                        .unwrap()
                        .write(offset, data[0])
                        .is_err()
                    {
                        println!("Failed to write data for serial, offset: {}", offset);
                    }
                }
            }
            VcpuExit::MmioRead(addr, mut data) => {
                if let Some(offset) = judge_serial_addr(addr as u64) {
                    data[0] = self.serial.as_ref().unwrap().lock().unwrap().read(offset);
                } else {
                    let data_len = data.len() as u64;
                    self.sys_mem
                        .read(&mut data, addr as u64, data_len)
                        .expect("Invalid mmio read.");
                }
            }
            VcpuExit::MmioWrite(addr, mut data) => {
                if let Some(offset) = judge_serial_addr(addr as u64) {
                    if self
                        .serial
                        .as_ref()
                        .unwrap()
                        .lock()
                        .unwrap()
                        .write(offset, data[0])
                        .is_err()
                    {
                        println!("Failed to write data for serial, offset: {}", offset);
                    }
                } else {
                    let data_len = data.len() as u64;
                    self.sys_mem
                        .write(&mut data, addr as u64, data_len)
                        .expect("Invalid mmio write.");
                }
            }
            VcpuExit::Hlt => {
                println!("KVM_EXIT_HLT");
                return false;
            }
            VcpuExit::Shutdown => {
                println!("Guest shutdown");

                return false;
            }
            r => panic!("Unexpected exit reason: {:?}", r),
        }

        true
    }
}
