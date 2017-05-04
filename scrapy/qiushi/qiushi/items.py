# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QiushiItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()  # 作者
    content = scrapy.Field()  # 内容
    img = scrapy.Field()  # 图片
    funNum = scrapy.Field()  # 点赞数量
    talkNum = scrapy.Field()  # 评论数量
