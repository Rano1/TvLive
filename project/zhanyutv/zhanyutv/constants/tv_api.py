# 设计相关的API

HOST_DOUYU = "http://open.douyucdn.cn/api/"
METHOD_DOUYU_ROOM_INFO = "RoomApi/room/"

# URL_DOUYU_ANCHOR_LIST_AJAX = "https://www.douyu.com/directory/all?isAjax=1&page="
URL_DOUYU_ANCHOR_LIST_AJAX = "https://www.douyu.com/directory/all?page="  # 主播在播列表

PLATFORM_DOUYU = 1 # 平台：斗鱼
PLATFORM_HUYA = 2 # 平台：虎牙

class ApiHelper():

    # 获取主播房间详情URL
    def get_douyu_roominfo_url(roomId):
        url = HOST_DOUYU + METHOD_DOUYU_ROOM_INFO + str(roomId)
        return url

    # 获取主播列表URL
    def get_douyu_list_url(page):
        url = URL_DOUYU_ANCHOR_LIST_AJAX + str(page)
        return url
