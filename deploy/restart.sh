#!bin/bash

# 重启图片服务器
sudo /usr/local/openresty/nginx/sbin/nginx -s reload

# 重启news_server
sudo supervisorctl restart news_server_list:*
