#!/usr/bin/env python3

from tasks.task import app

if __name__ == '__main__':
    ## 以worker的身份运行, 作用类似于`celery -A tasks.task worker`
    app.worker_main()
