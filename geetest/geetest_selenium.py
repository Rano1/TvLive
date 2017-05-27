# -*-coding:utf-8-*-

from selenium import webdriver
from PIL import Image
import time
import random
import re
import requests
import math
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

"""
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
        )

br = webdriver.PhantomJS(desired_capabilities=dcap)
"""
br = webdriver.Chrome()
br.maximize_window()
times = 1
while times > 0:
    br.get("https://www.douyu.com/member/login")
    # br.get("http://www.jianshu.com/sign_in")
    wait = WebDriverWait(br, 40, 1.0)
    # element = wait.until(EC.presence_of_element_located((By.ID, "session_email_or_mobile_number")))
    element = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    element.send_keys("test")
    time.sleep(1.2)
    # element = wait.until(EC.presence_of_element_located((By.ID, "session_password")))
    element = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    element.send_keys("test123")
    time.sleep(1.2)

    # 点击验证码区域
    element_radar_tip = br.find_element_by_class_name("geetest_radar_tip")
    ActionChains(br).click_and_hold(on_element=element_radar_tip).perform()
    ActionChains(br).release(on_element=element_radar_tip).perform()
    # element_radar_tip.submit()
    time.sleep(5)
    # 获取验证码



    hd = {
        'Accept': 'image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'static.geetest.com',
        'Origin': 'http://www.jianshu.com',
        'Referer': 'http://www.jianshu.com/sign_in',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1979.0 Safari/537.36',
    }

    wait = WebDriverWait(br, 40, 1.0)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gt_cut_fullbg_slice")))
    print(element.get_attribute('style'))
    try:
        tmp1 = re.findall('url\("(.*?)"\)', element.get_attribute('style'))[0].replace("webp", "jpg")
    except:
        tmp1 = re.findall('url\((.*?)\)', element.get_attribute('style'))[0].replace("webp", "jpg")
    print(tmp1)

    element = br.find_element_by_class_name("gt_cut_bg_slice")
    try:
        tmp2 = re.findall('url\("(.*?)"\)', element.get_attribute('style'))[0].replace("webp", "jpg")
    except:
        tmp2 = re.findall('url\((.*?)\)', element.get_attribute('style'))[0].replace("webp", "jpg")
    print(tmp2)
    cookies = {}
    for i in br.get_cookies():
        cookies[i['name']] = i['value']
    print(cookies)
    tf = open("fullbg.jpg", "wb")
    tf.write(requests.get(tmp1).content)
    tf.close()

    tf = open("bg.jpg", "wb")
    tf.write(requests.get(tmp2).content)
    tf.close()


    def image_process():
        a = [39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28, 29, 27, 26, 36, 37, 31, 30, 44, 45, 43, 42, 12,
             13, 23, 22, 14, 15, 21, 20, 8, 9, 25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4, 5, 19, 18, 16, 17]

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
            tmp = 0
            for i in range(3):
                if abs(rgb1[i] - rgb2[i]) > 50:
                    tmp += 1
            if tmp == 3:
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

        print(xpos)
        return xpos


    xpos = image_process()


    # def darbra_track(distance):
    #     last_move = random.randint(3, 5) * random.choice([1, 1])
    #     distance += last_move
    #     maxdst = distance
    #     ans = []
    #     # while distance > 0:
    #     #     # 轨迹代码已删除
    #     #     pass
    #     return ans
    def darbra_track(distance):
        maxdst = distance
        last_move = 0
        distance = 0
        ans = []
        if maxdst > 0:
            rand_max = int(maxdst / 6)
            if rand_max < 2:
                rand_max = 2
            while distance < maxdst:
                # last_move = random.randint(3, 5) * random.choice([1, 1])
                last_move = random.randint(1, rand_max) * random.choice([1, 4])
                if ((distance + last_move) > maxdst):
                    last_move = maxdst - distance
                distance += last_move
                print(distance)
                ans.append([last_move, 0, random.choice([1, 10]) / 10])
        return ans


    array_trail = darbra_track(xpos)
    print(array_trail)
    element = br.find_element_by_class_name("gt_slider_knob")
    ActionChains(br).click_and_hold(on_element=element).perform()
    for x, y, t in array_trail:
        print(x, y, t)
        ActionChains(br).move_to_element_with_offset(
            to_element=element,
            xoffset=x + 22,
            yoffset=y + 22).perform()
        ActionChains(br).click_and_hold().perform()
        time.sleep(t)
    time.sleep(0.24)
    ActionChains(br).release(on_element=element).perform()
    time.sleep(2)
    wait = WebDriverWait(br, 40, 1.0)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gt_info_text")))
    print(element.text)

    wait = WebDriverWait(br, 40, 1.0)
    # element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sign-in-button")))
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "loginbox-sbt")))
    element.submit()
    time.sleep(10)

    times -= 1

br.quit()
