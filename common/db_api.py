# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import sys
import unittest
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('/home/cugbacm/zhuzekun/soccer/config/soccer.config')
db_engine = config.get("db", "db_engine")
db_ip = config.get("db", "db_ip")
db_port = config.getint("db", "db_port")
db_name = config.get("db", "db_name")
news_table_name = config.get("db", "news_table_name")
processed_news_table_name = config.get("db", "processed_news_table_name")
image_table_name = config.get("db", "image_table_name")
match_table_name = config.get("db", "match_table_name")
jifen_table_name = config.get("db", "jifen_table_name")
shooter_table_name = config.get("db", "shooter_table_name")
lottery_table_name = config.get("db", "lottery_table_name")
image_server = config.get("server", "image_server")
news_page_server = config.get("server", "news_page_server")
team_logo_width = config.get("image", "team_logo_width")
team_logo_height = config.get("image", "team_logo_height")

class DBAPI(object):
    def __init__(self, db_engine, db_ip, db_port, db_name, table_name):
        self.db_engine = db_engine
        self.db_ip = db_ip
        self.db_port = db_port
        self.db_name = db_name
        self.table_name = table_name
        if self.db_engine == "mongo":
            self.conn = pymongo.MongoClient(host=self.db_ip, port=self.db_port)
            self.db = self.conn[self.db_name]
            self.table = self.db[self.table_name]

    def get_one(self, query):
        return self.table.find_one(query, projection={"_id": False})

    def get_all(self, query):
        return self.table.find(query)

    def add(self, kv_dict):
        return self.table.insert(kv_dict)

    def delete(self, query):
        return self.table.delete_many(query)

    def check_exist(self, query):
        ret = self.get(query)
        return len(ret) > 0

    # 如果没有 会新建
    def update(self, query, kv_dict):
        ret = self.table.update_many(
            query,
            {
                "$set": kv_dict,
            }
        )
        if not ret.matched_count or ret.matched_count == 0:
            self.add(kv_dict)
        elif ret.matched_count and ret.matched_count > 1:
            self.delete(query)
            self.add(kv_dict)

class NewsDBAPI(DBAPI):
    def __init__(self, db_engine, db_ip, db_port, db_name, table_name):
        super(NewsDBAPI, self).__init__(db_engine, db_ip, db_port, db_name, table_name)

    def add_news(self, url, kv_dict):
        return self.update({"url": url}, kv_dict)

    def get_news_list(self, compname, page, page_count):
        return self.table.find({"compname": compname, "rewritten_title": {"$ne": None}}, projection={"_id": False}).sort([("publish_time",-1)]).skip((page-1)*page_count).limit(page_count)

    def get_news(self, url):
        return self.get_one({"url": url})

    def process_news(self, news):
        if not news:
            return None
        content = []
        news["small_images"] = []
        for line in news["content"]:
            # image
            if line.strip().find("http") == 0:
                image = image_db_api.get_image(line.strip())
                if image:
                    line = image_server + image["image_path"]
                    size_args = "t" + str(image["small_width"]) + "x" + str(image["small_height"])
                    tokens = line.strip().split('.')
                    tokens[-1] = size_args + "." + tokens[-1]
                    small_image_url = '.'.join(tokens)
                    news["small_images"].append(small_image_url)
                content.append({"img": line})
            else:
                content.append({"string": line})
        if len(content) != 0:
            content_merged = []
            pre_string = ""
            pre_type = ""
            if "img" in content[0]:
                pre_type = "img"
            elif "string" in content[0]:
                pre_type = "string"
                pre_string = content[0]["string"]

            for i in range(1, len(content)):
                if "string" in content[i]:
                    pre_string += content[i]["string"]
                    pre_type = "string"
                else:
                    content_merged.append({"string": pre_string})
                    content_merged.append(content[i])
                    pre_type = "img"
                    pre_string = ""
            if pre_string != "":
                content_merged.append({"string": pre_string})
            content = content_merged
        news["content"] = content
        news["url"] = news_page_server + "?src=" + news["url"]
        return news

class ImageDBAPI(DBAPI):
    def __init__(self, db_engine, db_ip, db_port, db_name, table_name):
        super(ImageDBAPI, self).__init__(db_engine, db_ip, db_port, db_name, table_name)

    def add_image(self, raw_url, kv_dict):
        return self.update({"raw_url": raw_url}, kv_dict)

    def get_image(self, raw_url):
        return self.get_one({"raw_url": raw_url})

    def add_team_logo(self, team, kv_dict):
        return self.update({"team": team}, kv_dict)

    def get_team_logo(self, team):
        return self.get_one({"team": team})

class MatchDBAPI(DBAPI):
    def __init__(self, db_engine, db_ip, db_port, db_name, table_name):
        super(MatchDBAPI, self).__init__(db_engine, db_ip, db_port, db_name, table_name)

    def get_match(self, query):
        self.get_all(query)

    def add_match(self, url, kv_dict):
        self.update({"url": url}, kv_dict)

    def update_now_comp_info(self, compname, kv_dict):
        kv_dict["type"] = "now_comp_info"
        #self.delete({"compname": compname, "type": "now_comp_info"})
        self.update({"compname": compname, "type": "now_comp_info"}, kv_dict)

    def get_now_comp_info(self, compname):
        return self.get_one({"compname": compname, "type": "now_comp_info"})

    def get_match_list(self, compname, season):
        return self.table.find({"compname": compname, "season": season, "type": {"$exists": False}}, projection={"_id": False}).sort([("rd", 1)])

    def process_match_list(self, match_list):
        matches = []
        rd_matches = {}
        rd_matches["rd"] = match_list[0]["rd"]
        rd_matches["matches"] = []
        logo_size_args = "t" + team_logo_width + "x" + team_logo_height
        for match in match_list:
            host_logo_url = image_server + image_db_api.get_team_logo(match["host_team"])["images"][0]["path"]
            tokens = host_logo_url.strip().split('.')
            tokens[-1] = logo_size_args + "." + tokens[-1]
            host_logo_url = '.'.join(tokens)
            match["host_logo"] = host_logo_url

            guest_logo_url = image_server + image_db_api.get_team_logo(match["guest_team"])["images"][0]["path"]
            tokens = guest_logo_url.strip().split('.')
            tokens[-1] = logo_size_args + "." + tokens[-1]
            guest_logo_url = '.'.join(tokens)
            match["guest_logo"] = guest_logo_url
            if match["rd"] == rd_matches["rd"]:
                rd_matches["matches"].append(match)
            else:
                matches.append(rd_matches)
                rd_matches = {}
                rd_matches["rd"] = match["rd"]
                rd_matches["matches"] = [match]
        if len(rd_matches["matches"]) > 0:
            matches.append(rd_matches)
        return matches

class JifenDBAPI(DBAPI):
    def __init__(self, db_engine, db_ip, db_port, db_name, table_name):
        super(JifenDBAPI, self).__init__(db_engine, db_ip, db_port, db_name, table_name)

    def add_team_jifen(self, compname, team, season, kv_dict):
        query = {}
        query["compname"] = compname
        query["team"] = team
        query["season"] = season
        self.update(query, kv_dict)

    def get_team_jifen_list(self, compname, season):
        return self.table.find({"compname": compname, "season": season}, projection={"_id": False}).sort([("rank", 1)])

class ShooterDBAPI(DBAPI):
    def __init__(self, db_engine, db_ip, db_port, db_name, table_name):
        super(ShooterDBAPI, self).__init__(db_engine, db_ip, db_port, db_name, table_name)

    def add_shooter(self, compname, player, season, kv_dict):
        query = {}
        query["compname"] = compname
        query["player"] = player
        query["season"] = season
        self.update(query, kv_dict)

    def get_shooter_list(self, compname, season):
        return self.table.find({"compname": compname, "season": season}, projection={"_id": False}).sort([("rank", 1)])

    def reset_shooter_list(self, compname, season):
        return self.delete({"compname": compname, "season": season})

class LotteryDBAPI(DBAPI):
    def __init__(self, db_engine, db_ip, db_port, db_name, table_name):
        super(LotteryDBAPI, self).__init__(db_engine, db_ip, db_port, db_name, table_name)

    def add_yapei(self, compname, season, rd, host_team, guest_team, bookmaker, kv_dict):
        query = {}
        query["compname"] = compname
        query["season"] = season
        query["rd"] = rd
        query["host_team"] = host_team
        query["guest_team"] = guest_team
        query["bookmaker"] = bookmaker
        query["lottery_type"] = "asia"
        self.update(query, kv_dict)

    def add_oupei(self, compname, season, rd, host_team, guest_team, bookmaker, kv_dict):
        query = {}
        query["compname"] = compname
        query["season"] = season
        query["rd"] = rd
        query["host_team"] = host_team
        query["guest_team"] = guest_team
        query["bookmaker"] = bookmaker
        query["lottery_type"] = "europe"
        self.update(query, kv_dict)

    def get_lottery_list(self, lottery_type, compname, season, rd, host_team, guest_team):
        query = {}
        query["compname"] = compname
        query["season"] = season
        query["rd"] = int(rd)
        query["host_team"] = host_team
        query["guest_team"] = guest_team
        query["lottery_type"] = lottery_type
        return self.table.find(query, projection={"_id": False})

class DBAPITest(unittest.TestCase):
    def setUp(self):
        self.db_api = DBAPI(db_engine,
                            db_ip,
                            db_port,
                            "test",
                            "test_table")

    def test(self):
        db_api = self.db_api
        db_api.add({"url": "test_url", "k": "v"})
        self.assertEqual(db_api.get_one({"url": "test_url"})["k"], "v")

        db_api.update({"url": "test_url"}, {"url_update": "url_update"})
        ob = db_api.get_one({"url": "test_url"})
        self.assertEqual(ob["url_update"], "url_update")

        db_api.delete({"url": "test_url"})
        self.assertEqual(db_api.get_one({"url": "test_url"}), None)

class NewsDBAPITest(unittest.TestCase):
    def setUp(self):
        self.news_db_api = NewsDBAPI(db_engine,
                                     db_ip,
                                     db_port,
                                     "test",
                                     "test_news_table")

    def test(self):
        db_api = self.news_db_api
        db_api.add_news("test_url", {"url": "test_url", "content": "c"})
        ob = db_api.get_news("test_url")
        self.assertEqual(ob["url"], "test_url")
        self.assertEqual(ob["content"], "c")
        db_api.add_news("test_url", {"url": "test_url", "content": "xx"})
        ob = db_api.get_news("test_url")
        self.assertEqual(ob["url"], "test_url")
        self.assertEqual(ob["content"], "xx")

class ImageDBAPITest(unittest.TestCase):
    def setUp(self):
        self.image_db_api = ImageDBAPI(db_engine,
                                       db_ip,
                                       db_port,
                                       "test",
                                       "test_image_table")

    def test(self):
        db_api = self.image_db_api
        db_api.add_image("raw_url", {"raw_url": "raw_url", "image_path": "p"})
        ob = db_api.get_image("raw_url")
        self.assertEqual(ob["raw_url"], "raw_url")
        self.assertEqual(ob["image_path"], "p")


# 资讯数据库API
news_db_api = NewsDBAPI(db_engine,
                        db_ip,
                        db_port,
                        db_name,
                        news_table_name)

# 清洗组装后的资讯数据库
processed_news_db_api = NewsDBAPI(db_engine,
                                  db_ip,
                                  db_port,
                                  db_name,
                                  processed_news_table_name)

# 图片数据库API
image_db_api = ImageDBAPI(db_engine,
                          db_ip,
                          db_port,
                          db_name,
                          image_table_name)

# 比赛数据库API
match_db_api = MatchDBAPI(db_engine,
                          db_ip,
                          db_port,
                          db_name,
                          match_table_name)

# 积分数据库API
jifen_db_api = JifenDBAPI(db_engine,
                          db_ip,
                          db_port,
                          db_name,
                          jifen_table_name)

# 射手榜数据库API
shooter_db_api = ShooterDBAPI(db_engine,
                              db_ip,
                              db_port,
                              db_name,
                              shooter_table_name)

# 赔率数据库API
lottery_db_api = LotteryDBAPI(db_engine,
                              db_ip,
                              db_port,
                              db_name,
                              lottery_table_name)

if __name__ == '__main__':
    unittest.main()
