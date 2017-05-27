# 陌陌，通过数据抓取
import socket
import json
import urllib.parse
import re
import select
import time
import requests

HEADERS = {
    'user-agent': 'Mozilla/5.0',
    "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "text/plain"}


class MomoClien(object):
    def __init__(self):
        print("init MomoClien")

    def getInfo(self, roomId):
        url = 'https://web.immomo.com/webmomo/api/scene/profile/infosv2'
        payload = {'stid': roomId, 'src': 'url'}
        cookies = {
            's_id': '9f8f7b872d854abee247468b1654deaa',
            'cId': '49121262319856',
            'Hm_lvt_c391e69b0f7798b6e990aecbd611a3d4': '1492491213',
            'Hm_lpvt_c391e69b0f7798b6e990aecbd611a3d4': '1492491231'
        }
        data = urllib.parse.urlencode(payload)
        response = requests.post(url, data=data, headers=HEADERS, cookies=cookies)
        if response.status_code == requests.codes.ok:
            response_json = json.loads(response.text)
            print(response_json)

    # 获取房间列表
    def getList(self):
        room_set = set()
        while True:
            payload = {'page': page, 'item': -3, 'live': "false"}
            page += 1
            r = requests.post("https://web.immomo.com/webmomo/api/scene/recommend/lists", data=payload, headers=header)
            js = r.json()
            for room in js['data']['r_infos']:
                room_set.add(room['stid'])
            if not js['data']['h_next']:
                break
        return room_set


if __name__ == '__main__':
    roomId = '23501954'
    momoClinet = MomoClien()
    momoClinet.getInfo(roomId)
    room_set = momoClinet.getList()
    for room in room_set:
        print(room)
