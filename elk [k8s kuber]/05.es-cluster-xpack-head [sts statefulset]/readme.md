参考文章

1. [6，ELK进阶--elasticsearch-head-master](https://www.jianshu.com/p/83d12b0ca4c0)
2. [elasticsearch-head-master插件的安装与使用](https://blog.csdn.net/tripleDemo/article/details/100998309)
3. [Elasticsearch-head 插件安装](https://www.jianshu.com/p/c2b5d4590c3e)
    - `http://172.20.1.187:9100/?auth_user=elastic&auth_password=123456`
4. [when elasticsearch x-pack is enabled head can't connnect](https://github.com/mobz/elasticsearch-head/issues/304)
    - `boroborome`的回答真是救了命了...

相比于前面的示例, 本示例中增加了 [mobz/elasticsearch-head](https://github.com/mobz/elasticsearch-head) 工程, 当然也有ta的 Service(`NodePort`类型).

并且, 由于我们需要在 head 工程的 webUI 中输入 es 集群的地址进行监控管理, 所以我们还要加一个 es-cluster 对外的 NodePort 服务, 名为`es-cluster-public`(因为`headless service`不能同时为`NodePort`类型, 只能另外再建一个).

需要注意的是, 当 es 开启了 xpack 安全认证时, head 连接 es 的方法, 挺别致的...

![](https://gitee.com/generals-space/gitimg/raw/master/1069CFB42D5656B1D8190F49B39EC721.png)

在地址输入 head 的地址 xxx:9100 时, 要带上目标 es 集群的用户名和密码作为参数, 然后在打开界面的输入框中在填写 es 集群的地址时, 就不用写用户名和密码了...

地址栏中的认证参数分别为`auth_user`和`auth_password`.

其实 head 只是一个过滤产品, 貌似 6.x 之后的 kibana 就可以实现更高级更美观的监控管理功能, head 也就随之没落了.
