#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/wait.h>
#include <linux/poll.h>
#include <linux/sched.h>
#include <linux/slab.h>

#define BUFFER_MAX    (10)
#define OK            (0)
#define ERROR         (-1)

struct cdev *gDev;
struct file_operations *gFile;
dev_t  devNum;
unsigned int subDevNum = 1;

int reg_major  =  232;  // 主设备号
int reg_minor =   0;  // 从设备号

char *buffer;
int flag = 0;

int hello_open(struct inode *p, struct file *f)
{
    printk(KERN_EMERG "hello_open\r\n");
    return 0;
}

ssize_t hello_write(struct file *f, const char __user *u, size_t s, loff_t *l)
{
    printk(KERN_EMERG "hello_write\r\n");
    return 0;
}

ssize_t hello_read(struct file *f, char __user *u, size_t s, loff_t *l)
{
    printk(KERN_EMERG "hello_read\r\n");      
    return 0;
}

int hello_init(void)
{
    devNum = MKDEV(reg_major, reg_minor);  // 根据主设备号和从设备号生成 devNum，唯一标识一个设备
    if(OK == register_chrdev_region(devNum, subDevNum, "helloworld")) {  // 向内核注册设备号
        printk(KERN_EMERG "register chrdev region ok \n"); 
    } else {
        printk(KERN_EMERG "register chrdev region error n");
        return ERROR;
    }

    printk(KERN_EMERG "hello driver init \n");

    gDev = kzalloc(sizeof(struct cdev), GFP_KERNEL);  // 字符设备
    gFile = kzalloc(sizeof(struct file_operations), GFP_KERNEL);  // 文件操作
    gFile->open = hello_open;
    gFile->read = hello_read;
    gFile->write = hello_write;
    gFile->owner = THIS_MODULE;

    cdev_init(gDev, gFile);  // 建立字符设备和文件的联系
    cdev_add(gDev, devNum, 1);  // 建立字符设备和设备号的联系

    return 0;
}

void __exit hello_exit(void)
{
    cdev_del(gDev);
    unregister_chrdev_region(devNum, subDevNum);
    return;
}

module_init(hello_init);  // 驱动入口函数，执行 insmod 时被调用
module_exit(hello_exit);  // 驱动删除函数，执行 rmmod 时被调用
MODULE_LICENSE("GPL");
