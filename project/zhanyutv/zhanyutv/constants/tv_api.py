# 设计相关的API

HOST_DOUYU = "http://open.douyucdn.cn/api/"
METHOD_DOUYU_ROOM_INFO = "RoomApi/room/"

PLATFORM_DOUYU = 1 # 平台：斗鱼
PLATFORM_HUYA = 2 # 平台：虎牙

class ApiHelper():

    # 获取主播房间详情URL
    def get_douyu_roominfo_url(roomId):
        url = HOST_DOUYU + METHOD_DOUYU_ROOM_INFO + str(roomId)
        return url
