# Skunkworks -Redis

Load data on premise
```
cat downloaded.csv | awk -F',' '{print " SET \""$1"\" \""$0"\" \n"}' | redis-cli --pipe 
```

Python file <code>redis.py</code>

```python

import redis
import time

t0= time.clock()

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
for k in redis_db.keys('*'):
    
    print(redis_db.get(k))

t1 = time.clock() - t0
print("Time elapsed: ", t1 - t0)
```
