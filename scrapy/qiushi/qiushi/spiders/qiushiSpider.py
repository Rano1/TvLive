# -*- coding: utf-8 -*-
import scrapy
from ..items import QiushiItem

class QiushispiderSpider(scrapy.Spider):
    name = "qiushiSpider"
    allowed_domains = ["qiushibaike.com"]
    start_urls = ['http://www.qiushibaike.com/hot/']

    def parse(self, response):
        sel_selector = response.xpath('//div[contains(@id ,"qiushi_tag")]')
        items = []
        for sel in sel_selector:
            item = QiushiItem()
            if sel.xpath('./div[contains(@class ,"author")]/a[2]/h2/text()').extract():
                item['author'] = sel.xpath('./div[contains(@class ,"author")]/a[2]/h2/text()').extract()[0]
            else:
                item['author'] = sel.xpath('./div[contains(@class ,"author")]/span[2]/h2/text()').extract()[0]
            item['content'] = sel.xpath('./a[1]/div/span/text()').extract()[0]
            if sel.xpath('./div[@class="thumb"]/a/img/@src').extract():
                item['img'] = "http:" + sel.xpath('./div[@class="thumb"]/a/img/@src').extract()[0]
            else:
                item['img'] = ''
            item['funNum'] = sel.xpath('./div[@class="stats"]/span[@class="stats-vote"]/i/text()').extract()[0]
            item['talkNum'] = sel.xpath('./div[@class="stats"]/span[@class="stats-comments"]/a/i/text()').extract()[0]
            items.append(item)
            print(item)
        return items
