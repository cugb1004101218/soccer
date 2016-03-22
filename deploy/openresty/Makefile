.PHONY: all install clean

all:
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/LuaJIT-2.1-20160108 && $(MAKE) TARGET_STRIP=@: CCDEBUG=-g CC=cc PREFIX=/usr/local/openresty/luajit
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/lua-cjson-2.1.0.3 && $(MAKE) DESTDIR=$(DESTDIR) LUA_INCLUDE_DIR=/home/cugbacm/zhuzekun/soccer/deploy/openresty/build/luajit-root/usr/local/openresty/luajit/include/luajit-2.1 LUA_CMODULE_DIR=/usr/local/openresty/lualib LUA_MODULE_DIR=/usr/local/openresty/lualib CJSON_CFLAGS="-g -fpic" CC=cc
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/lua-redis-parser-0.12 && $(MAKE) DESTDIR=$(DESTDIR) LUA_INCLUDE_DIR=/home/cugbacm/zhuzekun/soccer/deploy/openresty/build/luajit-root/usr/local/openresty/luajit/include/luajit-2.1 LUA_LIB_DIR=/usr/local/openresty/lualib CC=cc
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/lua-rds-parser-0.06 && $(MAKE) DESTDIR=$(DESTDIR) LUA_INCLUDE_DIR=/home/cugbacm/zhuzekun/soccer/deploy/openresty/build/luajit-root/usr/local/openresty/luajit/include/luajit-2.1 LUA_LIB_DIR=/usr/local/openresty/lualib CC=cc
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/nginx-1.9.7 && $(MAKE)

install: all
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/LuaJIT-2.1-20160108 && $(MAKE) install TARGET_STRIP=@: CCDEBUG=-g CC=cc PREFIX=/usr/local/openresty/luajit DESTDIR=$(DESTDIR)
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/lua-cjson-2.1.0.3 && $(MAKE) install DESTDIR=$(DESTDIR) LUA_INCLUDE_DIR=/home/cugbacm/zhuzekun/soccer/deploy/openresty/build/luajit-root/usr/local/openresty/luajit/include/luajit-2.1 LUA_CMODULE_DIR=/usr/local/openresty/lualib LUA_MODULE_DIR=/usr/local/openresty/lualib CJSON_CFLAGS="-g -fpic" CC=cc
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/lua-redis-parser-0.12 && $(MAKE) install DESTDIR=$(DESTDIR) LUA_INCLUDE_DIR=/home/cugbacm/zhuzekun/soccer/deploy/openresty/build/luajit-root/usr/local/openresty/luajit/include/luajit-2.1 LUA_LIB_DIR=/usr/local/openresty/lualib CC=cc
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/lua-rds-parser-0.06 && $(MAKE) install DESTDIR=$(DESTDIR) LUA_INCLUDE_DIR=/home/cugbacm/zhuzekun/soccer/deploy/openresty/build/luajit-root/usr/local/openresty/luajit/include/luajit-2.1 LUA_LIB_DIR=/usr/local/openresty/lualib CC=cc
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/lua-resty-dns-0.14 && $(MAKE) install DESTDIR=$(DESTDIR) LUA_LIB_DIR=/usr/local/openresty/lualib INSTALL=/home/cugbacm/zhuzekun/soccer/deploy/openresty/build/install
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/lua-resty-memcached-0.13 && $(MAKE) install DESTDIR=$(DESTDIR) LUA_LIB_DIR=/usr/local/openresty/lualib INSTALL=/home/cugbacm/zhuzekun/soccer/deploy/openresty/build/install
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/lua-resty-redis-0.22 && $(MAKE) install DESTDIR=$(DESTDIR) LUA_LIB_DIR=/usr/local/openresty/lualib INSTALL=/home/cugbacm/zhuzekun/soccer/deploy/openresty/build/install
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/lua-resty-mysql-0.15 && $(MAKE) install DESTDIR=$(DESTDIR) LUA_LIB_DIR=/usr/local/openresty/lualib INSTALL=/home/cugbacm/zhuzekun/soccer/deploy/openresty/build/install
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/lua-resty-string-0.09 && $(MAKE) install DESTDIR=$(DESTDIR) LUA_LIB_DIR=/usr/local/openresty/lualib INSTALL=/home/cugbacm/zhuzekun/soccer/deploy/openresty/build/install
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/lua-resty-upload-0.09 && $(MAKE) install DESTDIR=$(DESTDIR) LUA_LIB_DIR=/usr/local/openresty/lualib INSTALL=/home/cugbacm/zhuzekun/soccer/deploy/openresty/build/install
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/lua-resty-websocket-0.05 && $(MAKE) install DESTDIR=$(DESTDIR) LUA_LIB_DIR=/usr/local/openresty/lualib INSTALL=/home/cugbacm/zhuzekun/soccer/deploy/openresty/build/install
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/lua-resty-lock-0.04 && $(MAKE) install DESTDIR=$(DESTDIR) LUA_LIB_DIR=/usr/local/openresty/lualib INSTALL=/home/cugbacm/zhuzekun/soccer/deploy/openresty/build/install
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/lua-resty-lrucache-0.04 && $(MAKE) install DESTDIR=$(DESTDIR) LUA_LIB_DIR=/usr/local/openresty/lualib INSTALL=/home/cugbacm/zhuzekun/soccer/deploy/openresty/build/install
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/lua-resty-core-0.1.4 && $(MAKE) install DESTDIR=$(DESTDIR) LUA_LIB_DIR=/usr/local/openresty/lualib INSTALL=/home/cugbacm/zhuzekun/soccer/deploy/openresty/build/install
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/lua-resty-upstream-healthcheck-0.03 && $(MAKE) install DESTDIR=$(DESTDIR) LUA_LIB_DIR=/usr/local/openresty/lualib INSTALL=/home/cugbacm/zhuzekun/soccer/deploy/openresty/build/install
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/resty-cli-0.05 && /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/install resty $(DESTDIR)/usr/local/openresty/bin/
	cd /home/cugbacm/zhuzekun/soccer/deploy/openresty/build/nginx-1.9.7 && $(MAKE) install DESTDIR=$(DESTDIR)

clean:
	rm -rf build
