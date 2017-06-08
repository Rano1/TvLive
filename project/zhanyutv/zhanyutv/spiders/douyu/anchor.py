# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.http import Request

from db.redisclient import RedisClient
from zhanyutv.constants.tv_api import ApiHelper
# from scrapy.loader import ItemLoader
from zhanyutv.items import AncharItem


# 主播数据爬取(通过接口的方式)
class AnchorSpider(scrapy.Spider):
    name = "douyu_anchor"
    allowed_domains = []
    start_urls = [ApiHelper.get_api_douyu_list_url(0)]

    """
    1.获取主播列表页中的主播房间url，交给scrapy下载后进行解析
    1.获取下一页的url并交给scrapy进行下载，下载完成交给parse解析
    """

    offset = 0

    def __init__(self):
        print("__init__")
        self.redis_client = RedisClient().getInstance()

    def parse(self, response):
        is_end = False
        anchor_list = []
        anchor_uids = []
        if response.body:
            result = json.loads(response.body)
            if result and int(result['error']) == 0:
                result_anchor_list = result['data']
                result_count = len(result_anchor_list)
                print("result_count : " + str(result_count))
                if result_count > 0:
                    for anchor_item in result_anchor_list:
                        anchor = AncharItem()
                        anchor['room_id'] = anchor_item['room_id']
                        anchor['room_href'] = anchor_item['url']
                        anchor['room_name'] = anchor_item['room_name']
                        anchor['room_status'] = anchor_item['show_status']
                        anchor['room_thumb'] = anchor_item['room_src']
                        anchor['nickname'] = anchor_item['nickname']
                        anchor['avatar'] = anchor_item['avatar']
                        anchor['sex'] = 0
                        anchor['weight'] = 0  # owner_weight
                        anchor['cate_id'] = anchor_item['cate_id']
                        anchor['start_time'] = anchor_item['show_time']
                        anchor['fans_num'] = anchor_item['fans']
                        anchor['online_num'] = anchor_item['online']
                        anchor_list.append(anchor)
                        anchor_uids.append(anchor['room_id'])
                        # 交给主播个人数据解析
                        roominfo_url = ApiHelper.get_douyu_roominfo_url(anchor['room_id'])
                        # 如果有数据了，那就不获取了
                        anchor_redis_name = 'anchor:1' + ":" + str(anchor['room_id'])
                        if self.redis_client.exists(anchor_redis_name):
                            yield anchor
                        else:
                            yield Request(url=roominfo_url, callback=self.parse_anchor_info)
                else:
                    is_end = True

                self.offset = self.offset + result_count

        print(anchor_uids)

        # 提取下一页并交给scrapy进行下载
        if is_end:
            print("爬取结束")
        else:
            url = ApiHelper.get_api_douyu_list_url(self.offset)
            yield Request(url=url, callback=self.parse)

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
                anchor_info['sex'] = 0
                anchor_info['weight'] = 0  # owner_weight
                anchor_info['cate_id'] = result_anchor_info['cate_id']
                anchor_info['cate_name'] = result_anchor_info['cate_name']
                anchor_info['start_time'] = result_anchor_info['start_time']
                anchor_info['fans_num'] = result_anchor_info['fans_num']
                anchor_info['online_num'] = result_anchor_info['online']
                anchor_info['gift_list'] = result_anchor_info['gift']
                yield anchor_info
                # pass
