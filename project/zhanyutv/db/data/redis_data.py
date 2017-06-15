# coding:utf-8

import redis
import time
import datetime
from conf import config


class RedisData:
    redis_params = config.DB_config.get("redis")
    pool = redis.ConnectionPool(host=redis_params.get("host"), port=redis_params.get("port"), db=0,
                                password=redis_params.get("password"))
    '''
    添加主播基础数据
    
    '''
    @staticmethod
    def add_anchor_info(anchor_info):
        # 从redis连接池取一条连接
        r = redis.Redis(connection_pool=RedisData.pool)
        # hash存储
        r.hset("zyh.anchor.info." + anchor_info["pid"] + "." + anchor_info["id"], anchor_info)
        # 添加主播ID集合
        r.sadd("zys.anchor.all." + anchor_info["pid"], anchor_info["id"])

    @staticmethod
    def add_cate_info(platform, cate_info):
        # 存入Redis
        r = redis.Redis(connection_pool=RedisData.pool)
        cate_redis_name = 'cate:' + str(platform) + ":" + cate_info['cate_id']  # 平台类别
        r.hmset(cate_redis_name, dict(cate_info))

    @staticmethod
    def add_gift_info(redis_client, platform, gift_info):
        if redis_client is None:
            redis_client = redis.Redis(connection_pool=RedisData.pool)
        # 存入Redis
        gift_redis_name = 'gift:%s:%s' % (str(platform), gift_info['gfid'])  # 平台加礼物ID
        redis_client.hmset(gift_redis_name, dict(gift_info))
