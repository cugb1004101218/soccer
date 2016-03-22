# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.httpserver
import tornado.web
import tornado.options
import pymongo
import json
import sys
sys.path.append('../common/')
from db_api import news_db_api, image_db_api
from cache import news_cache
import base_server

from tornado.options import define, options
define("port", default=20000, help="run on the given port", type=int)
define("ip", default="0.0.0.0", help="server_ip", type=str)
class NewsHandler(base_server.BaseHandler):
    def parse(self):
        self.page = int(self.get_argument('page'))
        self.compname = self.get_argument('compname')
        self.page_count = int(self.get_argument('page_count'))

    def get_data_from_db(self):
        ret = news_db_api.get_news_list(self.compname, self.page, self.page_count*3)
        items = []
        for item in ret:
            if len(items) >= self.page_count:
                break
            item = news_db_api.process_news(item)
            # 过滤
            if len(item["small_images"]) == 0 or item["rewritten_title"] == "":
                continue
            items.append(item)
        return items

    def get_data_from_cache(self):
        return news_cache.get_news_list_cache(self.compname, self.page, self.page_count)

    def set_cache(self, value):
        return news_cache.set_news_list_cache(self.compname, self.page, self.page_count, value)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/news", NewsHandler)])
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port, address=options.ip)
    tornado.ioloop.IOLoop.instance().start()
