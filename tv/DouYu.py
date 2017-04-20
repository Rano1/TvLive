# 斗鱼TV，通过官方API文档
import socket
import json
import re
import select
import time
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'}
cookies = {
    "PHPSESSID": "",
    "sys_adminname": "",
    "sys_adminid": ""}

# 后台HOST
host = 'http://family.yizhibo.com/'
# 主播列表
url_anchor_list = host + 'info/index/anchor_list'

class DouYuDanMuClient(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.codeLocalToServer = 689
        self.codeServerToLocal = 690
        self.gid = -9999
        self.rid = 16789
        self.server = {}

    def getInfo(self, roomId):
        url = 'http://open.douyucdn.cn/api/RoomApi/room/%s' % roomId
        print(url)
        data = requests.get(url).json()
        if data.get('error') == 0:
            print(data)
        else:
            print("请求错误")

            # 获取主播列表

    # 获取后台
    def getAnchorList(self, page):
        payload = {'page': page}
        data = urllib.parse.urlencode(payload)
        reuslt = requests.get(url_anchor_list, data=data, headers=HEADERS, cookies=cookies).text
        repositories = re.findall('<tbody>(.*?)</tbody>', reuslt, re.S)
        anchorGroup = re.findall('<tr>(.*?)</tr>', repositories[0], re.S)
        for anchor in anchorGroup:
            anchorItem = re.findall('<td class="td_bolder">(.*?)</td>', anchor, re.S)
            info = {}
            # info['avatar'] = anchorItem[0]
            info['id'] = anchorItem[1]  # 主播ID
            info['nickname'] = anchorItem[2]  # 主播昵称
            info['sign_time'] = anchorItem[3]  # 签约时间
            info['expire_time'] = anchorItem[5]  # 到期日期
            info['sign_duration'] = anchorItem[4]  # 合约期限
            info['status'] = anchorItem[7]  # 进度
            anchorList.append(info)


if (__name__ == '__main__'):
    roomId = 'wt55kai'
    danmu = DouYuDanMuClient()
    danmu.getInfo(roomId)
