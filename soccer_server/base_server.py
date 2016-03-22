# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.httpserver
import tornado.web
import tornado.options
import pymongo
import json
import sys
sys.path.append('../common/')
sys.path.append('../config/')
from db_api import news_db_api, image_db_api
from cache import news_cache

class BaseHandler(tornado.web.RequestHandler):
    # 解析 url 的参数
    def parse(self):
        pass

    def get_data_from_db(self):
        return None

    def get_data_from_cache(self):
        return None

    def set_cache(self, value):
        return True

    def get(self):
        self.parse()
        # 先从 cache 中取
        ret = self.get_data_from_cache()
        if not ret:
            ret = json.dumps(self.get_data_from_db(), ensure_ascii=False)
            # 写回cache
            self.set_cache(ret)
        self.write(ret)

application = tornado.web.Application([
    (r"/news", BaseHandler),
])

if __name__ == "__main__":
    #application.listen(20000)
    #tornado.ioloop.IOLoop.instance().start()

    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/news", BaseHandler)])
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port, address=options.ip)
    tornado.ioloop.IOLoop.instance().start()
