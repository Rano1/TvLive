# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HuajiaoItem(scrapy.Item):
    nickname = scrapy.Field()   # 昵称
    popularity = scrapy.Field()   # 人气

