#!bin/bash

# 安装 mongo
apt-get install mongodb

# 安装scrapy
pip install scrapy

# 安装tornado
pip install tornado

# redis python
pip install redis

pip install pymongo

pip install pillow

# 安装redis
apt-get install redis-server


# 安装 nginx
apt-get install libgd2-xpm libgd2-xpm-dev
apt-get install curl
apt-get install libcurl4-gnutls-dev
cd ./openresty
./configure --add-module=./ngx_image_thumb-master
make
make install

#ln -s /usr/local/openresty/nginx/conf/nginx.conf ../config/nginx.conf

# 安装Supervisord
pip install supervisor
