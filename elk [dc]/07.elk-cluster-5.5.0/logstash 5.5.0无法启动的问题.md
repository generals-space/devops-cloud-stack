# logstash 5.5.0无法启动的问题

参考文章

1. [logstash启动报配置文件错误Expected one of #, input, filter, output at line 1, column 1 (byte 1) after](https://blog.csdn.net/Crazy_T_B/article/details/79422602)
2. [Expected one of #, input, filter, output at line 2, column 1 (byte 2): Logstash](https://blog.csdn.net/wyqlxy/article/details/52583639)

我按照之前 7.2.0 版本的方式部署 5.5.0 的 ELK, 但是`logstash`总也无法启动, 日志信息中也没有什么重要的信息.

后来把`logstash`的配置改成如下, 进到容器里面看了看.

```yaml
  logstash:
    image: logstash:5.5.0
    environment:
      LS_JAVA_OPTS: "-Xmx256m -Xms256m"
    volumes:
      - ./logstash/config/logstash.conf:/usr/share/logstash/config/logstash.conf:ro
      - ./logstash/pipeline:/usr/share/logstash/pipeline:ro
    command: ["tail", "-f", "/docker-entrypoint.sh"]
```

使用如下命令启动服务.

```
logstash --log.level=debug --path.config=/usr/share/logstash/config/logstash.yml
```

打印了如下错误日志就直接退出了.

```
06:19:29.041 [LogStash::Runner] ERROR logstash.agent - Cannot create pipeline {:reason=>"Expected one of #, input, filter, output at line 1, column 1 (byte 1) after ", :backtrace=>["/usr/share/logstash/logstash-core/lib/logstash/pipeline.rb:59:in `initialize'", "/usr/share/logstash/logstash-core/lib/logstash/pipeline.rb:156:in `initialize'", "/usr/share/logstash/logstash-core/lib/logstash/agent.rb:286:in `create_pipeline'", "/usr/share/logstash/logstash-core/lib/logstash/agent.rb:95:in `register_pipeline'", "/usr/share/logstash/logstash-core/lib/logstash/runner.rb:314:in `execute'", "/usr/share/logstash/vendor/bundle/jruby/1.9/gems/clamp-0.6.5/lib/clamp/command.rb:67:in `run'", "/usr/share/logstash/logstash-core/lib/logstash/runner.rb:209:in `run'", "/usr/share/logstash/vendor/bundle/jruby/1.9/gems/clamp-0.6.5/lib/clamp/command.rb:132:in `run'", "/usr/share/logstash/lib/bootstrap/environment.rb:71:in `(root)'"]}
```

最开始我以为是我的 pipeline 格式写的不正确, 参考文章1中也说可能是字符集的原因, 但我核对了下明明没错啊.

后来又找到了参考文章2, 发现他们把 pipeline 的内容写到了 conf 文件里, 于是尝试把`pipeline`的内容放到`conf`文件, 把原来的`yml`配置文件移除, 然后启动成功了.

`logstash` 5.5.0 版本中, 可配置的字段是在命令行传入的, 不需要单独的配置文件.
