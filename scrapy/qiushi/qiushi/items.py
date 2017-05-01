# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QiushiItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    content = scrapy.Field()
    img = scrapy.Field()
    funNum = scrapy.Field()
    talkNum = scrapy.Field()
