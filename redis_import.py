import csv
import redis
import time
import pandas

#START TIME
t = time.localtime()
start_time = time.strftime("%H:%M:%S", t)


#CONNECT TO REDIS --------------------------------------------------------------------

# app as db server
# redis_db = redis.StrictRedis(host="ec2-54-179-183-215.ap-southeast-1.compute.amazonaws.com", port=8000, db=0)

# db as app server
redis_db = redis.StrictRedis(host="172.31.40.140", port=8090, db=0)


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

    redis_db.set(index, str(value))  
    # data[index] = value
    count+=1


# for key, value in data.items():
#     redis_db.set(key, str(value))
#     count_redis+=1

#Time after process
t1 = time.time() - t0


#PRINT INFO
print("Number of processed rows: ",count)
print("Time elapsed (set all key:value): ", t1)
print("Number of processed rows in Redis: ",count_redis)

#END TIME
t_1 = time.localtime()
end_time = time.strftime("%H:%M:%S", t_1)

#TOTAL PROCESS TIME OF REDIS
total_time = t1


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
