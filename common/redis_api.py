# -*- coding: utf-8 -*-
import redis
import sys
import time
import unittest
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('../config/soccer.config')
redis_ip = config.get("redis", "redis_ip")
redis_port = config.getint("redis", "redis_port")
redis_db = config.getint("redis", "redis_db")
news_list_cache_ttl = config.getint("redis", "news_list_cache_ttl")

class RedisAPI(object):
    def __init__(self, redis_ip, redis_port, redis_db):
        self.conn = redis.Redis(host=redis_ip, port=redis_port, db=redis_db)

    def set(self, k, v, ttl=None):
        ret = self.conn.set(k, v)
        if ttl:
            ret &= self.conn.expire(k, ttl)
        return ret

    def get(self, k):
        return self.conn.get(k)

    def delete(self, k):
        return self.conn.delete(k)

class RedisAPITest(unittest.TestCase):
    def setUp(self):
        self.redis_api = RedisAPI(redis_ip,
                                  redis_port,
                                  redis_db)

    def testset(self):
        redis_api = self.redis_api
        key = "key"
        value = "value"
        self.assertTrue(redis_api.set(key, value))
        self.assertEqual(redis_api.get(key), value)
        ttl = 3
        self.assertTrue(redis_api.set(key, value, ttl))
        self.assertEqual(redis_api.get(key), value)
        time.sleep(5)
        self.assertEqual(redis_api.get(key), None)

redis_cache = RedisAPI(redis_ip,
                       redis_port,
                       redis_db)

if __name__ == '__main__':
    unittest.main()
