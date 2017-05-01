# -*- coding: utf-8 -*-
import scrapy


class QiushispiderSpider(scrapy.Spider):
    name = "qiushiSpider"
    allowed_domains = ["qiushibaike.com"]
    start_urls = ['http://qiushibaike.com/']

    def parse(self, response):
        pass
