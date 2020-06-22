#!/usr/bin/env python3

from rq import Queue
from redis import Redis
import time
from jobs.producer import write_into_redis, count_words_at_url

redis_conn = Redis(host='redis-serv', port=6379)

q = Queue(connection=redis_conn)

while True:
    time.sleep(5)
    ## job = q.enqueue(count_words_at_url, 'https://www.baidu.com')
    job = q.enqueue(write_into_redis, 'https://www.baidu.com')

## 删除此任务队列对象, 同时会删除该队列中所有任务.
## 之后就不能再使用, 除非重新实例化
## q.delete(delete_jobs=True)
