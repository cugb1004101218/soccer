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
from db_api import news_db_api, image_db_api, lottery_db_api
from cache import news_cache
import base_server

from tornado.options import define, options
define("port", default=40000, help="run on the given port", type=int)
define("ip", default="0.0.0.0", help="server_ip", type=str)

class LotteryHandler(base_server.BaseHandler):
    def parse(self):
        self.lottery_type = self.get_argument('lottery_type')
        self.compname = self.get_argument('compname')
        self.season = self.get_argument('season')
        self.host_team = self.get_argument('host_team')
        self.guest_team = self.get_argument('guest_team')
        self.rd = int(self.get_argument('rd'))

    def get_data_from_db(self):
        ret = lottery_db_api.get_lottery_list(self.lottery_type,
                                              self.compname,
                                              self.season,
                                              self.rd,
                                              self.host_team,
                                              self.guest_team)
        lottery_list = []
        for lottery in ret:
            lottery_list.append(lottery)
        return lottery_list

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/lottery", LotteryHandler)])
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port, address=options.ip)
    tornado.ioloop.IOLoop.instance().start()
