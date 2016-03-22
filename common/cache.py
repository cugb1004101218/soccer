# -*- coding: utf-8 -*-
import sys
import time
import unittest
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('../config/soccer.config')
from redis_api import redis_cache
news_list_cache_ttl = config.getint("redis", "news_list_cache_ttl")
match_cache_ttl = config.getint("redis", "match_cache_ttl")
lottery_cache_ttl = config.getint("redis", "lottery_cache_ttl")

class Cache(object):
    def __init__(self, cache):
        self.cache = cache

    def gen_real_key(self, args):
        return "##".join(args)

    def set_cache(self, args, value, ttl=None):
        real_key = self.gen_real_key(args)
        return self.cache.set(real_key, value, ttl)

    def get_cache(self, args):
        real_key = self.gen_real_key(args)
        return self.cache.get(real_key)

class NewsCache(Cache):
    def __init__(self, cache):
        super(NewsCache, self).__init__(cache)

    def set_news_list_cache(self, compname, page, page_count, value):
        args = ["news", str(compname), str(page), str(page_count)]
        return self.set_cache(args, value, news_list_cache_ttl)

    def get_news_list_cache(self, compname, page,  page_count):
        args = ["news", str(compname), str(page), str(page_count)]
        return self.get_cache(args)

class MatchCache(Cache):
    def __init__(self, cache):
        super(MatchCache, self).__init__(cache)

    def set_match_list_cache(self, compname, value):
        args = ["match", compname]
        return self.set_cache(args, value, match_cache_ttl)

    def get_match_list_cache(self, compname):
        args = ["match", compname]
        return self.get_cache(args)

    def set_jifen_list_cache(self, compname, value):
        args = ["jifen", compname]
        return self.set_cache(args, value, match_cache_ttl)

    def get_jifen_list_cache(self, compname):
        args = ["jifen", compname]
        return self.get_cache(args)

    def set_shooter_list_cache(self, compname, value):
        args = ["shooter", compname]
        return self.set_cache(args, value, match_cache_ttl)

    def get_shooter_list_cache(self, compname):
        args = ["shooter", compname]
        return self.get_cache(args)

news_cache = NewsCache(redis_cache)
match_cache = MatchCache(redis_cache)
common_cache = Cache(redis_cache)
