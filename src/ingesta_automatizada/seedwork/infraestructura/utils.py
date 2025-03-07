import os
import time


def time_millis():
    return int(time.time() * 1000)


def broker_host():
    return os.getenv('BROKER_HOST', default="localhost")
