import Redis
from apscheduler.jobstores import redis

red = redis.Redis(
    host='redis-17914.c274.us-east-1-3.ec2.cloud.redislabs.com'
    port=17914
    password='AoZ4TZ2sAScHXk0qkaVljW1UJuTbJ2YK'
)