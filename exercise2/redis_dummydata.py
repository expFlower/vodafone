import redis
import time
import datetime


redisClient = redis.StrictRedis(host='localhost',port=6379,db=0)

while True:
    today = datetime.datetime.now()
    value = "World " + format(today)
    redisClient.set('Hello', value)
    time.sleep(300)










