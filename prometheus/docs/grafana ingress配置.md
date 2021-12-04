参考文章

1. [nginx代理grafana](https://www.cnblogs.com/wurijie/p/11109673.html)
2. [Prometheus + Grafana（三）nginx 设置反向代理](https://www.cnblogs.com/caoweixiong/p/12155712.html)

本来想通过ingress, 将prometheus与grafana配置成相同域名及端口, 仅通过uri路径做相应转发的, 但最终发现不行...

nginx的规则并不是万能的, 很多vue/react这种项目的静态资源路径是固定的(可通过配置进行变更)

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: monitoring
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  rules:
  - host: dev.kube.com
    http:
      paths:
      - path: /grafana(/|$)(.*)
        backend:
          serviceName: grafana
          servicePort: 3000

```

当我们访问`http://IP:port/grafana`时, 通过`rewrite-target`(其实就是nginx中的`proxy_path`), 将首页请求转发到后端grafana服务, 但是紧接着的静态资源仍然会以`/`作为根路径.

浏览器会以`http://IP:port/public/xxx`这种形式请求静态资源.

```html
    <link rel="icon" type="image/png" href="public/img/fav32.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="public/img/apple-touch-icon.png" />
    <link rel="mask-icon" href="public/img/grafana_mask_icon.svg" color="#F05A28" />

    <link rel="stylesheet" href="public/build/grafana.dark.4141596c10e564d57dfb.css" />

    <script src="public/build/runtime.4141596c10e564d57dfb.js" type="text/javascript"></script>
    <script src="public/build/angular~app.4141596c10e564d57dfb.js" type="text/javascript"></script>
    <script src="public/build/app.4141596c10e564d57dfb.js" type="text/javascript"></script>
    <script src="public/build/moment~app.4141596c10e564d57dfb.js" type="text/javascript"></script>
    <script src="public/build/vendors~app.4141596c10e564d57dfb.js" type="text/javascript"></script>
```

我们没有办法在发起首页请求时, 将`public/xxx`也变更为`/grafana/public/xxx`. 

![](https://gitee.com/generals-space/gitimg/raw/master/9b4bc8ff4c937f233638d5434193d2fb.png)

如果再额外加一句`/public`的路径规则, 虽然可以实现目前的要求, 但当其他工程也在`dev.kube.com`域名下拥有`/public`路径的静态资源时, 会被误定位到grafana服务.

所以要么直接通过NortPort, 要么就用域名进行区分吧.

------

参考文章1, 2有写到手动修改 grafana/prometheus 的代理前缀, 即通过配置将`public/xxx`变更为指定的前缀, 如`grafana/public/xxx`, 这样就可以匹配到了.

其实之前在做运维时, 一般是一个服务开一个端口, 或是一个域名, 在同一个端口下用路径区分多个服务的(就算有通过路径转发的, 也是转发到多个api类型的后端接口, 静态资源这种, 没搞过).
