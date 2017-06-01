# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
from .db.RedisClient import RedisClient

PLATFORM_DOUYU = 1

class ZhanyutvPipeline(object):
    def process_item(self, item, spider):
        # 做存储
        return item


# 主播Pipeline
class AncharPipeline(object):
    def process_item(self, item, spider):
        # 做存储
        return item


# 主播JSON 文件存储Pipeline
class JsonWithEncodingPipeline(object):
    # 自定义JSON文件的导出
    def __init__(self):
        self.file = codecs.open('anchar.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()

# 调用Scrapy提供的JsonExporter导出JSON文件
class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open('anchar_export.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


# 图片保存Pipeline
class AncharImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value['path']
        item['image_file_path'] = image_file_path
        return item


# 采用同步的机制MySQL
class MysqlPipeline(object):
    def __init__(self, host, db, user, passwd):
        self.conn = MySQLdb.connect(host, user, passwd, db, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    @classmethod
    def from_settings(cls, settings):
        host = settings['MYSQL_HOST']
        db = settings['MYSQL_DBNAME']
        user = settings['MYSQL_USER']
        passwd = settings['MYSQL_PASSWORD']
        return cls(host, db, user, passwd)

    def process_item(self, item, spider):
        insert_sql = """
            insert into anthor(nickname,sex,platform,room_id,room_href,room_name)
            VALUES (%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,
                            (item['nickname'], 1, 1, item['room_id'], item['room_href'], item['room_name']))
        self.conn.commit()
        return item


# 异步处理MySQL操作
class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
        self.redis_client = RedisClient()

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 因为是异步的，所以错误的查询
        query.addErrback(self.handle_error)  # 处理异常
        # # 存入Redis礼物数据
        gift_list = item['gift_list']
        for gift in gift_list:
            gift_redis_name = 'gift:' + str(PLATFORM_DOUYU) + ":" + gift['id']  # 平台加礼物ID
            self.redis_client.getInstance().hmset(gift_redis_name, dict(gift))
        # 存入Redis主播数据
        item.pop('gift_list')
        anchor_redis_name = 'anchor:' + str(PLATFORM_DOUYU) + ":" + item['room_id']
        self.redis_client.getInstance().hmset(anchor_redis_name, dict(item))


    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = """
                    insert into anthor(nickname,sex,platform,room_id,room_href,room_name)
                    VALUES (%s,%s,%s,%s,%s,%s)
                """
        cursor.execute(insert_sql, (item['nickname'], 1, 1, item['room_id'], item['room_href'], item['room_name']))

    def handle_error(self, failure):
        # 处理异步插入的异常
        print(failure)
