# 斗鱼TV（管理后台）
import socket
import json
import re
import select
import time
import urllib
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'cache-control': "no-cache",
    'postman-token': "8f81f550-7a87-60da-7f41-6043c384c58c",
    "Content-type": "text/html;charset=utf-8",
    "Content-type": "text/html;charset=utf-8",
}
cookies = {
    'acf_did': '0E6BCB3E9C58AD8D2C78A58A2010F348',
    '_dys_lastPageCode': ',',
    'PHPSESSID': '8pcg46kefe4jddccujrrfhcj70',
    'acf_auth': 'bb44nCFTsH5O%2F%2B04DhoovCy2G4gGkHeethQuughqlEmLB7RWmSLpP%2FQJ9%2FRUxC8OYeATYKZ6Bko6n%2BXtCpLtEAt9xrAmCkDifC4gNOxEGui%2FklBiDR8K',
    'wan_auth37wan': 'b3da62561993QJqtFzKcvIzNWmDgPs5ToOvBxPaO2DBChL3wJ1NUi9eIJg%2BtruGAE7SZ5Niw38ZEiRimi9GkjQqS8o2VljwNXGyCgQVK8zHcW06Img',
    'acf_uid': '1',
    'acf_username': '1',
    'acf_nickname': '',
    'acf_own_room': '1',
    'acf_groupid': '1',
    'acf_phonestatus': '1',
    'acf_avatar': '',
    'acf_ct': '0',
    'acf_ltkid': '30398385',
    'acf_biz': '1',
    'acf_stk': 'd3ce804b1f94c93d',
    '_dys_refer_action_code': 'show_page_staydur',
    'Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7': '1491717257,1492256876,1492700081',
    'Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7': '1492700099'
}

# 后台HOST
host = 'https://www.douyu.com/member/org_info/'
# 主播列表
url_anchor_list = host + 'anchorsInfo'
# # 主播业绩
# url_anchor_status = host + 'info/index/anchor_status'

# 主播列表
anchorList = []
# 主播业绩列表
anchorStatusList = []


class DouYuAdminClient:
    def __init__(self):
        print("init DouYuAdminClient")

    # 获取主播列表
    def getAnchorList(self, page):
        payload = {
            'tag': 'normal',
            'page': page,
        }
        data = urllib.parse.urlencode(payload)
        reuslt = requests.get(url_anchor_list, data=data, headers=HEADERS, cookies=cookies).text
        print(reuslt)
        print(url_anchor_list)
        repositories = re.findall('<tbody>(.*?)</tbody>', reuslt, re.S)
        anchorGroup = re.findall('<tr>(.*?)</tr>', repositories[0], re.S)
        for anchor in anchorGroup:
            anchorItem = re.findall('<td .*?">(.*?)</td>', anchor, re.S)
            info = {}
            # info['avatar'] = anchorItem[0]
            info['nickname'] = anchorItem[1]  # 主播昵称
            info['room_id'] = anchorItem[2]  # 主播房间ID
            info['gender'] = anchorItem[3]  # 性别
            info['phone'] = anchorItem[4]  # 手机号码
            info['qq'] = anchorItem[5]  # QQ
            anchorList.append(info)

    # 抓取总页数
    def getAnchorTotalPage(self):
        payload = {'page': 1}
        data = urllib.parse.urlencode(payload)
        reuslt = requests.get(url_anchor_list, data=data, headers=HEADERS, cookies=cookies).text
        repositories = re.findall('<div class=\\"pagelist\\"><span class=\'nonelink\'>(.*?)</span>', reuslt, re.S)
        pageResult = re.match('共(.*?) 页/(.*?) 条', repositories[0])
        return int(pageResult.group(1))


if __name__ == '__main__':
    mDouYuAdminClient = DouYuAdminClient()
    # totalAnchorPage = mDouYuAdminClient.getAnchorTotalPage()
    # print('总页数:', totalAnchorPage)
    totalAnchorPage = 1;
    page = 1
    while page <= totalAnchorPage:
        mDouYuAdminClient.getAnchorList(page)
        page = page + 1
    print('主播总数:', len(anchorList))
