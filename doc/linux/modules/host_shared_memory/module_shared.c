#include <linux/module.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>
#include <linux/vmalloc.h>

#define DEVICE_NAME "my_shared_mem"

static int major;
static dev_t dev_num;
static struct cdev my_cdev;
static char *shared_memory;
static const int shared_memory_size = PAGE_SIZE;  // 分配一页内存

// 新增：用于写入共享内存的函数
void write_to_shared_memory(const char *data, size_t size) {
    if (size > shared_memory_size) {
        size = shared_memory_size;
    }
    memcpy(shared_memory, data, size);
    printk("shared memory data: %s\n", shared_memory);
}

EXPORT_SYMBOL(write_to_shared_memory);

static int my_mmap(struct file *file, struct vm_area_struct *vma) {
    return remap_vmalloc_range(vma, shared_memory, 0);
}


static ssize_t device_read(struct file *filp, char __user *buffer, size_t length, loff_t *offset) {
    int bytes_read = 0;
    const char *shared_mem_ptr = shared_memory + *offset;

    // 检查偏移量
    if (*offset >= shared_memory_size) {
        return 0;  // 已到达内存末尾
    }

    // 读取数据到用户空间
    while (length && *offset < shared_memory_size) {
        put_user(*(shared_mem_ptr++), buffer++);
        length--;
        bytes_read++;
        (*offset)++;
    }

    return bytes_read;
}

static const struct file_operations my_fops = {
    .owner = THIS_MODULE,
    .mmap = my_mmap,
    .read = device_read,
};

static int __init my_module_init(void) {
    int ret;

    ret = alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME);
    if (ret < 0) {
        printk(KERN_ALERT "Unable to allocate major number\n");
        return ret;
    }

    cdev_init(&my_cdev, &my_fops);
    cdev_add(&my_cdev, dev_num, 1);

    printk(KERN_INFO "my_shared_mem module loaded with device number %d\n", MAJOR(dev_num));

    shared_memory = vmalloc_user(shared_memory_size);
    printk("module_shared: shared memory allocated");
    // 使用新的函数写入初始数据
    
    const char *ss = "Hello from kernel!";
    write_to_shared_memory(ss, strlen(ss));
    return 0;
}

static void __exit my_module_exit(void) {
    vfree(shared_memory);
    cdev_del(&my_cdev);
    unregister_chrdev_region(MKDEV(major, 0), 1);
}

module_init(my_module_init);
module_exit(my_module_exit);

MODULE_LICENSE("GPL");
