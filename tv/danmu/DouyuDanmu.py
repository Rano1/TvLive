#coding:utf-8
#爬取斗鱼弹幕


import json
import re
import socket
import threading
import time
import urllib.request
import urllib.parse

import socks

from sql import MongoDBClient


class douYuTVDanmu(object):

    def __init__(self):
        proxyIp = "116.255.153.137"
        proxyPort = 8082
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxyIp, proxyPort)
        # socket.socket = socks.socksocket
        self.mongo_clent = MongoDBClient.MongoDBClient('douyu')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.codeLocalToServer = 689
        self.serverToLocal = 690
        self.gid = -9999
        self.rid = 16789
        self.server = {}

    def log(self,str):
        #str = str.encode()
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        log = now_time + '\t\t' + str
        with open('log.txt','a',encoding='utf-8')as f:
            f.writelines(log + '\n')
        print(log)
    def sendMsg(self,msg):
            msg = msg.encode('utf-8')
            data_length= len(msg)+8
            msgHead=int.to_bytes(data_length,4,'little')+int.to_bytes(data_length,4,'little')+int.to_bytes(self.codeLocalToServer,4,'little')
            self.sock.send(msgHead)
            self.sock.sendall(msg)

    def keeplive(self):
        while True:
            msg='type@=keeplive/tick@='+str(int(time.time()))+'/\x00'
            self.sendMsg(msg)
            #keeplive=sock.recv(1024)
            time.sleep(20)


    #分析网页中的信息
    def getInfo(self,url):
        self.log("请求网页内容...")
        try:
            with urllib.request.urlopen(url)as f:
                data = f.read().decode()
        except BaseException as e:
            self.log("请求网页内容失败..." + e)
            exit(404)
        self.log("获取房间信息...")
        room = re.search('var \$ROOM = (.*);',data)
        if room:
            room = room.group(1)
            room = json.loads(room)
            self.log("房间名:"+room["room_name"]+'\t\t|\t\t主播:'+room["owner_name"])
            self.rid = room["room_id"]

            if room["show_status"] == 2:
                self.log("未开播!\t\t"+str(self.rid))
                exit(1)
        # self.log("获取弹幕服务器信息...")
        # server_config = re.search('server_config":"(.*)","de',data)
        # if server_config:
        #     server_config = server_config.group(1)
        #     server_config = urllib.parse.unquote(server_config)
        #     server_config = json.loads(server_config)
        #     self.server = server_config



    def connectToDanMuServer(self):
        #index = random.randint(0,len(self.server)-1)     #选择一个服务器
        # HOST = self.server[index]['ip']
        # PORT = self.server[index]['port']
        HOST = 'openbarrage.douyutv.com'
        PORT = 8601

        self.log("连接弹幕服务器..."+HOST+':'+str(PORT))
        self.sock.connect((HOST, PORT))
        self.log("连接成功,发送登录请求...")

        #抓包:msg = 'type@=loginreq/username@=qq_NEUBLK/password@=1234567890123456/roomid@=335166/'
        msg = 'type@=loginreq/username@=/password@=/roomid@='+str(self.rid)+'/\x00'
        self.sendMsg(msg)
        data = self.sock.recv(1024)
        self.log('Received from login\t\t'+ repr(data))
        a = re.search(b'type@=(\w*)', data)
        if a.group(1)!=b'loginres':
            self.log("登录失败,程序退出...")
            exit(0)
        self.log("登录成功")

        #data = self.sock.recv(1024)   #type@=msgrepeaterlist  服务器列表
        #self.log('msgrepeaterlist\t\t'+ repr(data))
        # gid = re.search('gid@=(.*)\/',data)
        # # data = self.sock.recv(1024)
        # # self.log('Received', repr(data))
        # if gid:
        #     self.gid = gid.group(1)
        #     self.log("找到弹幕服务器"+str(self.gid))



        msg = 'type@=joingroup/rid@='+str(self.rid)+'/gid@=-9999/\x00'
        #print(msg)
        self.sendMsg(msg)
        self.log("进入弹幕服务器...")
        threading.Thread(target=douYuTVDanmu.keeplive,args=(self,)).start()
        self.log("心跳包机制启动...")
        data = self.sock.recv(1024)
        print('Received', repr(data))




    def danmuWhile(self):
        self.log("监听中")
        while True:
            data = self.sock.recv(1024)
            # self.log(repr(data))
            a = re.search(b'type@=(\w*)', data)
            if a:
                if a.group(1)==b'chatmsg':
                    danmu = re.search(b'nn@=(.*)/txt@=(.*?)/',data)
                    #self.log(danmu.group(1).decode()+'\t:\t'+danmu.group(2).decode())
                    try:
                        danmu_content = danmu.group(2).decode()
                        # self.log(danmu_content)
                        # self.log(danmu.group(1).decode() + ":" + danmu.group(2).decode())
                    except BaseException as e:

                        self.log("\t\t_________解析弹幕信息失败:"+str(data))
                elif a.group(1)==b'dgb':
                    # self.log(repr(data))
                    danmu_nickname = re.search(b'/nn@=(.*?)/', data)
                    danmu_gift = re.search(b'gfid@=(.*?)/', data)
                    try:
                        gitf_item = {}
                        gitf_item['type'] = 'dgb'
                        gitf_item['rid'] = re.search(b'/rid@=(.*?)/', data).group(1).decode()
                        gitf_item['gfid'] = int(re.search(b'/gfid@=(.*?)/', data).group(1).decode())
                        gitf_item['uid'] = re.search(b'/uid@=(.*?)/', data).group(1).decode()
                        gitf_item['nn'] = re.search(b'/nn@=(.*?)/', data).group(1).decode()
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


if __name__ == '__main__':
    # url = 'http://www.douyu.com/301712'
    # url = 'http://www.douyu.com/wt55kai'
    url = 'https://www.douyu.com/nvliu'
    danmu = douYuTVDanmu()
    danmu.getInfo(url)
    danmu.connectToDanMuServer()
    danmu.danmuWhile()