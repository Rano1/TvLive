import requests
import re
from api import apiconstants
from db.mysqlclient import MysqlClient
from db.data.redis_data import RedisData
from zhanyutv.utils import common
from zhanyutv.items import GiftItem


# 爬取斗鱼基础礼物列表
class DouyuGiftCrawl(object):
    def __init__(self):
        self.mysql_conn = MysqlClient().getConn()
        self.platform = apiconstants.PLATFORM_DOUYU

    # 获取礼物数据
    def getGiftList(self):
        # 随便爬取一个可以爬到基础的礼物列表
        url = "https://www.douyu.com/catshow"
        html_data = requests.get(url)
        if html_data.content:
            content = html_data.content.decode()
            self.parse_data(content)
            # self.saveCateList(data['data'])
        else:
            print("请求错误")

    # 解析数据
    def parse_data(self, html_data):
        gift_list_json = re.search('\$ROOM\.propBatterConfig\s=\s({.*});', html_data).group(1)
        gift_json_format = common.valid_json(gift_list_json)
        if gift_json_format != False:
            print(gift_json_format)
            gift_list = []
            for gfid in gift_json_format:
                gift_item = GiftItem()
                gift_item['gfid'] = int(gfid)
                gift_item['name'] = gift_json_format[gfid]['name']
                gift_item['type'] = int(gift_json_format[gfid]['type'])
                gift_item['desc'] = ""
                gift_item['price'] = gift_json_format[gfid]['pc'] / 100 # 注意，这里斗鱼* 100
                gift_item['platform'] = apiconstants.PLATFORM_DOUYU
                gift_item['small_icon'] = gift_json_format[gfid]['himg']
                gift_item['animation_icon'] = gift_json_format[gfid]['himg']
                gift_list.append(gift_item)
            if gift_list and len(gift_list) > 0:
                self.save_gift_list(gift_list)

    # 保存礼物数据
    def save_gift_list(self, list):
        cursor = self.mysql_conn.cursor()
        for gift in list:
            # 存入Redis
            RedisData.add_gift_info(None, self.platform, gift)
            # 存入Mysql
            exist_sql = "select * from gift where platform=%s and gfid=%s" % (self.platform, gift['gfid'])
            try:
                cursor.execute(exist_sql)
                if cursor.fetchone() == None:
                    print("不存在分类数据，入库")
                    # 执行具体的插入
                    insert_sql = """
                                                insert into gift(gfid,name,type,`desc`,price,platform,small_icon,animation_icon)
                                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                                """
                    cursor.execute(insert_sql, (
                        gift['gfid'], gift['name'], gift['type'], gift['desc'],
                        gift['price'], self.platform, gift['small_icon'], gift['animation_icon']))
                    self.mysql_conn.commit()
                else:
                    print("存在分类数据")
            except Exception as e:
                print("出错了 :" + str(e.args))
                self.mysql_conn.rollback()

        cursor.close()


if __name__ == '__main__':
    douyu_gift_crawl = DouyuGiftCrawl()
    douyu_gift_crawl.getGiftList()
