# Redis工具
import redis
import config
__all__ = ['MongoDBClient']


class RedisClient(object):
    def __init__(self):
        
        host = config.DB_config.get('redis').get('host')
        port = config.DB_config.get('redis').get('port')
        password = config.DB_config.get('redis').get('password')
        db = config.DB_config.get('redis').get('db')
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db, password=password)

    def getInstance(self):
        return self.redis_client
