参考文章

1. [干货 | Elasticsearch 7.1免费安全功能全景认知](https://blog.csdn.net/laoyang360/article/details/90554761)
    - es 安全机制的演变历程
2. [<十三>ELK-学习笔记–elasticsearch-7.x使用xpack进行安全认证](http://www.eryajf.net/3500.html)
    - 单机与集群环境开启安全认证的实际操作示例.

前面创建的 es 集群都没有密码(虽然 yaml 中已经配置过了, 但都不生效), 不管是`curl es:9200`, 还是打开 kibana 的 webUI, 都不需要, 生产环境是绝对禁止的. 

所以这里我们尝试加上密码认证. 单机环境与集群环境开启密码认证的操作不同, 所以同样要区别对待.

其实只要在`es`配置文件`elasticsearch.yml`文件中添加如下一行就可以了.

```yaml
## 这条配置表示开启xpack认证机制
xpack.security.enabled: true 
```

参考文章2中说还要再加上一条`xpack.security.transport.ssl.enabled: true`, 否则 es 无法启动, 但是我在测试的时候不需要添加这条.

之后再使用 curl 访问, 就要带上用户名与密码了.

```console
$ curl es:9200/_cat/health
{"error":{"root_cause":[{"type":"security_exception","reason":"missing authentication credentials for REST request [/_cat/health]","header":{"WWW-Authenticate":"Basic realm=\"security\" charset=\"UTF-8\""}}],"type":"security_exception","reason":"missing authentication credentials for REST request [/_cat/health]","header":{"WWW-Authenticate":"Basic realm=\"security\" charset=\"UTF-8\""}},"status":401}

$ curl -u elastic:123456 es:9200/_cat/health
1592817746 09:22:26 elasticsearch green 1 1 2 2 0 0 0 0 - 100.0%
```

同时, 再访问 kibana 也是需要密码的.

![](https://gitee.com/generals-space/gitimg/raw/master/8ecde1c741d34655c2d405bf5b82f4e7.png)

> 注意: 此时 kibana 与 logstash 配置文件中的密码就是必须的了, 否则启动会失败.
