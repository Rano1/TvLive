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
        self.cookie = 'PHPSESSID=nkvcgh09pih8jn8dp4rfbicc86; acf_auth=3f33H8Hy4YnbIT%2BXBHIzUk39gr1kekSGiXqyb%2FDNlMk59EHcu2bDF1kk%2FxDXG0Z7kxYye4ulGTAjj2uQ3C9AGi5J1dTSdT%2BkQbrn7GER3a21DGbMD6RC; wan_auth37wan=25911f003529uLAw8zFw5gCy5Qdoi20E02gc6kZ4H7gH3pmgUGjYy9dy22En2IMa4kIcAKuuZjMQmUkY5JEHTlJS%2F8tRxbIs8h%2FTo6dKqx1oaWZzOw; acf_uid=75983034; acf_username=75983034; acf_nickname=%E6%88%98%E9%B1%BC%E5%BE%B7%E5%B7%9E%E5%9C%88%E4%B8%B6%E5%91%A8%E5%91%A8Chris; acf_own_room=1; acf_groupid=1; acf_phonestatus=1; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favanew%2Fface%2F201610%2F17%2F16%2F821fe9c5eb9308472483d501324f148d_; acf_ct=0; acf_ltkid=30398440; acf_biz=1; acf_stk=2aac8e54ac48def3; acf_devid=22ca6f714eb82b2d13ac09166ac5e788; _dys_lastPageCode=page_home,page_home; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1495621297,1495771169,1496376491,1496724805; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1496725601; _dys_refer_action_code=show_liftnavi_game_webremind'

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