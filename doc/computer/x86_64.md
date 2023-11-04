x86架构寄存器：
* 通用寄存器  
![general purpose registers](./images/general_purpose_registers.jpg)  
`%rax` 通常用于存储函数调用的返回结果，同时也用于乘法和除法指令中。
在imul 指令中，两个64位的乘法最多会产生128位的结果，需要 %rax 与 %rdx 共同存储乘法结果，在div 指令中被除数是128 位的，同样需要%rax 与 %rdx 共同存储被除数。  
`%rsp` 是堆栈指针寄存器，通常会指向栈顶位置，堆栈的 pop 和push 操作就是通过改变 %rsp 的值即移动堆栈指针的位置来实现的。  
`%rbp` 是栈帧指针，用于标识当前栈帧的起始位置。  
`%rdi, %rsi, %rdx, %rcx,%r8, %r9` 六个寄存器用于存储函数调用时的6个参数（如果有6个或6个以上参数的话）。  
被标识为 “miscellaneous registers” 的寄存器，属于通用性更为广泛的寄存器，编译器或汇编程序可以根据需要存储任何数据。  
区分一下 “Caller Save” 和 ”Callee Save” 寄存器，即寄存器的值是由”调用者保存“ 还是由 ”被调用者保存“。当产生函数调用时，子函数内通常也会使用到通用寄存器，那么这些寄存器中之前保存的调用者(父函数）的值就会被覆盖。为了避免数据覆盖而导致从子函数返回时寄存器中的数据不可恢复，CPU 体系结构中就规定了通用寄存器的保存方式。
如果一个寄存器被标识为”Caller Save”， 那么在进行子函数调用前，就需要由调用者提前保存好这些寄存器的值，保存方法通常是把寄存器的值压入堆栈中，调用者保存完成后，在被调用者（子函数）中就可以随意覆盖这些寄存器的值了。如果一个寄存被标识为“Callee Save”，那么在函数调用时，调用者就不必保存这些寄存器的值而直接进行子函数调用，进入子函数后，子函数在覆盖这些寄存器之前，需要先保存这些寄存器的值，即这些寄存器的值是由被调用者来保存和恢复的。


* Flags 寄存器
* 段寄存器
* 控制寄存器
* MSR(Model-Specific Registers)

VMCS
[Basic concepts in Intel VT-x](https://docs.hyperdbg.org/tips-and-tricks/considerations/basic-concepts-in-intel-vt-x)  
![guest state area/host state area](./images/vmcs1.jpg)
![control fileds/vm exit control fileds](./images/vmcs2.jpg)

参考
[How many registers does an x86-64 CPU have?](https://blog.yossarian.net/2020/11/30/How-many-registers-does-an-x86-64-cpu-have)  
