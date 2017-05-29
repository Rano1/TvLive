# 测试MongoDB工具
import pymongo

host = '192.168.2.105'
port = 27017
database = 'danmu'
collection_douyu = 'douyu'
# client = pymongo.MongoClient(host, port)
client = pymongo.MongoClient('mongodb://192.168.2.105:27017/')
# 连接数据库
db = client[database]
# 连接聚集
collection = db[collection_douyu]


print(collection.find_one())