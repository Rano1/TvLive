# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ..items import AncharItem

class AnchorSpider(scrapy.Spider):
    name = "anchor"
    allowed_domains = ["douyu.com"]
    start_urls = ['https://www.douyu.com/directory/all/']

    # ajax_url = "https://www.douyu.com/directory/all?isAjax=1&page="
    ajax_url = "https://www.douyu.com/directory/all?page="
    all_page = 0  # 总页数
    current_page = 1  # 当前页数
    """
    1.获取主播列表页中的主播房间url，交给scrapy下载后进行解析
    1.获取下一页的url并交给scrapy进行下载，下载完成交给parse解析
    """
    def parse(self, response):
        select_list = response.xpath("//div[@id='live-list-content']//a[@class='play-list-link']")
        if self.all_page == 0:
            self.get_all_page(response)
        anchor_list = []
        for select in select_list:
            anchor = AncharItem()
            anchor['room_id'] = int(select.xpath('@data-rid').extract()[0])
            anchor['room_href'] = select.xpath('@href').extract()[0]
            anchor['room_title'] = select.xpath('@title').extract()[0]
            anchor['room_sid'] = int(select.xpath('@data-sid').extract()[0])
            anchor['anchor_nickname'] = select.xpath('.//span[contains(@class ,"dy-name")]/text()').extract()[0]
            anchor['view_nums'] = select.xpath('.//span[contains(@class ,"dy-num")]/text()').extract()[0]
            anchor_list.append(anchor)
            # 交给主播个人数据解析
            # yield Request(url=parse.urljoin(response.url, anchor['room_href']), callback=self.parse_anchor_info)
            yield anchor

        # 提取下一页并交给scrapy进行下载
        if self.current_page < self.all_page:
            self.current_page = self.current_page + 1
            url = self.ajax_url + str(self.current_page)
            print(url)
            yield Request(url=url, callback=self.parse)
        else:
            print("爬取结束")

    # 爬取主播个人数据
    def parse_anchor_info(self, response):
        pass

    # 爬取在播列表总页数 (发现斗鱼的页数是在js渲染出来，所以抓取html抓不到生成的节点，可以通过抓取script )
    def get_all_page(self, response):
        body = str(response.body)
        regex_str = ".*?PAGE.pager = ({.*?});.*"
        pager = re.match(regex_str, body)
        if pager:
            pager_data = pager.group(1).replace('\\n', '').replace('\\r', '').replace(" ", "")
            regex_str = '.*count:"(\d+)".*'
            self.all_page = int(re.match(regex_str, pager_data).group(1))
