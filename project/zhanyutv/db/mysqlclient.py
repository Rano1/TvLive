# Redis工具
import config
import MySQLdb
import MySQLdb.cursors

__all__ = ['MysqlClient']


class MysqlClient(object):
    def __init__(self):
        # host = config.DB_config.get('mysql').get('host')
        # port = config.DB_config.get('mysql').get('port')
        # user = config.DB_config.get('mysql').get('user')
        # password = config.DB_config.get('mysql').get('password')
        # db = config.DB_config.get('database')
        # self.mysql_conn = MySQLdb.connect(host, user, password, db, charset="utf8", use_unicode=True)
        dbparms = config.DB_config.get("mysql")
        dbparms['db'] = config.database
        dbparms['cursorclass'] = MySQLdb.cursors.DictCursor
        dbparms['use_unicode'] = True
        self.mysql_conn = MySQLdb.connect(**dbparms)

    def getConn(self):
        return self.mysql_conn
