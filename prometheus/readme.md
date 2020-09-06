# prometheus

## 1.

在创建deploy之前, 需要先创建secret资源, 不然deploy会一直pending.

在独立的etcd集群部署中, 下面这条命令可以直接执行.

```
kubectl -n monitoring create secret generic etcd-certs --from-file=/etc/etcd/ssl/ca.crt --from-file=/etc/etcd/ssl/server.crt --from-file=/etc/etcd/ssl/server.key
```

如果是内置在集群的etcd, 由于`/etc/kubernetes/pki/etcd`目录下存放着etcd需要的所有密钥文件, 可以执行如下命令.

```
kubectl -n monitoring create secret generic etcd-certs --from-file=/etc/kubernetes/pki/etcd
```

## 2. 

修改`/etc/kubernetes/manifests/`目录下`kube-controller-manager.yaml`与`kube-scheduler.yaml`, 将其中的`--address=127.0.0.1`修改为`--address=0.0.0.0`, 然后重启kubelet服务.

注意: 所有master节点止的`controller manager`和`scheduler`的配置都要修改.

然后还要为ta们创建service资源, 以便prometheus能够访问到.

## 3. 

部署完成, 通过`IP:port`的形式访问, 可以得到如下界面.

![](https://gitee.com/generals-space/gitimg/raw/master/11e1f2b165128cd49df84523020c0e0d.png)

![](https://gitee.com/generals-space/gitimg/raw/master/0c0c5dfe54d152de0250abe6c290228b.png)

`grafana`可以通过`admin/admin`的默认用户名密码进行登录, prometheus则不需要登录.
