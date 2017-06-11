import requests
from api import apiconstants
from db.mysqlclient import MysqlClient
from db.data.redis_data import RedisData

class DouyuCateCrawl(object):
    def __init__(self):
        self.mysql_conn = MysqlClient().getConn()
        self.platform = apiconstants.PLATFORM_DOUYU

    def getCateList(self):
        url = 'http://open.douyucdn.cn/api/RoomApi/game'
        print(url)
        data = requests.get(url).json()
        if data.get('error') == 0:
            print(data)
            self.saveCateList(data['data'])
        else:
            print("请求错误")

    def saveCateList(self, list):
        cursor = self.mysql_conn.cursor()
        for item in list:
            cate = dict()
            cate['cate_id'] = item['cate_id']
            cate['cate_name'] = item['game_name']
            cate['cate_short_name'] = item['short_name']
            cate['cate_url'] = item['game_url']
            cate['cate_src'] = item['game_src']
            cate['cate_icon'] = item['game_icon']
            # 存入Redis
            RedisData.add_cate_info(self.platform, cate)
            # 存入Mysql
            exist_sql = "select * from cate where platform=%s and cate_id=%s" % (self.platform, cate['cate_id'])
            try:
                cursor.execute(exist_sql)
                if cursor.fetchone() == None:
                    print("不存在分类数据，入库")
                    # 执行具体的插入
                    insert_sql = """
                                                insert into cate(cate_id,cate_name,cate_short_name,cate_url,cate_src,cate_icon,platform)
                                                VALUES (%s,%s,%s,%s,%s,%s,%s)
                                """
                    cursor.execute(insert_sql, (
                        cate['cate_id'], cate['cate_name'], cate['cate_short_name'], cate['cate_url'], cate['cate_src'],
                        cate['cate_icon'], str(self.platform)))
                    self.mysql_conn.commit()
                else:
                    print("存在分类数据")
            except:
                self.mysql_conn.rollback()


        cursor.close()



if __name__ == '__main__':
    douyu_cate_crawl = DouyuCateCrawl()
    douyu_cate_crawl.getCateList()
