# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import os.path
import requests
import codecs
import json
import pymysql


class WeatherPipeline(object):
    def process_item(self, item, spider):
        cityDate = item['cityDate']
        week = item['week']
        img = item['img']
        temperature = item['temperature']
        weather = item['weather']
        wind = item['wind']
        # 打开数据库连接
        conn = pymysql.connect(
            host='192.168.2.104',
            port=3306,
            user='root',
            passwd='12%^&HGHJ&^%^>LOJGR',
            db='scrapyDB',
            charset='utf8')
        # 使用cursor()方法获取操作游标
        cur = conn.cursor()
        sql = "insert into weather(city_data,week,img,temperature,weather,wind) values ('%s','%s','%s','%s','%s','%s')" % (
            cityDate, week, img, temperature, weather, wind)
        print(sql)
        # 使用execute方法执行SQL语句
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()
        return item
