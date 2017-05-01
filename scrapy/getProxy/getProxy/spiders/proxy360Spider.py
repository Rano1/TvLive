# -*- coding: utf-8 -*-
import scrapy


class Proxy360spiderSpider(scrapy.Spider):
    name = "proxy360Spider"
    allowed_domains = ["proxy360.cn"]
    start_urls = ['http://proxy360.cn/']

    def parse(self, response):
        pass
