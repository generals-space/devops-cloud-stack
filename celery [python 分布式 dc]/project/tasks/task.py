#!/usr/bin/env python3

from celery import Celery
from redis import Redis
import requests

app = Celery('celery-app', broker='redis://:celery_redis_pwd@redis-serv:6379/0')
redis_conn = Redis(host='redis-serv', port=6379,password='celery_redis_pwd', db=1)

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())

## task装饰器, 把常规函数包装成任务对象.
## 之后可以在worker中注册(注册的意义就是表示这个worker用于处理这种任务的)
## 然后也可以在自己的系统中调用这个函数(通过task对象的delay()方法调用, 这样会把任务发送到broker, worker就会收到了)
@app.task(name="write-count-to-redis")
def write_into_redis(url):
    length = count_words_at_url(url)
    redis_conn.lpush('words_count', length)
