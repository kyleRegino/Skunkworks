# Skunkworks - Cassandra

Create Keyspace on premise
```
CREATE KEYSPACE test_skunkworks WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} 
AND durable_writes = 'true';
```
Use Keyspace on premise
```
USE test_skunkworks ;
```
Create table of premise
```
CREATE TABLE test_NYC_taxi (pickup timestamp, dropoff timestamp, rate_code int, passenger_count int, trip_distance float, payment_type int, pickup_lat float, dropoff_lat float, 
PRIMARY KEY(pickup, dropoff, rate_code));
```
Import CSV on table
```
COPY test_NYC_taxi (pickup, dropoff, rate_code, passenger_count, trip_distance, payment_type, pickup_lat, dropoff_lat) 
FROM '/home/kyle/DataScientist/Skunworks/downloaded.csv' WITH DELIMITER=',' AND HEADER=TRUE;

```

Python file <code>cassandra.py</code>

```python

from cassandra.cluster import Cluster
import time

cluster = Cluster()

session = cluster.connect('test_skunkworks')

t0= time.clock()
rows = session.execute("SELECT * FROM test_NYC_taxi")

for row in rows:
    print(row.pickup, row.dropoff, row.rate_code, row.passenger_count, 
    row.trip_distance, row.payment_type, row.pickup_lat, row.dropoff_lat)

t1 = time.clock() - t0
print("Time elapsed: ", t1 - t0)
print('finish')
```
