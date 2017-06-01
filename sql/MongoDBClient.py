# MongoDB模块
import pymongo
import json

__all__ = ['MongoDBClient']

class MongoDBClient(object):

    def __init__(self, platform):
        database = 'danmu'
        collection_douyu = 'douyu'
        # client = pymongo.MongoClient(host, port)
        # client = pymongo.MongoClient('mongodb://192.168.2.105:27017/')
        client = pymongo.MongoClient('mongodb://192.168.135.128:27017/')
        # 连接数据库
        db = client[database]
        # 连接聚集
        self.douyu_collection = db[collection_douyu]
        print('MongoDB init')

    def save_data(self, gift):
        self.douyu_collection.insert(gift)

