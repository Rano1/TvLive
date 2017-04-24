# 易直播TV（管理后台）
# -*- coding: utf-8 -*-
import socket
import json
import re
import select
import time
import urllib
import requests
from http import cookiejar
import hashlib
from captcha.rk import RClient

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'}
cookies = {
    "PHPSESSID": "",
    "sys_adminname": "",
    "sys_adminid": ""}

# 后台HOST
host = 'http://family.yizhibo.com/'
# 主播列表
url_anchor_list = host + 'info/index/anchor_list'
# 主播业绩
url_anchor_status = host + 'info/index/anchor_status'

# 主播列表
anchorList = []
# 主播业绩列表
anchorStatusList = []

ruokuai_username = "z86352868"
ruokuai_password = "86352868"
ruokuai_soft_id = "80287"
ruokuai_soft_key = "a467ec4e89f44a3191dc64e43a16e9a1"


class YiClient:
    def __init__(self):
        print("init YiClient")
        # 使用登录cookie信息
        self.isLogin = False
        self.session = requests.session()
        # 获取一个保存cookie的对象
        self.session.cookies = cookiejar.LWPCookieJar(filename='cookies_yi.txt')
        try:
            self.session.cookies.load(ignore_discard=True)
            self.isLogin = True
        except:
            print("还没有cookies信息")
            self.isLogin = False

    # 获取验证码
    def get_captcha(self):
        captcha_url = 'http://family.yizhibo.com/common/checkcode/checkcode?code_len=4&font_size=12&width=75&height=30&font_color=&background='
        r = self.session.get(captcha_url, headers=headers)
        with open('captcha.jpg', 'wb') as f:
            f.write(r.content)
        # captcha = input("请输入验证码：")
        # 通过若快破解验证码
        mRClient = RClient(ruokuai_username, ruokuai_password, ruokuai_soft_id, ruokuai_soft_key)
        im = open('captcha.jpg', 'rb').read()
        result = mRClient.rk_create(im, 3040)
        captcha = 0
        try:
            captcha = result['Result']
        except:
            pass
        print("验证码：" + captcha)
        return captcha

    # 登录
    def login(self, username, password):
        login_url = "http://family.yizhibo.com/account/login/init"
        print(self.getMd5(password))
        payload = {
            'dosubmit': 1,
            'username': username,
            'pwd': self.getMd5(password),
            "code": self.get_captcha(),
            'go': '/account/index/init'}
        response = self.session.post(login_url, data=payload, headers=headers)
        login_result = response.content
        print(login_result)
        self.session.cookies.save()

    # 获取MD5加密
    def getMd5(self, src):
        md5 = hashlib.md5()
        md5.update(src.encode(encoding='gb2312'))
        md5 = md5.hexdigest()
        # md5 = hashlib.md5(src.encode(encoding='gb2312'))
        return md5

    # 获取主播列表
    def getAnchorList(self, page):
        payload = {'page': page}
        data = urllib.parse.urlencode(payload)
        reuslt = requests.get(url_anchor_list, data=data, headers=headers, cookies=cookies).text
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

    # 抓取总页数
    # def getAnchorTotalPage(self):
    #     payload = {'page': 1}
    #     data = urllib.parse.urlencode(payload)
    #     reuslt = requests.get(url_anchor_list, data=data, headers=headers, cookies=cookies).text
    #     repositories = re.findall('<div class=\\"pagelist\\"><span class=\'nonelink\'>(.*?)</span>', reuslt, re.S)
    #     pageResult = re.match('共(.*?) 页/(.*?) 条', repositories[0])
    #     return int(pageResult.group(1))

    # 抓取总页数
    def getAnchorTotalPage(self):
        payload = {'page': 1}
        data = urllib.parse.urlencode(payload)
        reuslt = self.session.get(url_anchor_list, data=data, headers=headers).text
        repositories = re.findall('<div class=\\"pagelist\\"><span class=\'nonelink\'>(.*?)</span>', reuslt, re.S)
        pageResult = re.match('共(.*?) 页/(.*?) 条', repositories[0])
        return int(pageResult.group(1))

    # 获取主播业绩列表
    def getAnchorStatusList(self, page):
        payload = {'page': page}
        data = urllib.parse.urlencode(payload)
        reuslt = requests.get(url_anchor_status, data=data, headers=headers, cookies=cookies).text
        repositories = re.findall('<tbody>(.*?)</tbody>', reuslt, re.S)
        anchorGroup = re.findall('<tr>(.*?)</tr>', repositories[0], re.S)
        for anchor in anchorGroup:
            anchorItem = re.findall('<td class="td_bolder">(.*?)</td>', anchor, re.S)
            info = {}
            info['id'] = anchorItem[1]  # 主播ID
            info['nickname'] = anchorItem[2]  # 主播昵称
            info['gift_income'] = anchorItem[3]  # 礼物收入(元)
            info['gift_system'] = anchorItem[4]  # 系统赠送(元)
            info['diamond_income'] = anchorItem[5]  # 钻石收入(元)
            info['expire_day'] = anchorItem[6]  # 有效天
            info['live_time'] = anchorItem[7]  # 直播时长
            info['expire_duration'] = anchorItem[8]  # 有效时长
            info['fan_change'] = anchorItem[9]  # 粉丝变动
            anchorStatusList.append(info)

    # 抓取业绩总页数
    def getAnchorStatusTotalPage(self):
        payload = {'page': 1}
        data = urllib.parse.urlencode(payload)
        reuslt = requests.get(url_anchor_status, data=data, headers=headers, cookies=cookies).text
        repositories = re.findall('<div class=\\"pagelist\\"><span class=\'nonelink\'>(.*?)</span>', reuslt, re.S)
        pageResult = re.match('共(.*?) 页/(.*?) 条', repositories[0])
        return int(pageResult.group(1))


if __name__ == '__main__':
    username = ""
    password = ""
    yiClient = YiClient()
    # if not yiClient.isLogin:
    #     yiClient.login(username, password)
    yiClient.login(username, password)

    totalAnchorPage = yiClient.getAnchorTotalPage()
    print('总页数:', totalAnchorPage)

    page = 1
    while page <= totalAnchorPage:
        yiClient.getAnchorList(page)
        page = page + 1
    print('主播总数:', len(anchorList))

    totalAnchorStatusPage = yiClient.getAnchorStatusTotalPage()
    print('总页数:', totalAnchorStatusPage)
    page = 1
    while page <= totalAnchorStatusPage:
        yiClient.getAnchorStatusList(page)
        page = page + 1
    print('主播业绩总数:', len(anchorStatusList))
