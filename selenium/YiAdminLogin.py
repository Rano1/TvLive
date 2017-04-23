# 模拟一直播登录
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = "http://family.yizhibo.com/account/login/init"


class YiAdminLogin():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self, username, password):
        driver = self.driver
        driver.get(url)
        elem_username = driver.find_element_by_name('username')
        elem_username.send_keys(username)
        elem_password = driver.find_element_by_name('pwd')
        elem_password.send_keys(password)
        elem_code = driver.find_element_by_name('code')
        elem_login = driver.find_element_by_id("submit")
        # elem_login.click()
        elem_login.submit()

if __name__ == '__main__':
    mYiAdminLogin = YiAdminLogin()
    username = "test"
    password = "test1234"
    mYiAdminLogin.login(username, password)
