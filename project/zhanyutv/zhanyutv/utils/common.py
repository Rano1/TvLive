import hashlib


# 获取MD5(先判断传入的参数是否是utf8)
def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()
