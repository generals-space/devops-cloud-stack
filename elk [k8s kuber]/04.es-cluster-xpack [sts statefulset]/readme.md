参考文章

1. [干货 | Elasticsearch 7.1免费安全功能全景认知](https://blog.csdn.net/laoyang360/article/details/90554761)
    - es 安全机制的演变历程
2. [<十三>ELK-学习笔记–elasticsearch-7.x使用xpack进行安全认证](http://www.eryajf.net/3500.html)
    - 单机与集群环境开启安全认证的实际操作示例.

集群间节点的认证是通过密钥实现的, 密钥配置与用户名密码的配置并不冲突.

如下两条命令均一路回车即可, 不需要给秘钥再添加密码

```
/usr/share/elasticsearch/bin/elasticsearch-certutil ca
/usr/share/elasticsearch/bin/elasticsearch-certutil cert --ca elastic-stack-ca.p12
```

默认会在`/usr/share/elasticsearch/`目录下, 分别生成`elastic-stack-ca.p12`和`elastic-certificates.p12`文件. 可以使用`-out`选项指定生成的文件路径, 如下

```
/usr/share/elasticsearch/bin/elasticsearch-certutil ca -out /tmp/xxx-ca.p12
```

其实之后在配置文件中只会用到`elastic-certificates.p12`, 不需要`elastic-stack-ca.p12`, 所以上述命令可以只执行第2步, 不需要生成ca文件.

```yaml
## 这条配置表示开启xpack认证机制
xpack.security.enabled: true 
xpack.security.transport.ssl.enabled: true
xpack.security.transport.ssl.verification_mode: certificate
xpack.security.transport.ssl.keystore.path: /usr/share/elasticsearch/config/elastic-certificates.p12
xpack.security.transport.ssl.truststore.path: /usr/share/elasticsearch/config/elastic-certificates.p12
```

上述配置可以与用户名密码一同设置, 这样对 setup 的集群也可以生效.
