# Skunkworks -Redis
App Server - used as data storage
DB Server - used to perform reading of data from app server

Load data from DB server to App Server using <code>import_csv.py</code>
```python
import csv
import redis
import time
import pandas

#START TIME
t = time.localtime()
start_time = time.strftime("%H:%M:%S", t)
#print(start_time)

#CONNECT TO REDIS --------------------------------------------------------------------
# db as app server
# redis_db = redis.StrictRedis(host="ec2.compute.amazonaws.com", port=8090, db=0)


t0= time.time()

# df = pandas.read_csv('downloaded.csv')
df = pandas.read_csv('skunkworks.csv')

data = {}
columns = ['pickup', 'dropoff', 'distance', 'fare', 'p_long', 'p_lat', 'd_long', 'd_lat']
# columns = ['pickup', 'dropoff', 'rate_code', 'passenger_count', 'trip_distance', 'payment_type', 'pickup_lat', 'dropoff_lat']

count = 0 # galing sa csv
count_redis = 0 # nasa redis
for index, row in df.iterrows():
    value = {}
    for column in columns:
        value[column] = row[column]
        
    data[index] = value
    count+=1


for key, value in data.items():
    redis_db.set(key, str(value))
    count_redis+=1

#Time after process
t1 = time.time() - t0


#PRINT INFO
print("Number of processed rows: ",count)
print("Time elapsed (set all key:value): ", t1)
print("Number of processed rows in Redis: ",count_redis)
print(t2)

#END TIME
t_1 = time.localtime()
end_time = time.strftime("%H:%M:%S", t_1)

#TOTAL PROCESS TIME OF REDIS
total_time = t1-t0


def get_var_value(filename="redis_import.txt"):
    with open(filename, "a+") as f:
        f.seek(0)
        val = int(f.read() or 0) + 1
        f.seek(0)
        f.truncate()
        f.write(str(val))
        return val

your_counter = get_var_value()
print("This script has been run {} times.".format(your_counter))

#SAVE DATA TO CSV
with open('redis_import_logs.csv', mode='a') as file:
    
    headers = ['Import count', 'Time start', 'Time end', 'Total process time', 'Time elapsed (set all key:value)','Number of processed rows in Redis', 'Number of processed rows']
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    file.seek(0, 2)
    
    if file.tell() == 0:
        writer.writerow(headers)

    writer.writerow([your_counter, start_time, end_time, total_time, t1, count_redis, count])

```

Read file using python file <code>redis.py</code> in DB server

```python
import redis
import time
import csv
import os.path

#START TIME
t = time.localtime()
start_time = time.strftime("%H:%M:%S", t)
#print(start_time)


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


#PRINT INFO
print("start time: ", t0)
print("1st elapse: ", t1)
print("2nd elapse: ", t2)
print("3rd elapse: ", t3)
print("Time elapsed (get all keys only): ", time_keys)
print("Time elapsed (get all keys and value): ", time_keys_values)
print("Time elapsed (get specific key): ", time_key)
print("Number of processed rows: ",count)

#END TIME
t_1 = time.localtime()
end_time = time.strftime("%H:%M:%S", t_1)

#TOTAL PROCESS TIME OF REDIS
total_time = t3-t0

print("Start time", start_time)
print("End time", end_time)
print("This process took %.2f seconds" % total_time)


def get_var_value(filename="redis_process.txt"):
    with open(filename, "a+") as f:
        f.seek(0)
        val = int(f.read() or 0) + 1
        f.seek(0)
        f.truncate()
        f.write(str(val))
        return val

your_counter = get_var_value()
print("This script has been run {} times.".format(your_counter))


#SAVE DATA TO CSV
with open('redis_process_logs.csv', mode='a') as csvfile:

    headers = ['CSV count', 'Time start', 'Time end', 'Total process time', 'Time elapsed (get all keys only)', 'Time elapsed (set all key:value)', 'Time elapsed (get specific key)', 'Number of processed rows']
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    csvfile.seek(0, 2)
    
    if csvfile.tell() == 0:
        writer.writerow(headers)

    writer.writerow([your_counter, start_time, end_time, total_time, time_keys, time_keys_values, time_key, count])

```
