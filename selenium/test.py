from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = "http://www.python.org"
browser = webdriver.Chrome()
# browser = webdriver.Ie()
browser.get(url)
assert "Python" in browser.title
elem = browser.find_element_by_name("q")
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
print(browser.page_source)