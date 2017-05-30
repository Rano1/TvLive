# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhanyutvItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AncharItem(scrapy.Item):
    room_id = scrapy.Field()  # 房间ID
    room_href = scrapy.Field()  # 房间链接
    room_sid = scrapy.Field()  # 房间SID
    room_title = scrapy.Field()  # 标题
    anchor_nickname = scrapy.Field()  # 昵称
    view_nums = scrapy.Field()  # 观看人数
