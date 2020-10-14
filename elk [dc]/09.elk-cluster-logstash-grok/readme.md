# ELK

参考文章

1. [logstash grok插件语法介绍](https://blog.csdn.net/qq_34021712/article/details/79746413)
2. [logstash之grok过滤](https://blog.csdn.net/yanggd1987/article/details/50486779)
    - 我们的生产环境中，日志格式往往使用的是普通的格式，因此就不得不使用logstash的filter/grok进行过滤
    - nginx 配置中的 log_format 内置变量与 grok 模式的对应关系, 值得收藏.
3. [logstash-plugins/logstash-patterns-core](https://github.com/logstash-plugins/logstash-patterns-core/tree/master/patterns)
    - logstash 附加的 grok 模式(不过没有 nginx 的)

本示例基于示例[02.elk-logstash-lb](), 在使用两个 logstash 实例分别采集两个 nginx 实例的日志, 并直接传入 es 之外, 修改了 pipeline 配置中的`filter`字段, 使用`grok`过滤.

> 通过 kibana 创建 index pattern 的操作不变.

话说, 我之前有想过对 nginx 的日志进行采集, 当时考虑的, 要么是修改 nginx 的配置文件, 将其日志格式按照一定规则配置, 要么是在日志处理端进行正则匹配, 通过正则分组得到各字段的值. 不过当时没有实现, 现在通过 elk 都遇到了...

------

示例[02.elk-logstash-lb]()中 nginx 的日志格式配置成了 json, 在 pipeline 的`input`块中, 就可以使用`codec => json`进行解析, 得到各成员字段的值了.

现在将 nginx 配置中的 json 日志格式移除, 重启 nginx, 同时移除 logstash 配置中`codec => json`, 否则 logstash 在处理常规类型的 nginx 日志时会报如下错误.

```
[2020-10-13T10:49:50,060][ERROR][logstash.codecs.json     ] JSON parse error, original data now in message field {:error=>#<LogStash::Json::ParserError: Unexpected character ('.' (code 46)): Expected space separating root-level values
 at [Source: (String)"172.19.0.1 - - [13/Oct/2020:10:49:49 +0000] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44""; line: 1, column: 8]>, :data=>"172.19.0.1 - - [13/Oct/2020:10:49:49 +0000] \"GET / HTTP/1.1\" 200 612 \"-\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44\""}
```

------

然后修改`filter`字段, 原来的`filter`字段如下

```conf
filter {
    mutate {
        ## 使用过滤器添加节点名称, 以便分类
        add_field => {"_nodename" => "node-01"}
    }
}
```

于是来自 node-01 主机的 nginx 日志就会自动添加上一个`_nodename`字段, 如下

![](https://gitee.com/generals-space/gitimg/raw/master/bd8bdbf77c659a05fe5a34ffea1fb8bf.png)

现在我们将其换成`grok`.

由于 nginx 的原生日志格式如下

```
172.19.0.1 - - [13/Oct/2020:10:55:05 +0000] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44"
```

我们在`logstash`配置中添加如下过滤器配置

```conf
filter {
    grok {
        match => { 
            "message" => "%{IP:client} - - \[%{HTTPDATE:timestamp}\] \"%{WORD:method} %{URIPATHPARAM:uri} HTTP/%{NUMBER:httpversion}\" %{NUMBER:status} %{NUMBER:bytes} \"-\" \"%{GREEDYDATA:agent}\"" 
        }
    }
}
```

重启 logstash 容器, 再次访问 nginx, kibana得到的日志如下

![](https://gitee.com/generals-space/gitimg/raw/master/53e9deb686f358a35a6bae98bbe989dc.png)

可以看到, 结果中出现了`message`字段, 其值为该行日志的所有内容, 其余字段的值分别赋值给了`client`, `timestamp`等字段.

