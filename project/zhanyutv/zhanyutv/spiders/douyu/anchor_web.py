# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy.http import Request
# from scrapy.loader import ItemLoader
from urllib import parse
from zhanyutv.items import AncharItem
from zhanyutv.items import AncharItemLoader
from api import apiconstants

# 主播数据爬取(通过web的方式)
class AnchorSpider(scrapy.Spider):
    name = "douyu_anchor_web"
    allowed_domains = ["douyu.com", "douyucdn.cn"]
    start_urls = ['https://www.douyu.com/directory/all/']


    # 通过这里面先获取页数，之后进行异步的请求各页的数据
    def start_requests(self):
        return [scrapy.Request('https://www.douyu.com/directory/all/', callback=self.get_all_page)]

    # 爬取在播列表总页数 (发现斗鱼的页数是在js渲染出来，所以抓取html抓不到生成的节点，可以通过抓取script )
    def get_all_page(self, response):
        all_page = 0  # 总页数
        current_page = 1  # 当前页数
        body = str(response.body)
        regex_str = ".*?PAGE.pager = ({.*?});.*"
        pager = re.match(regex_str, body)
        if pager:
            pager_data = pager.group(1).replace('\\n', '').replace('\\r', '').replace(" ", "")
            regex_str = '.*count:"(\d+)".*'
            all_page = int(re.match(regex_str, pager_data).group(1))
        print("all_page :" + str(all_page))
        # 提取下一页并交给scrapy进行下载
        while current_page <= all_page:
            url = apiconstants.get_douyu_list_url(current_page)
            print(url)
            current_page = current_page + 1
            yield Request(url=url, callback=self.parse)
        print("爬取结束")


    """
    1.获取主播列表页中的主播房间url，交给scrapy下载后进行解析
    1.获取下一页的url并交给scrapy进行下载，下载完成交给parse解析
    """
    def parse(self, response):
        select_list = response.xpath("//div[@id='live-list-content']//a[@class='play-list-link']")
        anchor_list = []
        anchor_uids = []
        for select in select_list:
            anchor = AncharItem()
            anchor['room_id'] = int(select.xpath('@data-rid').extract()[0])
            anchor['room_href'] = select.xpath('@href').extract()[0]
            anchor['room_name'] = select.xpath('@title').extract()[0]
            anchor['room_sid'] = int(select.xpath('@data-sid').extract()[0])
            anchor['nickname'] = select.xpath('.//span[contains(@class ,"dy-name")]/text()').extract()[0]
            anchor['online_num'] = select.xpath('.//span[contains(@class ,"dy-num")]/text()').extract()[0]
            anchor_list.append(anchor)
            # 交给主播个人数据解析
            roominfo_url = apiconstants.get_douyu_roominfo_url(anchor['room_id'])
            # print(roominfo_url)

            anchor_uids.append(anchor['room_id'])

            yield Request(url=roominfo_url, callback=self.parse_anchor_info)

            # 通过ItemLoader加载实例
            # item_loader = AncharItemLoader(item=AncharItem(), response=response)
            # item_loader.add_xpath("room_id", "@data-rid")
            # item_loader.add_xpath("room_href", "@href")
            # item_loader.add_xpath("room_name", "@title")
            # item_loader.add_xpath("room_sid", "@data-sid")
            # item_loader.add_xpath("nickname", './/span[contains(@class ,"dy-name")]/text()')
            # item_loader.add_xpath("online_num", './/span[contains(@class ,"dy-num")]/text()')
            # anchor = item_loader.load_item()
            # item_loader.add_value()

            # yield anchor

        print(anchor_uids)

        # # 提取下一页并交给scrapy进行下载
        # if self.current_page < self.all_page:
        #     self.current_page = self.current_page + 1
        #     url = self.ajax_url + str(self.current_page)
        #     print(url)
        #     yield Request(url=url, callback=self.parse)
        # else:
        #     print("爬取结束")

    # 爬取主播个人数据
    def parse_anchor_info(self, response):
        if response.body:
            result = json.loads(response.body)
            if result and int(result['error']) == 0:
                result_anchor_info = result['data']
                anchor_info = AncharItem()
                anchor_info['room_id'] = result_anchor_info['room_id']
                # anchor_info['room_href'] = result_anchor_info['room_href']
                anchor_info['room_href'] = ""
                anchor_info['room_name'] = result_anchor_info['room_name']
                anchor_info['room_status'] = result_anchor_info['room_status']
                anchor_info['room_thumb'] = result_anchor_info['room_thumb']
                anchor_info['nickname'] = result_anchor_info['owner_name']
                anchor_info['avatar'] = result_anchor_info['avatar']
                anchor_info['cate_id'] = result_anchor_info['cate_id']
                anchor_info['cate_name'] = result_anchor_info['cate_name']
                anchor_info['start_time'] = result_anchor_info['start_time']
                anchor_info['fans_num'] = result_anchor_info['fans_num']
                anchor_info['online_num'] = result_anchor_info['online']
                anchor_info['gift_list'] = result_anchor_info['gift']
                yield anchor_info
        # pass

