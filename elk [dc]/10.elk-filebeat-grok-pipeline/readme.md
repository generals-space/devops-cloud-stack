# ELK

参考文章

1. [ELK + Filebeat 搭建日志系统](http://beckjin.com/2017/12/10/elk/)
2. [Plugins Inputs Beats](https://www.elastic.co/guide/en/logstash/current/plugins-inputs-beats.html)

filebeat 只有采集的功能, 而 logstash 除了采集, 还有对数据进行预处理的能力. 比如为不同主机上的日志添加主机名及IP字段, 添加采集时间等, 之后存入es后也方便查询.

在 es 5.x 时, 内置了 logstash 的预处理功能, 可以用 filebeat 这种轻量采集工具代替 logstash 了.

在使用`docker-compose up -d`启动集群后, 需要登录 kibana, 在`Dev Tools`界面发起如下请求创建`pipeline`.

```json
PUT _ingest/pipeline/nginx-log
{
    "description" : "用 grok 插件处理 nignx 日志",
    "processors": [
        {
            "grok": {
                "field": "message",
                "patterns": ["%{IP:client} - - \[%{HTTPDATE:timestamp}\] \"%{WORD:method} %{URIPATHPARAM:uri} HTTP/%{NUMBER:httpversion}\" %{NUMBER:status} %{NUMBER:bytes} \"-\" \"%{GREEDYDATA:agent}\""]
            }
        }
    ]
}
```

上面`pipeline`的内容与示例09中, logstash 配置的`filter.grok`部分的内容一致.
