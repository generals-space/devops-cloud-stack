这个工程搭建了python-rq集群, 需要先创建producer和worker镜像, 集群启动后可以访问`localhost:8080`来查看`rq-dashboard`的webui.

与我之前想的不同, 调度系统其实只需要编写**任务**对象, 由**生产者**放入队列, 就可以不用管了. 所谓的worker只是`rq worker`启动的运行进程, 不需要编写代码. 所要运行的任务由worker从队列中取出后直接执行. 可以启动任意多对象.

需要注意的是, 对于worker节点, 所要执行的**任务方法**必须是**可导入**的. 不管是放在`sys.path`还是要进入到工程目录里的相对路径. 我觉得应该是相对于入队列时导入的时候的路径.

实际上, 在celery官方文档里都说了

> The celery program can be used to start the worker (**you need to run the worker in the directory above project**)

实验了下, 在生产者中定义的任务使用redis连接操作, 在worker中执行时也是可以的.

重点在于任务的返回值, 和各种异常状况的处理. 关于异常状态在redis中的存储方式和过期时间还有重试机制, 由于文档太少(官方文档写的很没条理), 先不看了. 对比完celery再来看这个问题.