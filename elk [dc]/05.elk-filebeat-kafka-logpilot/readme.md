# ELK

参考文章

1. [BEATS 轻量型数据采集器](https://www.elastic.co/cn/products/beats)
    - beats组件的各类
2. [log-pilot](https://github.com/AliyunContainerService/log-pilot)

官网中列举出了7种beat组件, 用来收集各种不同的日志. 但是在容器化部署时, 由于容器要求进程在前端运行, 所以日志一般会输出到stdout. 

但是这7种beat组件没有一种能收集stdout的日志, 所以有一段时间我们是把dockerfile中的CMD指令写作`tail -f /etc/profile`, 而项目进程以守护进程的形式运行的.

但这又带来一个问题, linux本身拥有OOM机制, 强制杀死占用资源最多的进程. docker中的进程在前端运行时, pid为1, 被kill后相当于容器被stop, 此时重启机制可以生效, 不会出现服务挂掉的情况. 而如果使用`tail -f`的CMD, 项目进程被kill掉不影响docker本身的运行, 于是可能出现容器还在, 但是项目进程不在了的情况.

阿里云的log-pilot工具可以应对这种情况, 本实验主要的目的就是验证ta的功能.

log-pilot最大的功能就是可以收集stdout的日志...??? 

一定要注意`aliyun.logs.XXX`的标签配置中, `XXX`既是发往kafka的topic名称, 需要在logstash的input字段指定相同名称, 也是发往es的index名称, 如果直接发往es, 记得也要与此匹配.

nginx-01和nginx-02验证log-pilot对日志文件的收集功能, 而nginx-03则是验证其对stdout日志的收集功能(nginx-03没有挂载共享目录). 

由于docker的stdout日志实际上也是写在宿主的`/var/lib/docker/containers/xxx`目录的文件中, 而且log-pilot拥有docker.sock的权限, 所以我猜想log-pilot实际上只是确定了stdout日志的存放路径, 而处理过程与普通日志文件的处理方法没有区别.
