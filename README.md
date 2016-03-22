# 数据源
爬取网易体育的足球相关的数据。
爬取新浪体育足彩相关的数据。

# demo 接口
    足彩接口：http://115.28.170.176:8000/lottery?compname=英超&season=2015/2016&rd=31&host_team=西布朗&guest_team=诺维奇&lottery_type=europe
    资讯接口：http://115.28.170.176:8000/news?compname=英超&page=1&page_count=2
    射手榜：http://115.28.170.176:8000/shooter?compname=英超
    积分榜：http://115.28.170.176:8000/jifen?compname=英超
    赛程：http://115.28.170.176:8000/match?compname=英超

# 爬虫 soccer_spider
基于scrapy，数据库用的mongodb，redis作为缓存


# http接口 soccer_server
    用tornado封装成http server
    资讯新闻
    积分榜
    射手榜
    赛程
    每场比赛的赔率
