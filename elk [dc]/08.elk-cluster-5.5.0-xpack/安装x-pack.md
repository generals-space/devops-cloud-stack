参考文章

1. [官方文档 Installing X-Pack in Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/5.5/installing-xpack-es.html)
    - [x-pack下载链接](https://artifacts.elastic.co/downloads/packs/x-pack/x-pack-5.5.0.zip)
    - x-pack 与 es 的版本对照关系, 两者需要相互匹配才可使用, 相关在小版本也不行(比如 es 5.5.0 与 x-pack 5.5.3 就不能匹配).
2. [官方文档 Security Settings in Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/5.5/security-settings.html)
    - kibana x-pack 配置文档链接

目前所有的部署, 访问时都是无需认证的, 可以直接访问 es 的 restful api, 也可以直接登录 kibana 的 web 界面, logstash 也能无阻碍地将日志发往es集群.

为了安全, 我们需要为其添加上密码认证机制.

在 5.5.0 版本中, x-pack 作为插件安装在 es 中

## 1. 安装

es 初始部署时, bin目录的内容如下

```
root@deef9e5fcece:/usr/share/elasticsearch/bin# ls -al
total 36
drwxr-xr-x 2 root root 4096 Jul 24  2017 .
drwxr-xr-x 1 root root 4096 Jul 24  2017 ..
-rwxr-xr-x 1 root root 8075 Jun 30  2017 elasticsearch
-rwxr-xr-x 1 root root 2605 Jun 30  2017 elasticsearch-keystore
-rwxr-xr-x 1 root root 2595 Jun 30  2017 elasticsearch-plugin
-rwxr-xr-x 1 root root  223 Jun 30  2017 elasticsearch-systemd-pre-exec
-rwxr-xr-x 1 root root 2569 Jun 30  2017 elasticsearch-translog
-rwxr-xr-x 1 root root  367 Jun 30  2017 elasticsearch.in.sh
```

`elasticsearch-plugin list`的结果为空.

`x-pack`可以在线安装, 如下

```
bin/elasticsearch-plugin install x-pack
```

如果容器内不可联网, 或是希望将插件封装到镜像中, 可以将`x-pack`下载到本地(容器内部, 不要放在`plugins`目录下), 然后本地安装

```console
$ bin/elasticsearch-plugin install file:///usr/share/elasticsearch/x-pack-5.5.0.zip
root@deef9e5fcece:~# elasticsearch-plugin install file:///root/x-pack-5.5.0.zip
-> Downloading file:///root/x-pack-5.5.0.zip
[=================================================] 100%
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@     WARNING: plugin requires additional permissions     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
* java.io.FilePermission \\.\pipe\* read,write
* java.lang.RuntimePermission accessClassInPackage.com.sun.activation.registries
* java.lang.RuntimePermission getClassLoader
* java.lang.RuntimePermission setContextClassLoader
* java.lang.RuntimePermission setFactory
* java.security.SecurityPermission createPolicy.JavaPolicy
* java.security.SecurityPermission getPolicy
* java.security.SecurityPermission putProviderProperty.BC
* java.security.SecurityPermission setPolicy
* java.util.PropertyPermission * read,write
* java.util.PropertyPermission sun.nio.ch.bugLevel write
* javax.net.ssl.SSLPermission setHostnameVerifier
See http://docs.oracle.com/javase/8/docs/technotes/guides/security/permissions.html
for descriptions of what these permissions allow and the associated risks.

Continue with installation? [y/N]y  ## 这里输入y
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@        WARNING: plugin forks a native controller        @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
This plugin launches a native controller that is not subject to the Java
security manager nor to system call filters.

Continue with installation? [y/N]y  ## 这里输入y
-> Installed x-pack
```

安装完成后, 查看插件列表, 结果如下

```
$ elasticsearch-plugin list
x-pack
```

------

`x-pack`需要在所有`es`节点, `kibana`节点, 以及`logstash`, 全都需要安装`x-pack`. 安装包用同一个, 安装方法也都差不多. `kibana`的安装工具用`bin/kibana-plugin`(这个安装花了好久), `logstash`用`bin/logstash-plugin`.

## 2. 配置

`es`, `kibana`, `logstash`的`x-pack`都安装完成后, 需要在配置文件中添加`x-pack`相关内容, 然后重启各个容器.

### es

```yaml
xpack.security.enabled: true
```

`es`开启`x-pack`后, 默认的超级用户名密码为`elastic:changeme`.

### kibana

```yaml
xpack.security.enabled: true
elasticsearch.username: elastic
elasticsearch.password: changeme
```

官方文档就没说要加`username`和`password`这两个键...

### logstash

```conf
output {
    if [type] == "nginx-log"{
        elasticsearch {
            hosts => "esc-master-0:9200"
            user => "elastic"
            password => "changeme"
            index => "nginx-log-%{+YYYY.MM.dd}"
        }
    }
}

```

前面的示例中, `password`一直是`123456`, 不过因为没开启`x-pack`, 所以没啥问题. 现在这里要将`password`改成`changeme`, 与目标`es`集群保持一致.

### filebeat

本示例中没有使用`filebeat`组件(没找到 5.5.0 版本的镜像), 这里只是记录一下. 之前`filebeat`配置中的`output`都是`logstash`, 如果要向开启了`x-pack`的es集群直接传输日志, 需要写成如下格式.

```yml
output:
  logstash:
    enabled: true
    hosts: ["esc-master-0:9200"]
    username: elastic
    password: changeme

```

## 3. 使用

现在访问es, 就需要指定密码了, 否则将返回

```console
$ curl localhost:9200/_cat/health
{"error":{"root_cause":[{"type":"security_exception","reason":"missing authentication token for REST request [/_cat/health]","header":{"WWW-Authenticate":"Basic realm=\"security\" charset=\"UTF-8\""}}],"type":"security_exception","reason":"missing authentication token for REST request [/_cat/health]","header":{"WWW-Authenticate":"Basic realm=\"security\" charset=\"UTF-8\""}},"status":401}
```

默认的超级用户名密码为`elastic:changeme`.

```
$ curl -u elastic:changeme localhost:9200/_cat/health
1600305765 01:22:45 esc green 3 3 20 10 0 0 0 0 - 100.0%
```

访问`kibana`, 将显示登录界面.

![](https://gitee.com/generals-space/gitimg/raw/master/030973e9f72724c4aea62a9967ddcbc0.png)

输入`elastic:changeme`, 进入主界面.

![](https://gitee.com/generals-space/gitimg/raw/master/92a3197b1892588e3c2abd1fbb836bd9.png)

相较于未开启`x-pack`时, 左侧菜单多了`Machine Learning`, `Gragh`和`Monitoring`几个选项.

## 4. 后记

除了使用`elasticsearch-plugins install`安装插件, 其实也可以从安装好插件的`plugins`目录下将`x-pack`目录拷贝出来, 这个目录下全是jar包.

在启动时将这个目录直接映射到`plugins`目录中即可直接使用`x-pack`插件.

```yaml
    volumes:
      - ./elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml:ro
      - ./data/x-pack:/usr/share/elasticsearch/plugins/x-pack
```

不过`x-pack`除了在`plugins`生成子目录外, 还在`bin`目录下生成了一个`x-pack`子目录, 其下都是可执行文件, 如果不映射这些文件, 那么这些命令就没法直接用了.
