# 斗鱼TV，通过官方API文档
import socket
import json
import re
import select
import time
import requests


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


if (__name__ == '__main__'):
    roomId = 'wt55kai'
    danmu = DouYuDanMuClient()
    danmu.getInfo(roomId)
