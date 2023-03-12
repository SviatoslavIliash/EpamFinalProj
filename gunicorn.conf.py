# Gunicorn configuration file

import multiprocessing

max_requests = 1000
max_requests_jitter = 50

errorlog = '-'
loglevel = 'info'
accesslog = 'log.txt'

workers = multiprocessing.cpu_count() * 2 + 1
