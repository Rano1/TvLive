# 知乎模拟登录
import requests
import time
from http import cookiejar
from bs4 import BeautifulSoup

headers = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87',
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies_zhihu.txt')
try:
    print(session.cookies)
    session.cookies.load(ignore_discard=True)

except:
    print("还没有cookies信息")


# 获取html中的xsrf节点
def get_xsrf():
    response = session.get("https://www.zhihu.com", headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    xsrf = soup.find('input', attrs={"name": "_xsrf"}).get("value")
    return xsrf


# 获取验证码，可以选择手动输入或者是通过第三方库去自动识别
def get_captcha():
    # 把验证码保存在当前目录下手动识别
    t = str(int(time.time()) * 1000)
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + '&type=login'
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
    captcha = input("请输入验证码：")
    return captcha


# 登录
def login(email, password):
    login_url = "https://www.zhihu.com/login/email"
    payload = {
        'email': email,
        'password': password,
        '_xsrf': get_xsrf(),
        "captcha": get_captcha(),
        'remember_me': 'true'}
    response = session.post(login_url, data=payload, headers=headers)
    login_code = response.json()
    print(login_code)
    for i in session.cookies:
        print(i)
    session.cookies.save()


if __name__ == '__main__':
    email = "myfuture@vip.qq.com"
    password = ""
    login(email, password)
