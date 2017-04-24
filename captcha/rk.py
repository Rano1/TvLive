#!/usr/bin/env python
# coding:utf-8
# 若快打码 www.ruokuai.com
import requests
import hashlib
import json

class RClient(object):
    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = self.getMd5(password)
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()

    # 获取MD5加密
    def getMd5(self, src):
        md5 = hashlib.md5()
        md5.update(src.encode(encoding='gb2312'))
        md5 = md5.hexdigest()
        # md5 = hashlib.md5(src.encode(encoding='gb2312'))
        return md5

if __name__ == '__main__':
    username = "z86352868"
    password = "86352868"
    soft_id = "80287"
    soft_key = "a467ec4e89f44a3191dc64e43a16e9a1"
    rc = RClient(username, password, soft_id, soft_key)
    im = open('captcha.jpg', 'rb').read()
    result = rc.rk_create(im, 3040)
    captcha = 0
    try:
        captcha = result['Result']
    except:
        pass
    print(captcha)
