#!/usr/bin/env python3

import time
from tasks.task import write_into_redis

## 常规操作, 把任务下发出去, 由于write_into_redis()是被app.task装饰过的方法(即task对象), 
## 使用`delay`调用时, 会自动下发到实例化app时传入的broker实例中...
while True:
    time.sleep(5)
    write_into_redis.delay('https://www.baidu.com')
