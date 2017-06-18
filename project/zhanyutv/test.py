import sys
import re
import urllib.request
import urllib.parse
import urllib.error
import urllib
import requests
import http.cookiejar
from imp import reload

# 登录斗鱼,url on linux
loginurl = 'https://www.douyu.com/member/org_info/anchorsInfo'

class Login(object):
    def __init__(self):

    def login(self):
        '''登录网站'''
        #loginparams = {'domain': self.domain, 'email': self.name, 'password': self.pwd}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36',
            'cookie': self.cookie
        }
        req = urllib.request.Request(loginurl,headers=headers)
        response = urllib.request.urlopen(req)
        thePage = response.read().decode('utf-8')
        print('....ok')
        print(thePage)


if __name__ == '__main__':
    userlogin = Login()
    userlogin.login()
# test: auto login douyu by cookie