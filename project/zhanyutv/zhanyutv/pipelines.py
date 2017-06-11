# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

import MySQLdb
import MySQLdb.cursors
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi

from conf import config
from api import apiconstants
from db.redisclient import RedisClient
from zhanyutv.items import AncharItem


class ZhanyutvPipeline(object):
    def process_item(self, item, spider):
        # 做存储
        if isinstance(item, AncharItem):
            pass
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
        dbparms = config.DB_config.get("mysql")
        db = config.database
        host = dbparms['host']
        user = dbparms['user']
        passwd = dbparms['password']
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
        dbparms = config.DB_config.get("mysql")
        dbparms['db'] = config.database
        dbparms['cursorclass'] = MySQLdb.cursors.DictCursor
        dbparms['use_unicode'] = True

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert_anthor, item)
        # 因为是异步的，所以错误的查询
        query.addErrback(self.handle_error)  # 处理异常
        anthor_id = int(item['room_id'])
        # # 存入Redis礼物数据
        gift_list = item['gift_list']
        if gift_list:
            for gift in gift_list:
                gift_redis_name = 'gift:' + str(apiconstants.PLATFORM_DOUYU) + ":" + gift['id']  # 平台加礼物ID
                self.redis_client.getInstance().hmset(gift_redis_name, dict(gift))
            # 存入Redis主播数据
            item.pop('gift_list')
        anchor_redis_name = 'anchor:' + str(apiconstants.PLATFORM_DOUYU) + ":" + str(anthor_id)
        self.redis_client.getInstance().hmset(anchor_redis_name, dict(item))  # 更新数据库数据
        anchor_id_list_redis_name = 'anchor_id_list:' + str(apiconstants.PLATFORM_DOUYU)
        self.redis_client.getInstance().sadd(anchor_id_list_redis_name, anthor_id)

    # 保存主播数据
    def do_insert_anthor(self, cursor, item):
        # 判断主播是否存在
        exist_sql = "select * from anthor where platform=%s and room_id=%s" % (1, item['room_id'])
        cursor.execute(exist_sql)
        cursor.fetchall()
        if cursor.rowcount == 0:
            print("不存在主播数据，入库")
            # 执行具体的插入
            insert_sql = """
                                insert into anthor(nickname,avatar,sex,weight,platform,room_id,room_href,room_name,room_thumb,cate_id,fans_num)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """
            cursor.execute(insert_sql, (
                item['nickname'], item['avatar'], item['sex'], item['weight'], 1, item['room_id'], item['room_href'],
                item['room_name'], item['room_thumb'], item['cate_id'], item['fans_num']))
        else:
            print("存在主播数据")

    # 保存主播礼物数据
    def do_insert_gift(self, cursor, item):
        # 判断主播是否存在
        exist_sql = "select * from gift where platform=%s and gid=%s" % (1, item['room_id'])
        cursor.execute(exist_sql)
        cursor.fetchall()
        if cursor.rowcount == 0:
            print("不存在主播数据，入库")
            # 执行具体的插入
            insert_sql = """
                                insert into gift(gid,name,desc,intro,platform,cost,contribution)
                                VALUES (%s,%s,%s,%s,%s,%s,%s)
                            """
            cursor.execute(insert_sql, (
                item['gid'], item['name'], item['desc'], item['intro'], item['platform'], item['cost'], item['contribution']))
        else:
            print("存在主播数据")


    def handle_error(self, failure):
        # 处理异步插入的异常
        print(failure)
