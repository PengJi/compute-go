use kvm_bindings::{kvm_userspace_memory_region, KVM_MAX_CPUID_ENTRIES, KVM_MEM_LOG_DIRTY_PAGES};
use kvm_ioctls::{Kvm, VcpuFd, VmFd};
use vm_memory::{Bytes, GuestAddress, GuestMemory, GuestMemoryMmap};

