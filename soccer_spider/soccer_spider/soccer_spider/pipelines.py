# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import settings
import sys
sys.path.append('/home/cugbacm/zhuzekun/soccer/common/')
from db_api import news_db_api, image_db_api, match_db_api, jifen_db_api, shooter_db_api, lottery_db_api, processed_news_db_api
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
from scrapy import log
import PIL.Image
import math

class NewsPipeline(object):
    def process_item(self, item, spider):
        if spider.name not in ["news_spider"]:
            return item
        if str(item.__class__) == "<class 'soccer_spider.items.News'>":
            news_db_api.add_news(item["url"], dict(item))
            #item.gen_news()
            #processed_news_db_api.add_news(item["url"], dict(item))
        elif str(item.__class__) == "<class 'soccer_spider.items.Image'>":
            # 设置图片原始size和缩略图size
            self.set_size(item)
            image_db_api.add_image(item["raw_url"], dict(item))
        return item

    def set_size(self, item):
        item["image_path"] = item["images"][0]["path"]
        im = PIL.Image.open(settings.IMAGES_STORE + "/" + item["image_path"])
        item["width"] = im.size[0]
        item["height"] = im.size[1]
        # 计算缩放比例
        rate = max(float(item["width"]) / float(settings.SMALL_IMAGE_WIDTH), float(item["height"]) / float(settings.SMALL_IMAGE_HEIGHT))
        # 宽度和高度不能超过设定的最大值
        item["small_width"] = int(min(settings.SMALL_IMAGE_WIDTH, math.ceil(float(item["width"]) / rate)))
        item["small_height"] = int(min(settings.SMALL_IMAGE_HEIGHT, math.ceil(float(item["height"]) / rate)))

class MatchPipeline(object):
    def process_item(self, item, spider):
        if spider.name not in ["match_spider"]:
            return item
        if str(item.__class__) == "<class 'soccer_spider.items.Match'>":
            match_db_api.add_match(item["url"], dict(item))
        elif str(item.__class__) == "<class 'soccer_spider.items.NowCompInfo'>":
            match_db_api.update_now_comp_info(item["compname"], dict(item))
        elif str(item.__class__) == "<class 'soccer_spider.items.TeamJifen'>":
            jifen_db_api.add_team_jifen(item["compname"], item["team"], item["season"], dict(item))
        elif  str(item.__class__) == "<class 'soccer_spider.items.TeamLogoImage'>":
            item["image_path"] = item["images"][0]["path"]
            image_db_api.add_team_logo(item["team"], dict(item))
        return item

class ShooterPipeline(object):
    def process_item(self, item, spider):
        if spider.name not in ["shooter_spider"]:
            return item
        if str(item.__class__) == "<class 'soccer_spider.items.Shooter'>":
            shooter_db_api.add_shooter(item["compname"], item["player"], item["season"], dict(item))

class LotteryPipeline(object):
    def process_item(self, item, spider):
        if spider.name not in ["lottery_spider"]:
            return item
        if str(item.__class__) == "<class 'soccer_spider.items.MatchAsiaLottery'>":
            lottery_db_api.add_yapei(item["compname"],
                                     item["season"],
                                     item["rd"],
                                     item["host_team"],
                                     item["guest_team"],
                                     item["bookmaker"], dict(item))
        elif str(item.__class__) == "<class 'soccer_spider.items.MatchEuropeLottery'>":
            lottery_db_api.add_oupei(item["compname"],
                                     item["season"],
                                     item["rd"],
                                     item["host_team"],
                                     item["guest_team"],
                                     item["bookmaker"], dict(item))
