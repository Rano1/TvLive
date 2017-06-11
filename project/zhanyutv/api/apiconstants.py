# 设计相关的API

import urllib

PLATFORM_DOUYU = 1  # 平台：斗鱼
PLATFORM_HUYA = 2  # 平台：虎牙
PLATFORM_PANDA = 3  # 平台：熊猫

URL_API_DOUYU_ROOM_INFO = "http://open.douyucdn.cn/api/RoomApi/room/" # 主播房间信息
URL_API_DOUYU_ROOM_LIST = "http://api.douyutv.com/api/v1/live"  # 在播主播列表

# URL_DOUYU_ANCHOR_LIST_AJAX = "https://www.douyu.com/directory/all?isAjax=1&page="
URL_DOUYU_ANCHOR_LIST_AJAX = "https://www.douyu.com/directory/all?page="  # 主播在播列表


# 获取主播房间详情URL
def get_douyu_roominfo_url(roomId):
    url = URL_API_DOUYU_ROOM_INFO + str(roomId)
    return url

def get_api_douyu_list_url(offset):
    limit = 100
    payload = {'offset': offset, 'limit': limit}
    url = URL_API_DOUYU_ROOM_LIST + "?" + urllib.parse.urlencode(payload)
    print(url)
    return url

# 获取主播列表URL
def get_douyu_list_url(page):
    url = URL_DOUYU_ANCHOR_LIST_AJAX + str(page)
    return url