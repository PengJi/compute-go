# 部署
操作系统：ubuntu 26.04
K8S版本：1.34.0

部署节点
192.168.227.130

集群节点
192.168.227.131 master
192.168.227.132 node1
192.168.227.133 node2
192.168.227.134 node3

## 1. 配置集群节点环境

### 1.1 配置主机

#### （1）修改主机名（所有节点）
```bash
hostnamectl set-hostname master
```

#### （2）配置固定IP/DNS/默认网关（所有节点）
```bash
cd /etc/netplan/
cp 00-installer-config.yaml 00-installer-config.yaml.bak
vim /etc/netplan/00-installer-config.yaml
# This is the network config written by 'subiquity'
network:
  ethernets:
    ens33:
      dhcp4: no
      dhcp6: no
      addresses:
        - 192.168.227.131/24
      routes:
        - to: default
          via: 192.168.227.2
      match:
        macaddress: 00:0c:29:76:7e:41
      set-name: ens33
      nameservers:
        addresses: [223.5.5.5]
  version: 2
```

#### （3）修改时区
```bash
sudo timedatectl set-timezone Asia/Shanghai
timedatectl

```

注意：vmware 复制的虚拟机 mac 地址会变，但配置文件中不变，需要修改。

### 1.2 关闭防火墙（所有节点）
```bash
sudo ufw disable
```

### 1.3 配置NTP（所有节点）
```bash
sudo systemctl status chronyd
```

### 1.4 修改内核参数（所有节点）
```bash
# 修改进程资源限制
sudo cat <<EOF | sudo tee -a /etc/security/limits.conf
* soft nofile 32768
* hard nofile 65535
* soft nproc 32768
* hard nproc 65535
EOF

# 设置K8S内核参数
sudo cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
# ---------- 核心网络----------
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1   # 如果使用 IPv6 则需要，否则可注释
net.ipv4.ip_forward = 1
net.ipv4.ip_nonlocal_bind = 1            # 允许服务绑定到尚不存在的 IP（用于 LoadBalancer IP 故障转移）

# ---------- 内存与 OOM 行为----------
vm.overcommit_memory = 1                 # kubelet 要求
vm.panic_on_oom = 0                      # OOM 时触发 killer 而不是 panic
vm.swappiness = 0                        # 尽量少用 swap（如果必须禁用 swap 则此参数无效）

# ---------- 文件系统与 inotify ----------
fs.may_detach_mounts = 1                 # 帮助清理网络命名空间
fs.inotify.max_user_watches = 89100      # 提高文件监控上限，避免 Pod 日志/指标监控失败

# ---------- 网络连接跟踪（高并发场景推荐） ----------
net.netfilter.nf_conntrack_max = 2310720
# 如果遇到 conntrack 表满，可同时调大下面两个参数：
net.nf_conntrack_max = 2310720
net.netfilter.nf_conntrack_tcp_timeout_established = 86400

# ---------- TCP 性能调优（可选，适用于大量 Service/Pod） ----------
net.core.somaxconn = 16384
net.ipv4.tcp_max_syn_backlog = 16384
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_keepalive_probes = 3
net.ipv4.tcp_keepalive_intvl = 15
EOF

# 重新加载 sysctl 参数
sudo sysctl --system
```

### 1.5 安装docker（所有节点）
https://docs.docker.com/engine/install/ubuntu/#install-from-a-package
```sh

# 下载包
containerd.io_<version>_<arch>.deb
docker-ce_<version>_<arch>.deb
docker-ce-cli_<version>_<arch>.deb
docker-buildx-plugin_<version>_<arch>.deb
docker-compose-plugin_<version>_<arch>.deb

# 安装
sudo dpkg -i ./containerd.io_<version>_<arch>.deb \
  ./docker-ce_<version>_<arch>.deb \
  ./docker-ce-cli_<version>_<arch>.deb \
  ./docker-buildx-plugin_<version>_<arch>.deb \
  ./docker-compose-plugin_<version>_<arch>.deb
```

示例：
```sh
# 安装
sudo dpkg -i ./containerd.io_2.2.3-1~ubuntu.26.04~resolute_amd64.deb \
  ./docker-ce_29.4.3-1~ubuntu.26.04~resolute_amd64.deb \
  ./docker-ce-cli_29.4.3-1~ubuntu.26.04~resolute_amd64.deb  \
  ./docker-buildx-plugin_0.33.0-1~ubuntu.26.04~resolute_amd64.deb \
  ./docker-compose-plugin_5.1.3-1~ubuntu.26.04~resolute_amd64.deb

# 修改镜像代理
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://docker.unsee.tech",
    "https://dockerpull.org",
    "https://dockerhub.icu"
  ]
}
EOF

# 重启
sudo systemctl daemon-reload & sudo systemctl restart docker

# 测试
sudo docker run hello-world
```

### 1.6 设置互信访问（root用户，所有节点）
```bash
# 生成密钥对 
ssh-keygen

# 复制公钥到目标服务器  
ssh-copy-id root@<target_ip>
```

### 1.7 配置 root 可远程登录
```bash
sudo vim /etc/ssh/sshd_config
PermitRootLogin yes

sudo systemctl restart sshd
```

### 1.8 修改 containerd 镜像地址（前提：containerd已安装），使用镜像：https://xuanyuan.cloud/dashboard
```bash
sudo mkdir -p /etc/containerd/certs.d/docker.io
sudo tee /etc/containerd/certs.d/docker.io/hosts.toml <<EOF
server = "https://registry-1.docker.io"

[host."https://dh3ojyl9fgwo7tppxp.xuanyuan.run"]
  capabilities = ["pull", "resolve"]

[host."https://docker.m.daocloud.io"]
  capabilities = ["pull", "resolve"]
EOF

sudo mkdir -p /etc/containerd/certs.d/registry.k8s.io
sudo tee /etc/containerd/certs.d/registry.k8s.io/hosts.toml <<EOF
server = "https://registry.k8s.io"

[host."https://dh3ojyl9fgwo7tppxp-k8s.xuanyuan.run"]
  capabilities = ["pull", "resolve"]

[host."https://k8s.m.daocloud.io"]
  capabilities = ["pull", "resolve"]
EOF

sudo mkdir -p /etc/containerd/certs.d/quay.io
sudo tee /etc/containerd/certs.d/quay.io/hosts.toml <<EOF
server = "https://quay.io"

[host."https://dh3ojyl9fgwo7tppxp-quay.xuanyuan.run"]
  capabilities = ["pull", "resolve"]

[host."https://quay.m.daocloud.io"]
  capabilities = ["pull", "resolve"]
EOF

# gcr.io
sudo mkdir -p /etc/containerd/certs.d/gcr.io
sudo tee /etc/containerd/certs.d/gcr.io/hosts.toml <<EOF
server = "https://gcr.io"
[host."https://dh3ojyl9fgwo7tppxp-gcr.xuanyuan.run"]
  capabilities = ["pull", "resolve"]
[host."https://gcr.m.daocloud.io"]
  capabilities = ["pull", "resolve"]
EOF

# ghcr.io
sudo mkdir -p /etc/containerd/certs.d/ghcr.io
sudo tee /etc/containerd/certs.d/ghcr.io/hosts.toml <<EOF
server = "https://ghcr.io"
[host."https://dh3ojyl9fgwo7tppxp-ghcr.xuanyuan.run"]
  capabilities = ["pull", "resolve"]
[host."https://ghcr.m.daocloud.io"]
  capabilities = ["pull", "resolve"]
EOF

# 重启 containerd
sudo systemctl restart containerd

# 确认配置已生效
sudo containerd config dump | grep -A 10 "certs.d"

# 测试拉取（建议先拉小镜像）
sudo crictl pull docker.io/library/nginx:alpine
```

## 2 部署节点

### 2.1 下载kubespray（root用户）
```bash
git clone https://github.com/kubernetes-sigs/kubespray.git
# 或
wget https://github.com/kubernetes-sigs/kubespray/archive/refs/tags/v2.26.1.tar.gz
tar -zxvf v2.26.1.tar.gz
mv kubespray-v2.26.1 kubespray
```

### 2.2 修改 kubespray 配置（root用户）
```bash
cp -r inventory/sample inventory/mycluster

# 修改集群配置
vim inventory/mycluster/inventory.ini
# This inventory describe a HA typology with stacked etcd (== same nodes as control plane)
# and 3 worker nodes
# See https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html
# for tips on building your # inventory

# Configure 'ip' variable to bind kubernetes services on a different ip than the default iface
# We should set etcd_member_name for etcd cluster. The node that are not etcd members do not need to set the value,
# or can set the empty string value.
[all]
master ansible_host=192.168.227.131  # ip=10.3.0.1 etcd_member_name=etcd1
node1 ansible_host=192.168.227.132   # ip=10.3.0.2 etcd_member_name=etcd2
node2 ansible_host=192.168.227.133  # ip=10.3.0.3 etcd_member_name=etcd3
node3 ansible_host=192.168.227.134  # ip=10.3.0.4 etcd_member_name=etcd4

[kube_control_plane]
master

[kube_node]
node1
node2
node3

[etcd:children]
kube_control_plane

[k8s_cluster:children]
kube_control_plane
kube_node


# 修改镜像地址，镜像仓库：https://xuanyuan.cloud/dashboard
vim inventory/mycluster/group_vars/all/offline.yml
---
## Global Offline settings
### Private Container Image Registry
# registry_host: "myprivateregisry.com"
files_repo: "https://files.m.daocloud.io"
### If using CentOS, RedHat, AlmaLinux or Fedora
# yum_repo: "http://myinternalyumrepo"
### If using Debian
# debian_repo: "http://myinternaldebianrepo"
### If using Ubuntu
# ubuntu_repo: "http://myinternalubunturepo"

## Container Registry overrides
kube_image_repo: "dh3ojyl9fgwo7tppxp-k8s.xuanyuan.run" 
gcr_image_repo: "dh3ojyl9fgwo7tppxp-gcr.xuanyuan.run"
github_image_repo: "dh3ojyl9fgwo7tppxp-ghcr.xuanyuan.run"
docker_image_repo: "dh3ojyl9fgwo7tppxp.xuanyuan.run"
quay_image_repo: "dh3ojyl9fgwo7tppxp-quay.xuanyuan.run"
```

### 2.3 部署k8s（root用户）
```bash
# 切换为root用户
su root

# 开启虚拟环境
python3 -m venv /home/jipeng/venv

source /home/jipeng/venv/bin/activate


cd /home/jipeng/kubespray
# 安装相关包
pip install -r requirements.txt
# 部署
ansible-playbook \
-i inventory/mycluster/inventory.ini \
--user=root \
-e kube_version=1.34.0 \
-v cluster.yml
```

### 2.4 重新部署k8s（root用户）
```bash
# 重置k8s集群
ansible-playbook \
-i inventory/mycluster/inventory.ini reset.yml \
-b -vvv

# 重新部署
ansible-playbook \
-i inventory/mycluster/inventory.ini \
--user=root \
-e kube_version=1.34.0 \
-v cluster.yml
```

## ref
[Kubespray实现生产环境一键部署k8s v1.25.6集群](https://www.magiccloudnet.com/kubespray/#%E4%B8%BB%E6%9C%BA%E5%87%86%E5%A4%87)  
[下载 Kubernetes](https://v1-34.kubernetes.ac.cn/releases/download/)


# node扩容（root用户）

## 1. 扩容节点
```bash
# 开启虚拟环境
source /home/jipeng/venv/bin/activate

# 添加节点配置
vim inventory/mycluster/inventory.ini
[all]
node3 ansible_host=192.168.227.139  # ip=10.3.0.4 etcd_member_name=etcd4

[kube_node]
node3

# 收集并缓存所有节点的 Facts，并为接下来的扩容操作做准备
ansible-playbook \
-i inventory/mycluster/inventory.ini \
--user=root \
playbooks/facts.yml
-vvv

# 扩容节点
ansible-playbook \
-i inventory/mycluster/inventory.ini \
--user=root \
scale.yml \
--limit=node3 \
-vvv
```

## 2. 验证扩容结果
```bash
kubectl get pods --all-namespaces -o wide --field-selector spec.nodeName=node3
NAMESPACE     NAME                 READY   STATUS    RESTARTS   AGE     IP                NODE    NOMINATED NODE   READINESS GATES
kube-system   calico-node-mc6cn    1/1     Running   0          5m52s   192.168.227.139   node3   <none>           <none>
kube-system   kube-proxy-hkn9j     1/1     Running   0          5m52s   192.168.227.139   node3   <none>           <none>
kube-system   nginx-proxy-node3    1/1     Running   0          5m51s   192.168.227.139   node3   <none>           <none>
kube-system   nodelocaldns-gxt6t   1/1     Running   0          5m52s   192.168.227.139   node3   <none>           <none>
```

[使用 Kubespray 将新节点添加到 Kubernetes 集群](https://cn.console-linux.com/?p=20448)  
