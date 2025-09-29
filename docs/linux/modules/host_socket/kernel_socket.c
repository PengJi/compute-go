#include <linux/module.h>
#include <net/sock.h>
#include <linux/un.h>
#include <linux/net.h>

#define SOCKET_PATH "/tmp/kernel_socket"

static struct socket *sock;
static struct sockaddr_un addr;

int send_data_from_guest(const char *data) {
    struct kvec vec;
    struct msghdr msg;
    int len;

    printk(KERN_INFO "reveive msg begin\n");

    if (!sock) {
        printk(KERN_ERR "Socket is not created\n");
        return -ENOTCONN;
    }

    vec.iov_len = strlen(data);
    vec.iov_base = (char *)data;

    memset(&msg, 0, sizeof(msg));
    msg.msg_name = &addr;
    msg.msg_namelen = sizeof(struct sockaddr_un);

    len = kernel_sendmsg(sock, &msg, &vec, 1, strlen(data));

    printk("reveive msg: %s\n, msg len: %d", data, len);

    return len;
}
EXPORT_SYMBOL_GPL(send_data_from_guest);

static int __init kernel_socket_init(void) {
    int err;

    err = sock_create_kern(&init_net, AF_UNIX, SOCK_DGRAM, 0, &sock);
    if (err < 0) {
        printk(KERN_ERR "Error during socket creation\n");
        return err;
    }

    memset(&addr, 0, sizeof(struct sockaddr_un));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, SOCKET_PATH, sizeof(addr.sun_path) - 1);

    return 0;
}

static void __exit kernel_socket_exit(void) {
    if (sock) {
        sock_release(sock);
    }
}

module_init(kernel_socket_init);
module_exit(kernel_socket_exit);

MODULE_LICENSE("GPL");
