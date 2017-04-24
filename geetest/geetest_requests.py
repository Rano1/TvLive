# -*-coding:utf-8-*-

import requests
from bs4 import BeautifulSoup
import re
import random
import json
import time
import math
from PIL import Image

"""
for i in a.split("\n"):
	print "'%s':'%s',"%(i.split(":",1)[0].strip(),i.split(":",1)[1].strip())
"""


def request_process(s):
    cookies = {}

    hd1 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'uems.sysu.edu.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
    }

    url1 = """http://uems.sysu.edu.cn/jwxt/"""

    g1 = s.get(url1, headers=hd1, timeout=5)
    cookies = dict(g1.cookies)

    hd2 = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'uems.sysu.edu.cn',
        'Referer': 'http://uems.sysu.edu.cn/jwxt/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    url2 = """http://uems.sysu.edu.cn/jwxt/StartCaptchaServlet?ts=%s""" % (str(random.random()))

    g2 = s.get(url2, headers=hd2, cookies=cookies, timeout=5)
    json2 = json.loads(g2.content)
    gt = json2["gt"]
    challenge = json2["challenge"]
    # print challenge
    url3 = """http://api.geetest.com/getfrontlib.php?gt=%s&callback=geetest_%d""" % (
        gt, random.random() * 10000 + int(time.time() * 1000))
    hd3 = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'api.geetest.com',
        'Referer': 'http://uems.sysu.edu.cn/jwxt/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
    }

    g3 = s.get(url3, headers=hd3, cookies=cookies, timeout=5)
    cookies.update(dict(g3.cookies))

    url4 = """http://api.geetest.com/get.php?gt=%s&challenge=%s&product=float&offline=false&type=slide&callback=geetest_%d""" % (
        gt, challenge, random.random() * 10000 + int(time.time()))
    hd4 = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'api.geetest.com',
        'Referer': 'http://uems.sysu.edu.cn/jwxt/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
    }

    g4 = s.get(url4, headers=hd4, cookies=cookies, timeout=5)
    json4 = json.loads(re.findall("({.*?})", g4.content)[0])
    challenge = json4["challenge"]
    # print challenge
    hd5 = {
        'Accept': 'image/webp,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'uems.sysu.edu.cn',
        'Origin': 'http://uems.sysu.edu.cn',
        'Referer': 'http://uems.sysu.edu.cn/jwxt/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
    }

    bg = url1 + "geetest/" + json4["bg"]
    tf = open("bg.jpg", "wb")
    tf.write(s.get(bg, headers=hd5, cookies=cookies, timeout=5).content)
    tf.close()

    fullbg = url1 + "geetest/" + json4["fullbg"]
    tf = open("fullbg.jpg", "wb")
    tf.write(s.get(fullbg, headers=hd5, cookies=cookies, timeout=5).content)
    tf.close()

    slice = url1 + "geetest/" + json4["slice"]
    tf = open("slice.jpg", "wb")
    tf.write(s.get(slice, headers=hd5, cookies=cookies, timeout=5).content)
    tf.close()

    return gt, challenge, cookies


def image_process():
    a = [39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28, 29, 27, 26, 36, 37, 31, 30, 44, 45, 43, 42, 12, 13,
         23, 22, 14, 15, 21, 20, 8, 9, 25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4, 5, 19, 18, 16, 17]

    im = Image.open("bg.jpg")
    im_new = Image.new("RGB", (260, 116))
    width, height = im.size

    for row in range(2):
        for column in range(26):

            right = a[row * 26 + column] % 26 * 12 + 1
            down = 58 if a[row * 26 + column] > 25 else 0
            for w in range(10):
                for h in range(58):
                    ht = 58 * row + h
                    wd = 10 * column + w
                    # print ht, wd
                    im_new.putpixel((wd, ht), im.getpixel((w + right, h + down)))

    im_new.save("bg_after.jpg")

    im = Image.open("fullbg.jpg")
    im_new = Image.new("RGB", (260, 116))
    width, height = im.size

    for row in range(2):
        for column in range(26):

            right = a[row * 26 + column] % 26 * 12 + 1
            down = 58 if a[row * 26 + column] > 25 else 0
            for w in range(10):
                for h in range(58):
                    ht = 58 * row + h
                    wd = 10 * column + w
                    # print ht, wd
                    im_new.putpixel((wd, ht), im.getpixel((w + right, h + down)))

    im_new.save("fullbg_after.jpg")

    img1 = Image.open("bg_after.jpg")

    img2 = Image.open("fullbg_after.jpg")

    def diff(img1, img2, wd, ht):
        rgb1 = img1.getpixel((wd, ht))
        rgb2 = img2.getpixel((wd, ht))
        tmp1 = 0
        tmp2 = 0
        for i in range(3):
            tmp1 += rgb1[i]
            tmp2 += rgb2[i]
        if abs(tmp1 - tmp2) > 190:
            return True
        return False

    def col(img1, img2, cl):
        for i in range(img2.size[1]):
            if diff(img1, img2, cl, i):
                return True
        return False

    def judge(img1, img2):
        for i in range(img2.size[0]):
            if col(img1, img2, i):
                return i
        return -1

    xpos = judge(img1, img2) - 6

    # print "xpos", xpos
    return xpos


def gee_c(a):
    e = []
    f = 0
    g = []
    h = 0
    for h in range(len(a) - 1):
        b = int(round(a[h + 1][0] - a[h][0]))
        c = int(round(a[h + 1][1] - a[h][1]))
        d = int(round(a[h + 1][2] - a[h][2]))
        g.append([b, c, d])
        if b == 0 and c == 0 and d == 0:
            pass
        elif b == 0 and c == 0:
            f += d
        else:
            e.append([b, c, d + f])
            f = 0
    if f != 0:
        e.append([b, c, f])
    return e


def gee_d(a):
    b = "()*,-./0123456789:?@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqr"
    c = len(b)
    d = ""
    e = abs(a)
    f = e / c
    if f >= c: f = c - 1
    if f: d = b[f]
    e %= c
    g = ""
    if a < 0: g += "!"
    if d: g += "$"
    return g + d + b[e]


def gee_e(a):
    b = [[1, 0], [2, 0], [1, -1], [1, 1], [0, 1], [0, -1], [3, 0], [2, -1], [2, 1]]
    c = "stuvwxyz~"
    for d in range(len(b)):
        if a[0] == b[d][0] and a[1] == b[d][1]:
            return c[d]
    return 0


def gee_f(a):
    g = []
    h = []
    i = []
    for j in range(len(a)):
        b = gee_e(a[j])
        if b:
            h.append(b)
        else:
            g.append(gee_d(a[j][0]))
            h.append(gee_d(a[j][1]))
        i.append(gee_d(a[j][2]))
    return "".join(g) + "!!" + "".join(h) + "!!" + "".join(i)


def gee_userresponse(a, b):
    c = b[32:]

    d = []
    for i in range(len(c)):
        f = ord(c[i])
        d.append(f - 87 if f > 57 else f - 48)
    c = 36 * d[0] + d[1]
    g = round(a) + c
    b = b[0:32]
    i = [[], [], [], [], []]
    j = {}
    k = 0
    for e in range(len(b)):
        h = b[e]
        if h not in j:
            j[h] = 1
            i[k].append(h)
            k = k + 1
            if k == 5: k = 0

    n = g
    o = 4
    p = ""
    q = [1, 2, 5, 10, 50]
    while n > 0:
        if n - q[o] >= 0:
            m = int(random.random() * len(i[o]))
            p += str(i[o][m])

            n -= q[o]
        else:
            i = i[:o] + i[o + 1:]
            q = q[:o] + q[o + 1:]
            o -= 1
    return p


def darbra_trace(distance):
    y_float = 0.0
    xps = distance

    last_move = random.randint(3, 3) * random.choice([1, 1])
    distance += last_move
    maxdst = distance
    ans = []
    ttt = 0
    tans = [[-24, -16, 0], [0, 0, 0]]
    first = True
    second = True
    while distance > 0:
        pass
    # 这里的轨迹代码已删除
    return tans


def position_process(xpos, s, gt, challenge, cookies):
    act_pre = darbra_trace(xpos)
    # print act_pre
    act = gee_c(act_pre)

    enc_act = gee_f(act)
    print(enc_act)
    passtime = act_pre[-1][-1]
    time.sleep(0.5)
    passtime = str(passtime)
    imgload = str(random.randint(0, 200) + 50)
    userresponse = gee_userresponse(xpos, challenge)
    time.sleep(0.4)
    url6 = "http://api.geetest.com/ajax.php?gt=%s&challenge=%s&userresponse=%s&passtime=%s&imgload=%s&a=%s&callback=geetest_%d" % (
        gt, challenge, userresponse, passtime, imgload, enc_act, random.random() * 10000 + int(time.time() * 1000))

    hd6 = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'api.geetest.com',
        'Referer': 'http://uems.sysu.edu.cn/jwxt/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
    }

    g6 = s.get(url6, headers=hd6, cookies=cookies, timeout=5)
    # print g6.content
    json6 = json.loads(re.findall("({.*?})", g6.content)[0])
    print(json6)


def refresh(s, gt, challenge, cookies):
    url = "http://api.geetest.com/refresh.php?challenge=%s&gt=%s&callback=geetest_%d" % (
        challenge, gt, random.random() * 10000 + int(time.time() * 1000))
    headers7 = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'api.geetest.com',
        'Referer': 'http://uems.sysu.edu.cn/jwxt/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)  Safari/537.36',
    }

    g7 = s.get(url, headers=headers7, cookies=cookies)
    json7 = json.loads(re.findall("({.*?})", g7.content)[0])
    challenge = json7["challenge"]
    # print challenge
    hd5 = {
        'Accept': 'image/webp,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'uems.sysu.edu.cn',
        'Origin': 'http://uems.sysu.edu.cn',
        'Referer': 'http://uems.sysu.edu.cn/jwxt/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
    }
    url1 = """http://uems.sysu.edu.cn/jwxt/"""
    bg = url1 + "geetest/" + json7["bg"]
    tf = open("bg.jpg", "wb")
    tf.write(s.get(bg, headers=hd5, cookies=cookies, timeout=5).content)
    tf.close()

    fullbg = url1 + "geetest/" + json7["fullbg"]
    tf = open("fullbg.jpg", "wb")
    tf.write(s.get(fullbg, headers=hd5, cookies=cookies, timeout=5).content)
    tf.close()

    slice = url1 + "geetest/" + json7["slice"]
    tf = open("slice.jpg", "wb")
    tf.write(s.get(slice, headers=hd5, cookies=cookies, timeout=5).content)
    tf.close()
    return challenge


for i in range(100):
    print(i)
    try:
        s = requests.session()
        gt, challenge, cookies = request_process(s)
        xpos = image_process()
        if xpos > 100: continue
        print(xpos)
        position_process(xpos, s, gt, challenge, cookies)
        s.close()
    except:
        continue

    time.sleep(1)
