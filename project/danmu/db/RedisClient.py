# Redis工具
import redis

__all__ = ['MongoDBClient']


class RedisClient(object):
    def __init__(self):
        # host = '192.168.2.105'
        host = '192.168.135.128'
        port = 6379
        password = 'zxcvbnm'
        self.redis_client = redis.StrictRedis(host=host, port=port, db=0, password=password)

    def getInstance(self):
        return self.redis_client
