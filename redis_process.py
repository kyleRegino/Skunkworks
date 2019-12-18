import redis
import time
import csv
import os.path

#START TIME
t = time.localtime()
start_time = time.strftime("%H:%M:%S", t)

t0= time.time()
count = 0 
# app as db server
# redis_db = redis.StrictRedis(host="ec2-54-179-183-215.ap-southeast-1.compute.amazonaws.com", port=8000, db=0)

# db as app server
redis_db = redis.StrictRedis(host="172.31.40.140", port=8090, db=0)

#GENERATE DATA IN REDIS-------------------------------------------------------------------------------------

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


def get_var_value(filename="redis_process_server.txt"):
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

