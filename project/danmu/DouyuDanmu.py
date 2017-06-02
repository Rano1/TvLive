# coding:utf-8
# 爬取斗鱼弹幕


import json
import re
import socket
import threading
from time import sleep, ctime
import time
import urllib.request
import urllib.parse
import socks
from project.danmu.db.RedisClient import RedisClient

from sql import MongoDBClient


class douYuTVDanmu(object):
    def __init__(self, roomId):
        proxyIp = "115.213.202.171"
        proxyPort = 808
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxyIp, proxyPort)
        socket.socket = socks.socksocket
        self.mongo_clent = MongoDBClient.MongoDBClient('douyu')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.codeLocalToServer = 689
        self.serverToLocal = 690
        self.gid = -9999
        self.roomId = roomId
        self.server = {}
        self.log("初始化 :" + str(self.roomId))

    def log(self, str):
        # str = str.encode()
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        log = now_time + '\t\t' + str
        with open('log.txt', 'a', encoding='utf-8')as f:
            f.writelines(log + '\n')
        print(log)

    def sendMsg(self, msg):
        msg = msg.encode('utf-8')
        data_length = len(msg) + 8
        msgHead = int.to_bytes(data_length, 4, 'little') + int.to_bytes(data_length, 4, 'little') + int.to_bytes(
            self.codeLocalToServer, 4, 'little')
        self.sock.send(msgHead)
        self.sock.sendall(msg)

    def keeplive(self):
        while True:
            msg = 'type@=keeplive/tick@=' + str(int(time.time())) + '/\x00'
            self.sendMsg(msg)
            # keeplive=sock.recv(1024)
            time.sleep(20)

    def connectToDanMuServer(self):
        # index = random.randint(0,len(self.server)-1)     #选择一个服务器
        # HOST = self.server[index]['ip']
        # PORT = self.server[index]['port']
        HOST = 'openbarrage.douyutv.com'
        PORT = 8601

        self.log("连接弹幕服务器..." + HOST + ':' + str(PORT))
        self.sock.connect((HOST, PORT))
        self.log("连接成功,发送登录请求...")

        # 抓包:msg = 'type@=loginreq/username@=qq_NEUBLK/password@=1234567890123456/roomid@=335166/'
        msg = 'type@=loginreq/username@=/password@=/roomid@=' + str(self.roomId) + '/\x00'
        self.sendMsg(msg)
        data = self.sock.recv(1024)
        self.log('Received from login\t\t' + repr(data))
        a = re.search(b'type@=(\w*)', data)
        if a.group(1) != b'loginres':
            self.log("登录失败,程序退出...")
            exit(0)
        self.log("登录成功")

        msg = 'type@=joingroup/rid@=' + str(self.roomId) + '/gid@=-9999/\x00'
        # print(msg)
        self.sendMsg(msg)
        self.log("进入弹幕服务器...")
        threading.Thread(target=douYuTVDanmu.keeplive, args=(self,)).start()
        self.log("心跳包机制启动...")
        data = self.sock.recv(1024)
        print('Received', repr(data))

    def danmuWhile(self):
        self.log("监听中 :" + str(self.roomId))
        while True:
            data = self.sock.recv(1024)
            # self.log(repr(data))
            a = re.search(b'type@=(\w*)', data)
            if a:
                if a.group(1) == b'chatmsg':
                    danmu = re.search(b'nn@=(.*)/txt@=(.*?)/', data)
                    # self.log(danmu.group(1).decode()+'\t:\t'+danmu.group(2).decode())
                    try:
                        danmu_content = danmu.group(2).decode()
                        # self.log(danmu_content)
                        # self.log(danmu.group(1).decode() + ":" + danmu.group(2).decode())
                    except BaseException as e:

                        self.log("\t\t_________解析弹幕信息失败:" + str(data))
                elif a.group(1) == b'dgb':
                    # self.log(repr(data))
                    try:
                        gitf_item = {}
                        gitf_item['type'] = 'dgb'
                        gitf_item['rid'] = re.search(b'/rid@=(.*?)/', data).group(1).decode()
                        gitf_item['gfid'] = int(re.search(b'/gfid@=(.*?)/', data).group(1).decode())
                        gitf_item['uid'] = re.search(b'/uid@=(.*?)/', data).group(1).decode()
                        gitf_item['nickname'] = re.search(b'/nn@=(.*?)/', data).group(1).decode()
                        gitf_item['level'] = int(re.search(b'/level@=(.*?)/', data).group(1).decode())
                        gfcnt = re.search(b'/gfcnt@=(.*?)/', data)
                        hits = re.search(b'/hits@=(.*?)/', data)
                        gitf_item['gfcnt'] = 0
                        gitf_item['hits'] = 0
                        gitf_item['time'] = int(time.time() * 1000)
                        if gfcnt:
                            gitf_item['gfcnt'] = int(gfcnt.group(1).decode())
                        if hits:
                            gitf_item['hits'] = int(hits.group(1).decode())
                        print(gitf_item)
                        self.mongo_clent.save_data(gitf_item)
                        # self.log(danmu_nickname.group(1).decode() + " 增送了：" + danmu_gift.group(1).decode())
                    except BaseException as e:
                        self.log("\t\t_________解析礼物信息失败:" + str(data))



class DouYuTVDanmuThread(threading.Thread):
    def __init__(self, room_id):
        threading.Thread.__init__(self)
        proxyIp = "116.255.153.137"
        proxyPort = 8082
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxyIp, proxyPort)
        # socket.socket = socks.socksocket
        self.mongo_clent = MongoDBClient.MongoDBClient('douyu')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.codeLocalToServer = 689
        self.serverToLocal = 690
        self.gid = -9999
        self.roomId = room_id
        self.server = {}
        self.log("初始化 :" + str(self.roomId))

    def run(self):
        self.connectToDanMuServer()
        self.danmuWhile()

    def log(self, str):
        # str = str.encode()
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        log = now_time + '\t\t' + str
        with open('log.txt', 'a', encoding='utf-8')as f:
            f.writelines(log + '\n')
        print(log)

    def sendMsg(self, msg):
        msg = msg.encode('utf-8')
        data_length = len(msg) + 8
        msgHead = int.to_bytes(data_length, 4, 'little') + int.to_bytes(data_length, 4, 'little') + int.to_bytes(
            self.codeLocalToServer, 4, 'little')
        self.sock.send(msgHead)
        self.sock.sendall(msg)

    def keeplive(self):
        while True:
            msg = 'type@=keeplive/tick@=' + str(int(time.time())) + '/\x00'
            self.sendMsg(msg)
            # keeplive=sock.recv(1024)
            time.sleep(20)

    def connectToDanMuServer(self):
        # index = random.randint(0,len(self.server)-1)     #选择一个服务器
        # HOST = self.server[index]['ip']
        # PORT = self.server[index]['port']
        HOST = 'openbarrage.douyutv.com'
        PORT = 8601

        self.log("连接弹幕服务器..." + HOST + ':' + str(PORT))
        self.sock.connect((HOST, PORT))
        self.log("连接成功,发送登录请求...")

        # 抓包:msg = 'type@=loginreq/username@=qq_NEUBLK/password@=1234567890123456/roomid@=335166/'
        msg = 'type@=loginreq/username@=/password@=/roomid@=' + str(self.roomId) + '/\x00'
        self.sendMsg(msg)
        data = self.sock.recv(1024)
        self.log('Received from login\t\t' + repr(data))
        a = re.search(b'type@=(\w*)', data)
        if a.group(1) != b'loginres':
            self.log("登录失败,程序退出...")
            exit(0)
        self.log("登录成功")

        msg = 'type@=joingroup/rid@=' + str(self.roomId) + '/gid@=-9999/\x00'
        # print(msg)
        self.sendMsg(msg)
        self.log("进入弹幕服务器...")
        threading.Thread(target=douYuTVDanmu.keeplive, args=(self,)).start()
        self.log("心跳包机制启动...")
        data = self.sock.recv(1024)
        print('Received', repr(data))

    def danmuWhile(self):
        self.log("监听中 :" + str(self.roomId))
        while True:
            data = self.sock.recv(1024)
            # self.log(repr(data))
            a = re.search(b'type@=(\w*)', data)
            if a:
                if a.group(1) == b'chatmsg':
                    danmu = re.search(b'nn@=(.*)/txt@=(.*?)/', data)
                    # self.log(danmu.group(1).decode()+'\t:\t'+danmu.group(2).decode())
                    try:
                        danmu_content = danmu.group(2).decode()
                        # self.log(danmu_content)
                        # self.log(danmu.group(1).decode() + ":" + danmu.group(2).decode())
                    except BaseException as e:

                        self.log("\t\t_________解析弹幕信息失败:" + str(data))
                elif a.group(1) == b'dgb':
                    # self.log(repr(data))
                    try:
                        gitf_item = {}
                        gitf_item['type'] = 'dgb'
                        gitf_item['rid'] = re.search(b'/rid@=(.*?)/', data).group(1).decode()
                        gitf_item['gfid'] = int(re.search(b'/gfid@=(.*?)/', data).group(1).decode())
                        gitf_item['uid'] = re.search(b'/uid@=(.*?)/', data).group(1).decode()
                        gitf_item['nickname'] = re.search(b'/nn@=(.*?)/', data).group(1).decode()
                        gitf_item['level'] = int(re.search(b'/level@=(.*?)/', data).group(1).decode())
                        gfcnt = re.search(b'/gfcnt@=(.*?)/', data)
                        hits = re.search(b'/hits@=(.*?)/', data)
                        gitf_item['gfcnt'] = 0
                        gitf_item['hits'] = 0
                        gitf_item['time'] = int(time.time() * 1000)
                        if gfcnt:
                            gitf_item['gfcnt'] = int(gfcnt.group(1).decode())
                        if hits:
                            gitf_item['hits'] = int(hits.group(1).decode())
                        print(gitf_item)
                        self.mongo_clent.save_data(gitf_item)
                        # self.log(danmu_nickname.group(1).decode() + " 增送了：" + danmu_gift.group(1).decode())
                    except BaseException as e:
                        self.log("\t\t_________解析礼物信息失败:" + str(data))





def loop(room_id):
    print("start thread : " + str(room_id))
    sleep(1)


if __name__ == '__main__':
    key_anthor_id_list = 'anchor_id_list:' + str(1)
    redis_client = RedisClient().getInstance()
    # while True:
    anthor_id_list = redis_client.srandmember(key_anthor_id_list, 200)  # 随机获取值
    # anthor_id_list = redis_client.zrange(key_anthor_id_list, 1, 10)  # 随机获取值
    # anthor_id_list = [78561, 142823, 16101, 2127419, 84452, 176341, 1557505, 507882, 432071, 545318, 74706, 208114, 74751, 2018597, 782454, 522423, 84074, 1859312, 699689, 782546, 1275878, 3484, 48699, 1811143, 2102398, 13703, 533813, 414818, 787579, 506510, 93912, 1746151, 1047629, 2110203, 61372, 526408, 288016, 782360, 553918, 17349, 442836, 221869, 2141673, 83379, 103361, 921393, 1647060, 641986, 15177, 1863767, 517915, 93589, 1017358, 227670, 891464, 1803963, 759099, 22082, 432033, 1378146, 69752, 320155, 298982, 2055655, 676218, 981741, 710676, 1954481, 1386455, 2169946, 297535, 318624, 1568, 70898, 1037792, 570089, 549287, 444141, 1235350, 280072, 68172, 110441, 1345550, 1976204, 223592, 1634149, 1768633, 3258, 54738, 478203, 645, 1278831, 285896, 890434, 2115718, 329364, 511452, 60937, 671435, 39300, 1785701, 702151, 780824, 702130, 2044310, 255287, 111716, 44198, 525207, 424998, 1122858, 1109676, 1048142, 2072785, 855539, 315173, 41829, 331074, 1700133, 701579]
    # anthor_id_list = [532683, 1048142, 656574, 67925, 1109676, 816736, 500228, 97376, 697342, 649820, 1232275, 64593, 703484, 625764, 688512, 600401, 475879, 6906, 16487, 1950493, 1016580, 1978453, 222015, 2083207, 607887, 248753, 172992, 564687, 1688063, 539439, 755909, 1891873, 24418, 1929072, 1216369, 775197, 1409119, 713484, 2163767, 214514, 48748, 539088, 289992, 2200942, 74763, 2039064, 1986192, 1439052, 691833, 1925319, 93936, 605964, 584920, 861644, 107345, 1947656, 210398, 613077, 1658899, 70994, 1993389, 944146, 335835, 6540, 1909342, 521207, 469731, 468241, 252802, 587997, 97739, 218859, 1126960, 145201, 453567, 828709, 1782781, 67205, 1940017, 2039116, 2132902, 1799432, 816988, 236686, 660090, 651133, 119790, 466788, 1295916, 1409834, 2162136, 625099, 434213, 162752, 1063732, 1942818, 83172, 1069894, 856876, 68190, 504343, 1696183, 122024, 713337, 1400514, 1161765, 2143492, 828705, 2051433, 599053, 2202005, 1930365, 455513, 2069811, 2199347, 2126454, 1412437, 122402, 660219, 481827]
    # anthor_id_list = [330435, 644021, 962, 711902, 1964215, 149115, 533955, 290114, 790009, 1893627, 2184103, 549306, 1754684, 3928, 1527318, 964817, 1495967, 96577, 67761, 497976, 65962, 734565, 2120674, 218522, 67734, 987697, 632386, 1824331, 1021624, 881983, 796228, 2132850, 1377759, 1379340, 509279, 1443526, 416499, 744837, 210330, 1944212, 1867637, 2200204, 546621, 1007912, 231464, 1935001, 445469, 624489, 633421, 2117607, 540910, 1338316, 46966, 36337, 1855598, 1937174, 101217, 2161949, 444146, 233535, 460066, 708024, 1708799, 228947, 831528, 568462, 1272002, 2070962, 1746306, 747517, 473910, 175843, 893046, 1555999, 1369971, 79101, 1984718, 296948, 702986, 195358, 1743915, 527, 196775, 2160371, 323714, 1738104, 870188, 464086, 571881, 276506, 1202054, 1667374, 969506, 503866, 224924, 244119, 2196230, 336538, 1743023, 318731, 35954, 284986, 236866, 916601, 1725439, 2115227, 325742, 213114, 1981414, 2065660, 323470, 237472, 31880, 1565199, 172392, 284550, 1931566, 525816, 1882986, 654370]
    anthor_id_list = [330435]

    print(anthor_id_list)
    threads = []
    # anthor_id_list = [1312662, 585704]
    print(anthor_id_list)
    for roomId in anthor_id_list:
        thread = DouYuTVDanmuThread(roomId)
        thread.name = roomId
        threads.append(thread)

    # for roomId in anthor_id_list:
    #     thread = threading.Thread(target=loop, args=(roomId,))
    #     thread.name = roomId
    #     threads.append(thread)
        # redis_client.srem(key_anthor_id_list, int(roomId))
        # danmu = douYuTVDanmu(roomId)
        # danmu.connectToDanMuServer()
        # danmu.danmuWhile()

    i = 0
    for thread in threads:
        i = i + 1
        print("i :" + str(i))
        sleep(0.5)
        thread.start()
