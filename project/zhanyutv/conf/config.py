# coding=utf-8

# HOST = "192.168.2.105"
HOST = "192.168.135.128"

DB_config = {
    # 'db_type': 'mongodb',
    'db_type': 'mysql',

    'mysql': {
        'host': HOST,
        'port': 3306,
        'user': 'root',
        'password': '1qaz*2WSX',
        'charset': 'utf8'
    },
    'redis': {
        'host': HOST,
        'port': 6379,
        'password': 'zxcvbnm',
        'db': 0,
    },
    'mongodb': {
        'host': HOST,
        'port': 27017,
        'username': '',
        'password': '',
    }
}

database = 'zhanyutv'

free_ipproxy_table = 'free_ipproxy'
httpbin_table = 'httpbin'

data_port = '8000'
