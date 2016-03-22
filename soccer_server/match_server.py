# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.httpserver
import tornado.web
import tornado.options
import pymongo
import json
import sys
sys.path.append('../common/')
from db_api import match_db_api, jifen_db_api, shooter_db_api
from tornado.options import define, options
import base_server
from cache import match_cache
define("port", default=21000, help="run on the given port", type=int)
define("ip", default="0.0.0.0", help="server_ip", type=str)

class MatchHandler(base_server.BaseHandler):
    def parse(self):
        self.compname = self.get_argument('compname')

    def get_data_from_db(self):
        now_comp_info = match_db_api.get_now_comp_info(self.compname)
        season = now_comp_info["season"]
        match_list = match_db_api.get_match_list(self.compname, season)
        matches = match_db_api.process_match_list(match_list)
        ret = {}
        ret["comp_info"] = now_comp_info
        ret["match_list"] = matches
        return ret

    def get_data_from_cache(self):
        return match_cache.get_match_list_cache(self.compname)

    def set_cache(self, value):
        match_cache.set_match_list_cache(self.compname, value)


class JifenHandler(base_server.BaseHandler):
    def parse(self):
        self.compname = self.get_argument('compname')

    def get_data_from_db(self):
        now_comp_info = match_db_api.get_now_comp_info(self.compname)
        season = now_comp_info["season"]
        jifen_list = jifen_db_api.get_team_jifen_list(self.compname, season)
        jifens = []
        for jifen in jifen_list:
            jifens.append(jifen)
        ret = {}
        ret["comp_info"] = now_comp_info
        ret["jifen_list"] = jifens
        return ret

    def get_data_from_cache(self):
        return match_cache.get_jifen_list_cache(self.compname)

    def set_cache(self, value):
        match_cache.set_jifen_list_cache(self.compname, value)

class ShooterHandler(base_server.BaseHandler):
    def parse(self):
        self.compname = self.get_argument('compname')

    def get_data_from_db(self):
        now_comp_info = match_db_api.get_now_comp_info(self.compname)
        season = now_comp_info["season"]
        shooter_list = shooter_db_api.get_shooter_list(self.compname, season)
        shooters = []
        for shooter in shooter_list:
            shooters.append(shooter)
        ret = {}
        ret["shooter_list"] = shooters
        ret["comp_info"] = now_comp_info
        return ret

    def get_data_from_cache(self):
        return match_cache.get_shooter_list_cache(self.compname)

    def set_cache(self, value):
        match_cache.set_shooter_list_cache(self.compname, value)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/match", MatchHandler), (r"/jifen", JifenHandler), (r"/shooter", ShooterHandler)])
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port, address=options.ip)
    tornado.ioloop.IOLoop.instance().start()
