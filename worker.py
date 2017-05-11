"""
Worker process to listen for queued tasks.
"""

### IMPORTS ###################################################################
import os

import redis
from rq import Worker, Queue, Connection

### SETUP ######################################################################
listen = ['default']
redis_url = os.getenv('REDISTOGO_URL', 'redid://localhost:6379')
conn = redis.from_url(redis_url)

### RUN ON MAIN ###############################################################
if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
