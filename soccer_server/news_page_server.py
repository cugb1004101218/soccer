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

from tornado.options import define, options
define("port", default=30000, help="run on the given port", type=int)
define("ip", default="0.0.0.0", help="server_ip", type=str)

class NewsPageHandler(tornado.web.RequestHandler):
    def get(self):
        src = self.get_argument('src')
        news = news_db_api.process_news(news_db_api.get_news(src))
        if news:
            self.render("news.html", news=news)
        else:
            self.write("404")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/news_page", NewsPageHandler)])
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port, address=options.ip)
    tornado.ioloop.IOLoop.instance().start()
