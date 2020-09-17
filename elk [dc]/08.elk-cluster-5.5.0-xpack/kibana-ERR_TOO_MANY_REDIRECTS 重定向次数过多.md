# kibana-ERR_TOO_MANY_REDIRECTS 重定向次数过多

参考文章

最开始按照官方文档安装了`x-pack`插件, 重启集群后访问`kibana`, 浏览器显示了如下错误.

![](https://gitee.com/generals-space/gitimg/raw/master/01f7a84f1c25295a73c77b8b3fec5851.png)

网上找了一些方法, 都没用, 后来发现是我配置文件里写了两个`username`字段, 没写`password`字段...

总之`kibana`出现这个问题一般是因为`es`的用户名密码不正确.
