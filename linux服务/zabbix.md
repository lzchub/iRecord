#1 zabbix
##1.1 yum安装

官网3.4中文文档：[https://www.zabbix.com/documentation/3.4/zh/manual](https://www.zabbix.com/documentation/3.4/zh/manual)

**Server:**

	1.更新yum源
		~]# rpm -ivh https://mirrors.aliyun.com/zabbix/zabbix/3.0/rhel/7/x86_64/zabbix-release-3.0-1.el7.noarch.rpm
	2.server端安装相关软件
		~]# yum install zabbix-web zabbix-server-mysql zabbix-get zabbix-web-mysql mariadb-server -y
	3.修改php时区配置
		~]# vim/etc/httpd/conf.d/zabbix.conf
			php_value date.timezone Asia/Shanghai
	4.数据库配置
		~]# vim /etc/my.cnf
			skip_name_resolve=ON
		~]# systemctl start mariadb
		~]# mysql
		> create database zabbix;
		> grant all on zabbix.* to zbxuser@'192.168.%.%' identified by 'zbxpass';
		> grant all on zabbix.* to zbxuser@'localhost' identified by 'zbxpass';
		> flush privileges;
		~]# zcat /usr/share/doc/zabbix-server-mysql-3.0.24/create.sql.gz | mysql -uzbxuser -pzbxpass zabbix
	5.修改zabbix-server配置
		~]# vim /etc/zabbix/zabbix_server.conf
			DBHost=localhost  #数据库所在主机
			DBName=zabbix  #数据库名
			DBUser=zabbix  #数据库用户
			DBPassword=123456  #数据库密码
	6.启动服务
		~]# systemctl start zabbix-server httpd

	7.访问web界面
		http://192.168.164.134/zabbix/setup.php
		初始账号：Admin
		初始密码：zabbix

**Agent:**

	1.更新yum源
		~]# rpm -ivh https://mirrors.aliyun.com/zabbix/zabbix/3.0/rhel/7/x86_64/zabbix-release-3.0-1.el7.noarch.rpm
	2.agent端安装相关软件
		~]# yum install -y zabbix-sender zabbix-agent
	3.修改zabbix-agent配置
		~]# vim /etc/zabbix/zabbix_agentd.conf 
			Server=192.168.179.110			#若有proxy，则server为proxy
	4.启动服务
		~]# systemctl start zabbix-agent


	windows:
		windows客户端
		拷贝安装包到相应位置（官网下载）
		在命令行执行命令：
			安装agent ： D:\zabbix\bin\win64\zabbix_agentd.exe -i -c D:\zabbix\conf\zabbix_agentd.win.conf
			启动agent客户端 ：D:\zabbix\bin\win64\zabbix_agentd.exe -c D:\zabbix\conf\zabbix_agentd.win.conf -s
		打开windows的zabbix服务
		开启防火墙规则，允许10050端口，防火墙允许ping服务

		https://blog.csdn.net/wh211212/article/details/78836729

	注： 
		报错：active check configuration update from [127.0.0.1:10051] started to fail (cannot connect to [[127.0.0.1]:10051]: [111] Connection refused)
		直接注释掉：
			ActiveServer

	
**Proxy：**

	1.更新yum源
		~]# rpm -ivh https://mirrors.aliyun.com/zabbix/zabbix/3.0/rhel/7/x86_64/zabbix-release-3.0-1.el7.noarch.rpm
	2.proxy端安装相关软件
		~]# yum install -y zabbix-proxy-mysql zabbix-get mariadb-server
	3.数据库配置
		~]# systemctl start mariadb
		~]# mysql
			> create database zabbix_proxy;
			> grant all on zabbix_proxy.* to zbxproxy@'localhost' identified by 'zbxpass';
			> flush privileges;
		~]# zcat /usr/share/doc/zabbix-proxy-mysql-3.0.24/schema.sql.gz | mysql -uzbxproxy -pzbxpass zabbix_proxy
	4.修改zabbix-proxy配置			
		]# cat /etc/zabbix/zabbix_proxy.conf | grep -Ev "^#|^$"
			Server=192.168.164.134
			Hostname=proxy.zabbix.com
			DBHost=localhost
			DBName=zabbix_proxy
			DBUser=zbxproxy
			DBPassword=zbxpass
			
	5.启动服务
		~]# systemctl start zabbix-proxy

**注：以上默认为被动模式，若为主动模式，要注意hostname参数。**

##1.2 源码安装zabbix-server

##1.3 自动发现

	配置——>定义自动发现——>定义动作	
	
	注意：agent端，hostname参数就是server自动发现后的名字，否则默认为主机名

##1.4 定义报警媒介，定义动作，添加报警
	
##1.5 添加模板
	
##1.6 主动模式与被动模式

	被动模式：默认为被动模式，服务端会主动连接客户端获取监控项目数据，客户端被动地接受连接，并把监控信息传递给服务端
	~]# cat /etc/zabbix/zabbix_agentd.conf | grep -Ev "^#|^$" 
		PidFile=/var/run/zabbix/zabbix_agentd.pid
		LogFile=/var/log/zabbix/zabbix_agentd.log
		LogFileSize=0
		Server=192.168.164.134						#被动模式配置这个参数即可
		Hostname=Zabbix server
		Include=/etc/zabbix/zabbix_agentd.d/*.conf


	主动模式：客户端会把监控数据汇报给服务端，服务端只负责接受即可
	~]# cat /etc/zabbix/zabbix_agentd.conf | grep -Ev "^#|^$"
		PidFile=/var/run/zabbix/zabbix_agentd.pid
		LogFile=/var/log/zabbix/zabbix_agentd.log
		LogFileSize=0
		Server=192.168.164.134						#服务器参数
		StartAgents=0								#设置为0表示启用主动模式， 不监听本地端口
		ServerActive=192.168.164.134				#zabbix server的IP或域名，指agent收集的数据往哪儿发送
		Hostname=192.168.164.137					#agent的名称，不配置则使用主机名，必须要和server端添加主机的名字相同
		Include=/etc/zabbix/zabbix_agentd.d/*.conf



	注:
		1.当客户端数量非常多时，建议使用主动给模式，降低服务器压力
		2.主动模式需要使用主动模式模板
		3.主动模式下，zbx监控可能不会显示或者显示错误，但任有数据跟新
[https://www.jianshu.com/p/ddc7f2dc51ae](https://www.jianshu.com/p/ddc7f2dc51ae)

##1.7 添加监控，item，triggers，graph，screen
	

##1.8 监控nginx连接数,自定义key

	在需要监控的agent上执行

	UserParameter=nginx.status[*],./usr/bin/ngxstatus.sh $1		

	~]# chmod +x ngxstatus.sh
	~]# cat ngxstatus.sh
		#!/bin/bash
		HOST=127.0.0.1
		PORT=80
		URI='ngxstatus'
		
		active(){
		    curl -s http://$HOST:$PORT/$URI | awk '/^Active/{print $3}'
		}
		accepts(){
		    curl -s http://$HOST:$PORT/$URI | awk 'NR==3{print $1}'
		}
		handled(){
		    curl -s http://$HOST:$PORT/$URI | awk 'NR==3{print $2}'
		}
		requests(){
		    curl -s http://$HOST:$PORT/$URI | awk 'NR==3{print $3}'
		}
		reading(){
		    curl -s http://$HOST:$PORT/$URI | awk 'NR==4{print $2}'
		}
		writing(){
		    curl -s http://$HOST:$PORT/$URI | awk 'NR==4{print $4}'
		}
		waiting(){
		    curl -s http://$HOST:$PORT/$URI | awk 'NR==4{print $6}'
		}
		
		$1	

	注：需重启agent刷新配置

	服务器测试
		zabbix_get -s IP -p 10050 -k "nginx.status[active..]"

##1.9 监控tomcat
	
	1.1 agent主机上安装
		~]# yum install -y java-1.8.0-openjdk-devel zabbix-java-gateway
	1.2 配置
		~]# vim /etc/zabbix/zabbix_java_gateway.conf
	1.3 启动
		~]# systemctl start zabbix-java-gateway
	2.1 agent主机tomcat安装
		~]# cd /usr/local/src
		~]# wget http://mirrors.hust.edu.cn/apache/tomcat/tomcat-8/v8.5.32/bin/apache-tomcat-8.5.32.tar.gz
		~]# tar -xzvf apache-tomcat-8.5.32.tar.gz -C /usr/local/
		~]# ln -s /usr/local/apache-tomcat-8.5.32/ /usr/local/tomcat
	2.2 添加监控配置
		~]# vim /usr/local/tomcat/bin/catalina.sh
			CATALINA_OPTS="$CATALINA_OPTS -Dcom.sun.management.jmxremote
			  -Dcom.sun.management.jmxremote.port=8888
			  -Dcom.sun.management.jmxremote.ssl=false
			  -Dcom.sun.management.jmxremote.authenticate=false
			  -Djava.rmi.server.hostname=IPADDR"
	2.3 启动tomcat
		~]# /usr/local/tomcat/bin/startup.sh

	3.1 server主机配置
		~]# vim /etc/zabbix/zabbix_server.conf
			JavaGateway=192.168.179.143  #监控客户机
			StartJavaPollers=5   #开启进程数
	3.2 重启server
		~]# systemctl restart zabbix-server
		
	注：若是编译安装，记得设置环境变量

##.x自定义报警脚本

	下载zabbix server源码包
	wget -O zabbix-4.0.4.tar.gz  https://sourceforge.net/projects/zabbix/files/ZABBIX%20Latest%20Stable/4.0.4/zabbix-4.0.4.tar.gz/download
	
	安装依赖
	yum install wget telnet net-tools python-paramiko gcc gcc-c++ dejavu-sans-fonts python-setuptools python-devel sendmail mailx net-snmp net-snmp-devel net-snmp-utils freetype-devel libpng-devel perl unbound libtasn1-devel p11-kit-devel OpenIPMI unixODBC  libevent-devel  mysql-devel  libxml2-devel  libssh2-devel  OpenIPMI-devel  java-1.8.0-openjdk-devel  openldap-devel  curl-devel unixODBC-devel
	
	解压并编译安装
	tar -zxvf zabbix-4.0.4.tar.gz
	cd  zabbix-4.0.4/
	
	建立编译安装目录
	mkdir -p /data/findsec/zabbix
	./configure --prefix=/data/findsec/zabbix  --enable-server  --enable-agent --enable-java  --with-mysql --with-libxml2 --with-unixodbc  --with-net-snmp --with-ssh2 --with-openipmi --with-ldap --with-libcurl --with-iconv
	make
	make install
	
	
	/data/findsec/zabbix/sbin/zabbix_server  -V
	
	
	数据库安装
	yum install mariadb-server
	systemctl  start mariadb.service
	systemctl  status mariadb.service
	mysql_secure_installation
	
	创建数据库
	mysql -uroot -p
	create database zabbix character set utf8 collate utf8_bin;
	grant all privileges on zabbix.* to zabbix@localhost identified by 'zabbix@findsec123';
	
	导入数据结构
	mysql -uzabbix -pzabbix@findsec123  zabbix < /root/zabbix-4.0.4/database/mysql/schema.sql 
	mysql -uzabbix -pzabbix@findsec123  zabbix < /root/zabbix-4.0.4/database/mysql/images.sql
	mysql -uzabbix -pzabbix@findsec123  zabbix < /root/zabbix-4.0.4/database/mysql/data.sql 
	
	修改zabbix server配置
	vim /data/findsec/zabbix/etc/zabbix_server.conf
	
	增加用户
	groupadd --system zabbix
	useradd --system -g zabbix -d /usr/lib/zabbix -s /sbin/nologin -c "Zabbix Monitoring System" zabbix
	
	启动服务
	/data/findsec/zabbix/sbin/zabbix_server -c /data/findsec/zabbix/etc/zabbix_server.conf
	
	tailf /tmp/zabbix_server.log
	
	
	增加Zabbix镜像源
	rpm -ivh https://repo.zabbix.com/zabbix/4.0/rhel/7/x86_64/zabbix-release-4.0-1.el7.noarch.rpm
	
	安装Zabbix Frontend
	yum install zabbix-web-mysql
	
	配置Zabbix frontend
	vim /etc/php.ini
	
	max_execution_time = 300
	memory_limit = 128M
	post_max_size = 16M
	upload_max_filesize = 2M
	max_input_time = 300
	max_input_vars = 10000
	always_populate_raw_post_data = -1
	date.timezone = Asia/Shanghai
	
	
	启动httpd
	systemctl  start  httpd.service
	systemctl  status  httpd.service
	
	http://10.211.55.7/zabbix/setup.php
	
	Admin
	zabbix
	
	
	安装Zabbix Agent
	yum install zabbix-agent
	
	systemctl  start zabbix-agent.service