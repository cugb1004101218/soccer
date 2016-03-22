# -*- coding: utf-8 -*-
import scrapy
import datetime
import json
from soccer_spider.items import Match, NowCompInfo, TeamJifen, MatchAsiaLottery, MatchEuropeLottery
import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

class LotterySpider(scrapy.Spider):
    name = "lottery_spider"
    allowed_domains = ["platform.sina.com.cn"]
    start_urls = (
        # 英超
        "http://platform.sina.com.cn/sports_all/client_api?app_key=3979320659&%20_sport_t_=Odds&_sport_a_=typeSDMatches&type=8",
        # 意甲
        "http://platform.sina.com.cn/sports_all/client_api?app_key=3979320659&%20_sport_t_=Odds&_sport_a_=typeSDMatches&type=21",
        # 西甲
        "http://platform.sina.com.cn/sports_all/client_api?app_key=3979320659&%20_sport_t_=Odds&_sport_a_=typeSDMatches&type=23",
        # 德甲
        "http://platform.sina.com.cn/sports_all/client_api?app_key=3979320659&%20_sport_t_=Odds&_sport_a_=typeSDMatches&type=22",
    )

    def parse(self, response):
        result = json.loads(response.body)
        for rd in range(1, int(result["result"]["max_rnd"]) + 1):
            url = response.url + "&rnd=" + str(rd)
            yield self.crawl_comp(url)

    def crawl_comp(self, url):
        return scrapy.http.Request(url=url,
                                   callback=lambda response : self.crawl_round(response))

    def crawl_round(self, response):
        matches = json.loads(response.body)
        for d in matches["result"]["data"]:
            print d["LeagueType_cn"], d["Season"], d["Round"], d["Team1"], d["Team2"], d["oddsid"]
            compname = d["LeagueType_cn"]
            yapei = "http://platform.sina.com.cn/sports_all/client_api?app_key=3979320659&_sport_t_=Odds&_sport_a_=AsiaIniNewData&id=" + d["oddsid"]
            yield scrapy.http.Request(url=yapei,
                                      callback=lambda response,
                                      host_team=d["Team1"],
                                      guest_team=d["Team2"],
                                      season=d["Season"],
                                      compname=compname,
                                      rd=int(d["Round"]): self.crawl_yapei(response, host_team, guest_team, season, compname, rd))
            oupei = "http://platform.sina.com.cn/sports_all/client_api?app_key=3979320659&_sport_t_=Odds&_sport_a_=euroIniNewData&id=" + d["oddsid"]
            yield scrapy.http.Request(url=oupei,
                                      callback=lambda response,
                                      host_team=d["Team1"],
                                      guest_team=d["Team2"],
                                      season=d["Season"],
                                      compname=compname,
                                      rd=int(d["Round"]): self.crawl_oupei(response, host_team, guest_team, season, compname, rd))

    def crawl_yapei(self, response, host_team, guest_team, season, compname, rd):
        result = json.loads(response.body)
        for d in result["result"]["data"]:
            match_lottery = MatchAsiaLottery()
            match_lottery["lottery_type"] = "asia"
            match_lottery["bookmaker"] = d["name"]
            match_lottery["host_team"] = host_team
            match_lottery["guest_team"] = guest_team
            match_lottery["season"] = season + "/" + str(int(season) + 1)
            match_lottery["compname"] = compname
            match_lottery["rd"] = rd
            match_lottery["initial_host_shuiwei"] = float(d["ini"]["o1"])
            match_lottery["initial_guest_shuiwei"] = float(d["ini"]["o2"])
            match_lottery["initial_pankou"] = d["ini"]["o3"]
            match_lottery["new_host_shuiwei"] = float(d["new"]["o1"])
            match_lottery["new_guest_shuiwei"] = float(d["new"]["o2"])
            match_lottery["new_pankou"] = d["new"]["o3"]
            match_lottery["change_time"] = d["new"]["change_time"]
            yield match_lottery

    def crawl_oupei(self, response, host_team, guest_team, season, compname, rd):
        result = json.loads(response.body)
        if result["result"]["status"]["code"] != 0:
            return
        for d in result["result"]["data"]:
            match_lottery = MatchEuropeLottery()
            match_lottery["lottery_type"] = "europe"
            match_lottery["bookmaker"] = d["name"]
            match_lottery["host_team"] = host_team
            match_lottery["guest_team"] = guest_team
            match_lottery["season"] = season + "/" + str(int(season) + 1)
            match_lottery["compname"] = compname
            match_lottery["rd"] = rd
            match_lottery["initial_win"] = float(d["odds"]["ini"]["o1"])
            match_lottery["initial_lost"] = float(d["odds"]["ini"]["o3"])
            match_lottery["initial_tie"] = float(d["odds"]["ini"]["o2"])
            match_lottery["new_win"] = float(d["odds"]["new"]["o1"])
            match_lottery["new_lost"] = float(d["odds"]["new"]["o3"])
            match_lottery["new_tie"] = float(d["odds"]["new"]["o2"])
            match_lottery["change_time"] = d["odds"]["new"]["change_time"]
            yield match_lottery
