import requests
from redis import Redis

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())

redis_conn = Redis(host='redis-serv', port=6379, db=1)

def write_into_redis(url):
    length = count_words_at_url(url)
    redis_conn.lpush('words_count', length)
