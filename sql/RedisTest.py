# Redis测试
import redis

# host = '192.168.2.105'
host = '192.168.135.128'
port = 6379
password = 'zxcvbnm'

r = redis.StrictRedis(host=host, port=port, db=0, password=password)
r.hset('user', 'name', 'will')
