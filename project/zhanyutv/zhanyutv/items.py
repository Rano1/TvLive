# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import datetime
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import TakeFirst
from scrapy.loader.processors import Join

class ZhanyutvItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AncharItemLoader(ItemLoader):
    # 自定义ItemLoader
    default_input_processor = TakeFirst()

class AncharItem(scrapy.Item):
    room_id = scrapy.Field(
        output_processor=TakeFirst()
    )  # 房间ID
    room_href = scrapy.Field()  # 房间链接
    room_sid = scrapy.Field()  # 房间SID
    room_name = scrapy.Field()  # 房间名称
    room_thumb = scrapy.Field()  # 房间封面
    nickname = scrapy.Field()  # 昵称
    avatar = scrapy.Field()  # 头像
    cate_id = scrapy.Field()  # 类别ID
    cate_name = scrapy.Field()  # 类别名称
    weight = scrapy.Field()  # 主播体重
    start_time = scrapy.Field()  # 开播时间（需要转成时间戳）
    fans_num = scrapy.Field()  # 粉丝数
    online_num = scrapy.Field()  # 在线人数
    gift_list = scrapy.Field()  # 礼物列表
