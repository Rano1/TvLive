# -*- coding: utf-8 -*-
import scrapy
from ..items import HuajiaoItem


class HuajiaospiderSpider(scrapy.Spider):
    name = "huajiaoSpider"
    allowed_domains = ["huajiao.com"]
    start_urls = ['http://www.huajiao.com/category/1000']

    def parse(self, response):
        sel_selector = response.xpath('//li[contains(@class ,"li-")]')
        items = []
        for sel in sel_selector:
            item = HuajiaoItem()
            item['id'] = sel.xpath('.//a/@href').extract()[0]
            item['name'] = sel.xpath('.//a/p[1]/text()').extract()[1]
            item['avatar'] = sel.xpath('.//a/p[1]/img/@src').extract()[0]
            item['img'] = sel.xpath('.//a/div[1]/img/@src').extract()[0]
            items.append(item)
        print(items)
        return items
