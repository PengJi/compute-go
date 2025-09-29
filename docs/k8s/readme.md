
常用命令
```bash
# 进入容器
kubectl exec -it prometheus-k8s-0 -c prometheus -n monitoring -- /bin/sh

# 端口转发
kubectl port-forward -n esx-develop deployment/authx-srv 8081:8081
```
