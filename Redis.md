# Skunkworks -Redis

Load data on premise
```
cat downloaded.csv | awk -F',' '{print " SET \""$1"\" \""$0"\" \n"}' | redis-cli --pipe 
```

Python file <code>redis.py</code>

```python
import redis
import time
import csv

t = time.localtime()
start_time = time.strftime("%H:%M:%S", t)
print(start_time)


t0= time.time()
count = 0
# create a connection to the localhost Redis server instance, by
# default it runs on port 6379

# local server
redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)

# app as db server
# redis_db = redis.StrictRedis(host="ec2-54-179-183-215.ap-southeast-1.compute.amazonaws.com", port=8000, db=0)

# db as app server
# redis_db = redis.StrictRedis(host="ec2-13-229-215-30.ap-southeast-1.compute.amazonaws.com", port=8090, db=0)

#generate dataset in redis


# see what keys are in Redis
print(redis_db.keys())
t1 = time.time()
time_keys = t1 -t0

# get all keys and print
for k in redis_db.keys('*'):
    print(redis_db.get(k))
    count += 1
t2 = time.time()
time_keys_values = t2 -t1

#get specific key
print("-------------------------------------------------------------------------")
print(redis_db.get('299425'))
t3 = time.time()
time_key = t3 - t2

print("start time: ", t0)
print("1st elapse: ", t1)
print("2nd elapse: ", t2)
print("3rd elapse: ", t3)
print("Time elapsed (get all keys only): ", time_keys)
print("Time elapsed (get all keys and value): ", time_keys_values)
print("Time elapsed (get specific key): ", time_key)
print("Number of processed rows: ",count)

t_1 = time.localtime()
end_time = time.strftime("%H:%M:%S", t_1)
print(end_time)
```
