# ELK

es容器启动需要宿主机的`vm.max_map_count`大于262144, 否则在启动过程中会报如下错误然后退出, 记得要提前设置

```
elasticsearch_1  | ERROR: [1] bootstrap checks failed
elasticsearch_1  | [1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
```

1. [ELK单节点最简示例](./01.elk-single/readme.md)
2. [ELK多节点, 多logstash](./02.elk-logstash-lb/readme.md)
3. [ELK+filebeat](./03.elk-filebeat/readme.md)
4. [ELK+filebeat+kafka](./04.elk-filebeat-kafka/readme.md)
5. [ELK+filebeat+kafka+阿里云logpilot](./05.elk-filebeat-kafka-logpilot/readme.md)

