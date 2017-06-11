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

        self.cookie = 'PHPSESSID=pv296o53ldm2hsuok5fvuenm34; acf_did=333026D1FCF84179CA0F741D04E749E0; acf_auth=6df5PlfGk%2Fn2J1TE5f7saO%2FSahZYNEyLHvq92qeuSp5yV3QIVr7fEWlXuWcNOQXWsY4LiZ50RSZQB3G5P1BXgwn4hbcEkSrQO%2FtttmDGsAcs8T8caltk; wan_auth37wan=7aaeac403cf90cxdokys%2Bd7EbsDC%2BX55rJuMIs8%2BaP6%2B%2FQWHef1VIVW%2B29ifuu%2BqlcXPPxSZD%2BxG%2FnEVQXWApTidiOpmtP7GwZ1mHm7dMQeJvl%2BoVg; acf_uid=75983034; acf_username=75983034; acf_nickname=%E6%88%98%E9%B1%BC%E5%BE%B7%E5%B7%9E%E5%9C%88%E4%B8%B6%E5%91%A8%E5%91%A8Chris; acf_own_room=1; acf_groupid=1; acf_phonestatus=1; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favanew%2Fface%2F201610%2F17%2F16%2F821fe9c5eb9308472483d501324f148d_; acf_ct=0; acf_ltkid=30398444; acf_biz=1; acf_stk=b40f04a63331f5d9; _dys_lastPageCode=page_home,page_home; _dys_refer_action_code=init_page_home; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1495617202,1495693735,1496392529,1496740851; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1496976761; acf_ccn=373e24d11f45f32d632bb526d9548c20'

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