# 斗鱼人气
import requests

url = "https://www.douyu.com/2206496"
result = requests.get(url=url)  # 最基本的GET请求
print(result.status_code)    # 获取返回状态
