# 模拟一直播登录
import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time

url = "https://www.douyu.com/member/login"


class DouYuAdminLogin():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        # self.driver.set_window_size(1000, 800)
        # self.driver.set_window_position(22, 33)
        # self.driver = webdriver.PhantomJS(
        #     executable_path='C: UsersGentlyguitarDesktopphantomjs - 1.9.7 - windowsphantomjs.exe')

    def login(self, username, password):
        self.driver.get(url)
        elem_username = self.driver.find_element_by_name('username')
        elem_username.send_keys(username)
        elem_password = self.driver.find_element_by_name('password')
        elem_password.send_keys(password)
        # # 元素拖拽
        # action_chains = ActionChains(self.driver)
        # # elem_code = self.driver.find_element_by_name('geetest_validate')
        # elem_code = self.driver.find_element_by_class_name('gt_slider_knob')
        # location = elem_code.location
        # size = elem_code.size
        # moveX = 99  # 移动位置
        # action_chains.click_and_hold(elem_code)
        # time.sleep(5)
        # action_chains.drag_and_drop_by_offset(elem_code, moveX, 0).perform()
        # # action_chains.move_to_element_with_offset(elem_code, moveX, 0).perform()
        # elem_login = self.driver.find_element_by_class_name("loginbox-sbt btn-sub")
        # elem_login.submit()


        try:
            somedom = WebDriverWait(self.driver, 30)
            html = somedom.find_element_by_xpath("//div[@class='o-login fl']")
            print(html)
        finally:
            print("finally")
            pass
        self.driver.quit()
        # driver.quit()


if __name__ == '__main__':
    mYiAdminLogin = DouYuAdminLogin()
    username = "战鱼德州圈丶周周Chris"
    password = "cris218314zhou"
    mYiAdminLogin.login(username, password)
