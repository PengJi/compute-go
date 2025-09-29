**mmap**  
* 作用：`mmap` 能将一个磁盘文件映射到存储空间中的一个缓冲区上。
当想缓冲区中取数据时，就相当于读文件中的相应字节，将数据存入缓冲区时，相应字节就自动写入文件。
这样，就可以在不使用 read 和 write 的情况下执行 I/O。
* 头文件：`#include<sys/mmap.h>`
* 函数签名：`void *mmap(void *addr, size_t len, int prot, int flags, int fd, off_t off)`
* 参数：
    * `addr` 用于指定映射存储区的起始地址。通常将其设置为0，这表示有系统选择该映射区的起始地址。
    * `len` 映射的字节数。
    * `prot` 指定映射区的保护要求，包含如下值：
        * `PROT_READ` 映射区可读
        * `PROT_WRITE`映射区可写
        * `PROT_EXEC` 映射区可执行
        * `PROT_NONE` 映射区不可访问
    * `flags` 设置映射存储区的属性
        * `MAP_FIXED`  返回值必须等于 addr。如果未指定此标志，而且 addr 非0，则内核只把 addr 视为在何处设置映射区的一种建议，但不保证会使用所要求的的地址。将 addr 指定为 0 可以获得最大可移植性。
        * `MAP_SHARED`  这一标志描述了本进程对映射区所进行的存储操作的配置。此标志指定存储操作修改映射文件，也就是，存储操作相当于对该文件的 write。
        * `MAP_PRIVATE`  本标志说明对映射区的存储操作导致创建该映射文件的衣蛾私有副本，所有后来对该映射区的引用都是引用该副本。（此标志的一种用途是用于调试程序，它将程序文件的正文部分映射至存储区，但允许用户修改其中的指令，任何修改只影响程序文件的副本，而不影响源文件。）
    * `fd` 指定要被映射文件的描述符。在文件映射地到地址空间之前，必须先打开该文件（open 函数返回）。
    * `off` 要映射字节在文件中的起始偏移量，大小为 PAGE_SIZE 的整数倍。

    > 注意事项：  
    > 1. 可将 `prot` 参数指定为 PROT_NONE、PROT_READ或其他值的任意组合的按位或。
    > 2. 对存储映射区指定 prot 保护要求不能超过 open 模式访问权限。例如：若文件是只读打开的，那么对存储映射区就不能指定 `PROT_WRITE`。
    > 3. off 的值和 addr 的值（如果指定了 MAP_FIXED）通常被要求是系统虚拟存储页长度的整数倍。
* 返回值
映射区的起始地址，即被映射区的指针，表示需要映射的内核空间在用户空间的虚拟地址。

**应用**  
（1）使用 mmap 复制文件（类似于 cp 命令）
```c
#include "apue.h"
#include <fcntl.h>
#include <sys/mman.h>

#define COPYINCR (1024*1024*1024)   /* 1 GB */

int
main(int argc, char *argv[])
{
    int         fdin, fdout;
    void        *src, *dst;
    size_t      copysz;
    struct stat sbuf;
    off_t       fsz = 0;

    if (argc != 3)
        err_quit("usage: %s <fromfile> <tofile>", argv[0]);

    if ((fdin = open(argv[1], O_RDONLY)) < 0)
        err_sys("can't open %s for reading", argv[1]);

    if ((fdout = open(argv[2], O_RDWR | O_CREAT | O_TRUNC, FILE_MODE)) < 0)
        err_sys("can't creat %s for writing", argv[2]);

    if (fstat(fdin, &sbuf) < 0)         /* need size of input file */
        err_sys("fstat error");

    if (ftruncate(fdout, sbuf.st_size) < 0) /* set output file size */
        err_sys("ftruncate error");

    while (fsz < sbuf.st_size) {
        if ((sbuf.st_size - fsz) > COPYINCR)
            copysz = COPYINCR;
        else
            copysz = sbuf.st_size - fsz;

        if ((src = mmap(0, copysz, PROT_READ, MAP_SHARED, fdin, fsz)) == MAP_FAILED)
            err_sys("mmap error for input");
        if ((dst = mmap(0, copysz, PROT_READ | PROT_WRITE, MAP_SHARED, fdout, fsz)) == MAP_FAILED)
            err_sys("mmap error for output");

        memcpy(dst, src, copysz);   /* does the file copy */
        munmap(src, copysz);
        munmap(dst, copysz);
        fsz += copysz;
    }
    exit(0);
}
```

（2）在驱动与应用中使用 mmap
驱动程序配置一页大小的内存，用于进程通过 mmap 将大小为一页的内存映射到内核空间的页上。
映射完成后，驱动程序想映射区写10个字节的数据，用户进程将数据读出来。

编写驱动程序
```c
#include <linux/miscdevice.h>
#include <linux/delay.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/init.h>
#include <linux/mm.h>
#include <linux/fs.h>
#include <linux/types.h>
#include <linux/delay.h>
#include <linux/moduleparam.h>
#include <linux/slab.h>
#include <linux/errno.h>
#include <linux/ioctl.h>
#include <linux/cdev.h>
#include <linux/string.h>
#include <linux/list.h>
#include <linux/pci.h>
#include <linux/gpio.h>

#define DEVICE_NAME "mymap"
 
static unsigned char array[10]={0,1,2,3,4,5,6,7,8,9};
static unsigned char *buffer;
  
static int my_open(struct inode *inode, struct file *file)
{
    return 0;
} 
 
static int my_map(struct file *filp, struct vm_area_struct *vma)
{    
    unsigned long page;
    unsigned char i;
    unsigned long start = (unsigned long)vma->vm_start;
    //unsigned long end =  (unsigned long)vma->vm_end;
    unsigned long size = (unsigned long)(vma->vm_end - vma->vm_start);
 
    // 得到物理地址
    page = virt_to_phys(buffer);

    // 将用户空间的一个 vma 虚拟内存区映射到以 page 开始的一段连续物理页面上
    if(remap_pfn_range(vma, start, page >> PAGE_SHIFT, size, PAGE_SHARED))  //第三个参数是页帧号，由物理地址右移PAGE_SHIFT得到
        return -1;
 
    // 往该内存写10字节数据
    for(i = 0; i < 10; i++)
        buffer[i] = array[i];
     
    return 0;
}
 
static struct file_operations dev_fops = {
    .owner    = THIS_MODULE,
    .open    = my_open,
    .mmap   = my_map,
};
 
static struct miscdevice misc = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = DEVICE_NAME,
    .fops = &dev_fops,
};
  
static int __init dev_init(void)
{
    int ret;    

    //注册混杂设备
    ret = misc_register(&misc);

    //内存分配
    buffer = (unsigned char *)kmalloc(PAGE_SIZE,GFP_KERNEL);

    //将该段内存设置为保留
    SetPageReserved(virt_to_page(buffer));
 
    return ret;
}
  
static void __exit dev_exit(void)
{
    //注销设备
    misc_deregister(&misc);

    //清除保留
    ClearPageReserved(virt_to_page(buffer));

    //释放内存
    kfree(buffer);
}
 
 
module_init(dev_init);
module_exit(dev_exit);
MODULE_LICENSE("GPL");
MODULE_AUTHOR("LKN@SCUT");
```

用户程序读取驱动数据
```c
#include <unistd.h>  
#include <stdio.h>  
#include <stdlib.h>  
#include <string.h>  
#include <fcntl.h>  
#include <linux/fb.h>  
#include <sys/mman.h>  
#include <sys/ioctl.h>   
  
#define PAGE_SIZE 4096  
  
  
int main(int argc , char *argv[])  
{  
    int fd;  
    int i;  
    unsigned char *p_map;  
      
    //打开设备  
    fd = open("/dev/mymap",O_RDWR);  
    if(fd < 0)  
    {  
        printf("open fail\n");  
        exit(1);  
    }  
  
    //内存映射  
    p_map = (unsigned char *)mmap(0, PAGE_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);  
    if(p_map == MAP_FAILED)
    {  
        printf("mmap fail\n");  
        goto here;  
    }  
  
    //打印映射后的内存中的前10个字节内容  
    for(i = 0; i < 10; i++)  
        printf("%d\n",p_map[i]);  

here:  
    munmap(p_map, PAGE_SIZE);  
    return 0;  
}
```

（3）进程间共享内存
进程a代码
```c
#include <sys/mman.h>  
#include <sys/stat.h>  
#include <fcntl.h>  
#include <stdio.h>  
#include <stdlib.h>  
#include <unistd.h>  
#include <error.h>  
  
#define BUF_SIZE 100  
  
int main(int argc, char **argv)  
{
    int fd, nread, i;
    struct stat sb;
    char *mapped, buf[BUF_SIZE];
  
    for (i = 0; i < BUF_SIZE; i++) {
        buf[i] = '#';
    }

    /* 打开文件 */  
    if ((fd = open(argv[1], O_RDWR)) < 0) {
        perror("open");
    }
  
    /* 获取文件的属性 */  
    if ((fstat(fd, &sb)) == -1) {
        perror("fstat");
    }  
  
    /* 将文件映射至进程的地址空间 */  
    if ((mapped = (char *)mmap(NULL, sb.st_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0)) == (void *)-1) {
        perror("mmap");
    }
  
    /* 文件已在内存, 关闭文件也可以操纵内存 */
    close(fd);
      
    /* 每隔两秒查看存储映射区是否被修改 */
    while (1) {
        printf("%s\n", mapped);
        sleep(2);
    }

    return 0;
}
```

进程b代码
```c
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <error.h> 

#define BUF_SIZE 100

int main(int argc, char **argv)
{
    int fd, nread, i;
    struct stat sb;
    char *mapped, buf[BUF_SIZE];

    for (i = 0; i < BUF_SIZE; i++) {
        buf[i] = '#';
    }
  
    /* 打开文件 */
    if ((fd = open(argv[1], O_RDWR)) < 0) {
        perror("open");
    }
  
    /* 获取文件的属性 */
    if ((fstat(fd, &sb)) == -1) {  
        perror("fstat");  
    }  
  
    /* 私有文件映射将无法修改文件 */  
    if ((mapped = (char *)mmap(NULL, sb.st_size, PROT_READ | PROT_WRITE, MAP_PRIVATE, fd, 0)) == (void *)-1) {
        perror("mmap");
    }
  
    /* 映射完后, 关闭文件也可以操纵内存 */
    close(fd);
  
    /* 修改一个字符 */
    mapped[20] = '9';
   
    return 0;  
}
```

（4）匿名映射实现父子进程通信
```c
#include <sys/mman.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define BUF_SIZE 100

int main(int argc, char** argv)
{
    char *p_map;

    /* 匿名映射,创建一块内存供父子进程通信 */
    p_map = (char *)mmap(NULL, BUF_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);

    if(fork() == 0) {
        sleep(1);
        printf("child got a message: %s\n", p_map);
        sprintf(p_map, "%s", "hi, dad, this is son");
        munmap(p_map, BUF_SIZE);  //实际上，进程终止时，会自动解除映射。
        exit(0);
    }

    sprintf(p_map, "%s", "hi, this is father");
    sleep(2);
    printf("parent got a message: %s\n", p_map);

    return 0;
}
```
输出：
```
child got a message: hi, this is father
parent got a message: hi, dad, this is son
```

《UNIX环境高级编程（第3版）》  
[brandongooch/apue.3e](https://github.com/brandongooch/apue.3e)  
[mmap详解](https://nieyong.github.io/wiki_cpu/mmap%E8%AF%A6%E8%A7%A3.html#toc_0.1)  
[认真分析mmap：是什么 为什么 怎么用 ](https://www.cnblogs.com/huxiao-tee/p/4660352.html)  
