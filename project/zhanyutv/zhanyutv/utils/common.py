import hashlib
import re
import json


# 获取MD5(先判断传入的参数是否是utf8)
def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


# 从字符串中提取出数字
def extract_num(text):
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums

# 验证是否为 json 数据格式
def valid_json(my_json):
    """ 验证是否为 json 数据格式"""
    try:
        json_object = json.loads(my_json)
    except ValueError as e:
        print(e)
        return False
    return json_object

