#!bin/bash
for keyword in start_spider.sh start_match_spider.sh start_shooter_spider.sh start_lottery_spider.sh
do
    ps -ef|grep $keyword|grep -v grep|cut -c 9-15|xargs kill -9
done
ps -ef|grep "scrapy crawl"|grep -v grep|cut -c 9-15|xargs kill -9
