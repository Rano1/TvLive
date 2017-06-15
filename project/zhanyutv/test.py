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

        self.cookie = 'PHPSESSID=t9281ofbvate1g6ae5shvqgue0;acf_auth=2fa746dZprtqQazVpxAXjkwrQ%2BCZDTz1oO9tAgnSrZ4JtDHAXlEzFrDorZ8gpU5dDNXTfj8HeTAvtG0dM315cOHkWW5cramTcZm4r2%2B1Tupt4BeObu0Z;wan_auth37wan=47ce30b408ff%2Fo93iI23aWFzdJ%2FV2ksL53LEm8hu%2FdEIQoOyUBzYf2pBXDIzLp%2BN%2B5uAzsJdJz0TnBz91ii4m6C%2Bd8q614OVF4dP%2FztwyhIhw73Hdw;acf_uid=75983034;acf_username=75983034;acf_nickname=%E6%88%98%E9%B1%BC%E5%BE%B7%E5%B7%9E%E5%9C%88%E4%B8%B6%E5%91%A8%E5%91%A8Chris;acf_own_room=1;acf_groupid=1;acf_phonestatus=1;acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favanew%2Fface%2F201610%2F17%2F16%2F821fe9c5eb9308472483d501324f148d_;acf_ct=0;acf_ltkid=30398466;acf_biz=1;acf_stk=a7b06c5db3d87ab6;acf_devid=07ec8c2316e6f33c40e3e1cace74a21a;smidV2=201706131722237cf1b78a7a1187723d39d516fe6a371fe518a71684b1ebc40;Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1497345707;Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1497345823;_dys_lastPageCode=page_home,;acf_ccn=0d7ea82e00e1c05901eeca804e73299f;_dys_refer_action_code=show_topnavi_gameremind;'

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