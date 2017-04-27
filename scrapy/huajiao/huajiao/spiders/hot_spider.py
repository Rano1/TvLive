# 花椒：热门

from scrapy.spiders import Spider
from scrapy.selector import Selector
import scrapy


class HotSpider(Spider):
    name = 'hot_spider'

    start_urls = [
        'http://www.huajiao.com/category/1000',
    ]

    # def start_requests(self):
    #     urls = [
    #         'http://www.huajiao.com/category/1000',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        sel = Selector(response)
        for sel in response.xpath('//*[@id="doc-bd"]/div/div/div [2]/div[1]/ul'):
            title = sel.xpath('li/a/p[1]/text()').extract()
            print(title)
