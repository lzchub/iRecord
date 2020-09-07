官网：http://apache.org

# 1.编译安装httpd

	httpd依赖：apr、apr-util、pcre、pcre-devel、expat-devel、gcc
	
	yum安装:   pcre（perl正则表达式包）、pcre-devel、expat-devel 
	需编译安装: apr、apr-util 
	编译环境:   gcc
	
	~]# wget https://mirrors.tuna.tsinghua.edu.cn/apache/apr/apr-1.6.5.tar.gz
	~]# wget https://mirrors.tuna.tsinghua.edu.cn/apache/apr/apr-util-1.6.1.tar.gz
	~]# wget https://mirrors.tuna.tsinghua.edu.cn/apache/httpd/httpd-2.4.37.tar.gz
	
	解决依赖：
		~]# yum install -y pcre pcre-devel expat-devel gcc
	
	编译apr:
		~]# tar xf apr-1.6.5.tar.gz
		~]# cd apr-1.6.5
		~]# ./configure --prefix=/usr/local/apr 
		~]# make && make install
	
	编译apr-util:
		~]# tar xf apr-util-1.6.1.tar.gz
		~]# cd ../apr-util-1.6.1
		~]# ./configure --prefix=/usr/local/apr-util --with-apr=/usr/local/apr
		~]# make && make install
	
	编译httpd:
		~]# tar xf httpd-2.4.37.tar.gz
		~]# cd httpd-2.4.37
		~]# ./configure --prefix=/usr/local/apache --sysconfdir=/etc/apache --with-z --with-pcre --with-apr=/usr/local/apr --with-apr-util=/usr/local/apr-util --with-mpm=event --enable-mpms-shared=all
		~]# make && make install
	
	更多编译参数：
		~]# ./configure -h
	官方配置文档：
		http://httpd.apache.org/docs/2.4/programs/configure.html#configurationoptions


编译安装后的规范操作：
	
	# 设置man路径。
	~]# echo "MANPATH /usr/local/apache/man" >>/etc/man.config
	
	# 设置PATH环境变量。
	~]# echo 'PATH=/usr/local/apache/bin:$PATH' >/etc/profile.d/apache.sh
	~]# source /etc/profile.d/apache.sh
	
	# 输出头文件。
	~]# ln -s /usr/include /usr/local/apache/include

# 2.设置长连接

	~]# cat keepalive.conf 
	KeepAlive On				#开启on,关闭off
	MaxKeepAliveRequests 100	#最大请求处理数
	KeepAliveTimeout 15		#超时时长
	
	~]# telnet 192.168.179.110 80  
	Trying 192.168.179.110...
	Connected to 192.168.179.110.
	Escape character is '^]'.
	GET /index.html HTTP/1.1
	host:192.168.179.110
	
	HTTP/1.1 200 OK
	Date: Tue, 27 Nov 2018 13:07:38 GMT
	Server: Apache/2.4.6 (CentOS)
	Last-Modified: Tue, 27 Nov 2018 13:04:16 GMT
	ETag: "a-57ba5163b963d"
	Accept-Ranges: bytes
	Content-Length: 10
	Content-Type: text/html; charset=UTF-8
	
	test page

# 3.虚拟主机
## 3.1 基于ip

	~]# ip addr add 192.168.179.111 dev ens33
	~]# cat virtualhost.conf 
	<VirtualHost 192.168.179.110:80>
	    ServerName www.ilinux.io
	    DocumentRoot /data/www/ilinux
	    <Directory /data/www/ilinux>
	        AllowOverride none
	        require all granted
	    </Directory>
	</VirtualHost>
	
	<VirtualHost 192.168.179.111:80>
	    ServerName www.iunix.io
	    DocumentRoot /data/www/iunix
	    <Directory /data/www/iunix>
	            AllowOverride none
	            require all granted
	    </Directory>
	</VirtualHost>
	
	~]# mkdir /data/www/{ilinux,iunix}/ -pv
	~]# echo www.ilinux.io > /data/www/ilinux/index.html
	~]# echo www.iunix.io > /data/www/iunix/index.html 


​	
	注：源码安装要打开主配置中的Include

## 3.2 基于端口

	~]# cat virtualhost.conf 
	Listen 8080
	
	<VirtualHost 192.168.179.110:80>
	    ServerName www.ilinux.io
	    DocumentRoot /data/www/ilinux
	    <Directory /data/www/ilinux>
	            AllowOverride none
	            require all granted
	    </Directory>
	</VirtualHost>
	
	<VirtualHost 192.168.179.110:8080>
	    ServerName www.iunix.io
	    DocumentRoot /data/www/iunix
	    <Directory /data/www/iunix>
	            AllowOverride none
	            require all granted
	    </Directory>
	</VirtualHost>

## 3.3 基于FQDN

	~]# cat virtualhost.conf 
	<VirtualHost 192.168.179.110:80>
	    ServerName www.ilinux.io
	    DocumentRoot /data/www/ilinux
	    <Directory /data/www/ilinux>
	            AllowOverride none
	            require all granted
	    </Directory>
	</VirtualHost>
	
	<VirtualHost 192.168.179.110:80>
	    ServerName www.iunix.io
	    DocumentRoot /data/www/iunix
	    <Directory /data/www/iunix>
	            AllowOverride none
	            require all granted
	    </Directory>
	</VirtualHost>
	
	注：需修改本机hosts文件
		windows：
			C:\Windows\System32\drivers\etc\hosts
		linux:
			/etc/hosts

# 4.访问控制
**基于用户：**

	~]# htpasswd -c /etc/httpd/.htpasswd tom
	~]# htpasswd /etc/httpd/.htpasswd jerry    # -c创建文件，第二次不需要添加，否则会覆盖
	
	~]# cat access.conf 
	<VirtualHost 192.168.179.110:80>
	    ServerName www.ilinux.io
	    DocumentRoot /data/www/ilinux
	    <Directory /data/www/ilinux>
	        AllowOverride None
	        AuthType Basic
	        AuthName "username & passwd"
	        AuthUserFile /etc/httpd/.htpasswd
	        Require user tom jerry
	    </Directory>
	</VirtualHost>

**基于用户组：**

	~]# echo 'allow:jerry alice' >> /etc/httpd/.htgroup
	
	<VirtualHost 192.168.100.14:80>
	    ServerName www.a.com
	    DocumentRoot /usr/local/apache/htdocs/a.com
	    <Directory /usr/local/apache/htdocs/a.com>
	            AllowOverride Authconfig
	            AuthType Basic
	            AuthName "please enter your name & passwd"
	            AuthUserFile /etc/httpd/.htpasswd
	            AuthGroupFile /etc/httpd/.htgroup
	            Require user Jim Bob
	            Require group allow
	        </Directory>
	</VirtualHost>
	
	注：所有用户都要将密码写入.htpasswd

# 5.内置status状态页

	~]# cat status.conf 
	<VirtualHost 192.168.179.110:80>
	    ServerName www.iunix.io
	    <Location /server-status>
	        SetHandler server-status
	        <RequireAll>
	                Require ip 192.168
	        </RequireAll>
	    </Location>
	</VirtualHost>
	
	http://www.iunix.io/server-status

# 6.实现文件压缩

	# mod_deflate 依赖模块
	
	~]# cat yasuo.conf
	SetOutputFilter DEFLATE
	
	AddOutputFilterByType DEFLATE text/html
	AddOutputFilterByType DEFLATE text/plain
	AddOutputFilterByType DEFLATE application/xhtml+xml
	AddOutputFilterByType DEFLATE text/xml
	AddOutputFilterByType DEFLATE application/xml
	AddOutputFilterByType DEFLATE application/x-javascript
	AddOutputFilterByType DEFLATE text/javascript
	AddOutputFilterByType DEFLATE text/css
	
	#level of compression(highest9-lowest 1)
	DeflateCompressionLevel 9

# 7.实现https服务

**CA主机：**
	
	1.CA生成
	~]# cd /etc/pki/CA/
	~]# echo 01 > serial
	~]# touch index.txt
	~]# (umask 077;openssl genrsa -out private/cakey.pem 2048)
	~]# openssl req -new -x509 -key private/cakey.pem -out cacert.pem -days 365
	Country Name (2 letter code) [XX]:CN
	State or Province Name (full name) []:SiChuan
	Locality Name (eg, city) [Default City]:ChengDu  
	Organization Name (eg, company) [Default Company Ltd]:chuan
	Organizational Unit Name (eg, section) []:chuan.com
	Common Name (eg, your name or your server's hostname) []:www.chuan.com
	Email Address []:
	
	3.颁发证书
	~]# openssl ca -in /tmp/httpd_csr.pem -out certs/httpd_crt.pem
	~]# scp certs/httpd_crt.pem root@192.168.179.110:/etc/httpd/ssl/


**httpd主机：**
	
	2.提供公钥给CA
	已开启默认http服务
	~]# yum install -y mod_ssl
	~]# cd /etc/httpd/
	~]# mkdir ssl
	~]# cd ssl/
	~]# (umask 077;openssl genrsa -out httpd_key.pem 1024)
	~]# openssl req -new -key httpd_key.pem -out httpd_csr.pem
	    Country Name (2 letter code) [XX]:CN
	    State or Province Name (full name) []:SiChuan
	    Locality Name (eg, city) [Default City]:ChengDu
	    Organization Name (eg, company) [Default Company Ltd]:chuan
	    Organizational Unit Name (eg, section) []:chuan.com
	    Common Name (eg, your name or your server's hostname) []:www.test.com 
	    Email Address []:
	
	    Please enter the following 'extra' attributes
	    to be sent with your certificate request
	    A challenge password []:
	    An optional company name []:
	~]# scp httpd_csr.pem root@192.168.179.113:/tmp/
	
	4.提供ssl配置
	~]# vim /etc/httpd/conf.d/ssl.conf
	    DocumentRoot "/var/www/html"  #若是目的修改，需要显示授权
	    ServerName www.test.com:443
	    SSLCertificateFile /etc/httpd/ssl/httpd_crt.pem
	    SSLCertificateKeyFile /etc/httpd/ssl/httpd_key.pem

# 8.压力测试

	工具：ab、webbench、http_load、jmeter、loadrunner、tcpcopy
	
	~]# yum install -y httpd-tools
	~]# ab -n 100000 -c 10 URL[http://192.168.179.110:80/index.html]

# 9.处理动态请求（httpd+php）
## 9.1 yum安装
**方法一：php编译成模块**

	~]# yum install -y httpd php php-mysql mariadb-server
	~]# cd /var/www/html/
	~]# vim index.php
		<?php
			phpinfo();
		?>
	~]# systemctl start httpd #可查看php测试页面
	
	~]# vim mysql.php
		<?php
	        $conn = mysql_connect('localhost','root','');
	        if ($conn)
	                echo "OK";
	        else
	                echo "NO";
		?>
	~]# systemctl start mariadb  #可测试是否连接mysql	


**方法二：php-fpm管理php进程**
	
	httpd主机：192.168.179.110
		~]# yum install -y httpd
		~]# cat virtualhost.conf 
		<VirtualHost 192.168.179.110:80>
	        DirectoryIndex index.php
	        ServerName www.chuan.com
	        DocumentRoot /data/www/html
	        ProxyRequests off
	        ProxyPassMatch ^/(.*\.php)$ fcgi://192.168.179.111:9000/data/www/html/$1
	        <Directory /data/www/html>
	            Options FollowSymLinks
	            AllowOverride None
	            Require all granted
	        </Directory>
		</VirtualHost>
		~]# systemctl start httpd
	
	php-fpm主机：192.168.179.111
		~]# yum install -y php-fpm php-mbstring php-mysql php-mcrypt
		~]# vim /etc/php-fpm.d/www.conf
			listen = 192.168.179.111:9000
			listen.allowed_clients = 192.168.179.110
		~]# mkdir /data/www/html -pv
	
		#测试
		~]# wget https://files.phpmyadmin.net/phpMyAdmin/4.0.10.20/phpMyAdmin-4.0.10.20-all-languages.tar.gz  
		~]# tar xf phpMyAdmin-4.0.10.20-all-languages.tar.gz -C /data/www/html/
		~]# ln -sv /data/www/html/phpMyAdmin-4.0.10.20-all-languages/ /data/www/html/pma
		~]# cd /data/www/html/pma 
		~]# cp config.sample.inc.php config.inc.php	
		~]# vim config.inc.php
			$cfg['Servers'][$i]['host'] = '192.168.179.113';
	
		~]# mkdir /var/lib/php/session -pv
		~]# chown apache:apache /var/lib/php/session/
		~]# systemctl start php-fpm
	
	mariadb主机：192.168.179.113
		~]# yum install -y mariadb-server
		~]# mysql
			> grant all on *.* to "tom"@"%" identified by "960711";
		~]# systemctl start mariadb
		
	注：skip-name-resolve=ON #mysql 跳过主机名解析，反解  /etc/my.cnf
	
	访问：
		http://192.168.179.110/pma/
	
	注：
		服务配置文件：/etc/php-fpm.conf,/etc/php-fpm.d/*.conf
		php环境配置文件：/etc/php.ini,/etc/php.d/*.ini


# 9.2编译安装

# 10.httpd三种模式参数
**prefork模式：**


	StartServers：初始化创建的子进程数量，默认为5
	ServerLimit：硬控制最大的子进程数量，默认值为256
	MaxSpareServers：最大空闲子进程数量，默认值为10
	MinSpareServers：最小空闲子进程数量，默认值为5
	MaxRequestWorkers：最大允许的并发连接数量，如果某一刻涌进了大量连接请求，超出该指令值的连接请求会暂时放入等待队列中。


**worker模式：**

	StartServers:初始化创建的子进程数量，默认为3
	ThreadsPerChild：每个子进程中的线程数量
	MaxSpareThreads：每个子进程中最大的空闲线程数
	MinSpareThreads：每个子进程中最小的空闲线程数
	MaxRequestWorkers：指定最大允许的并发连接数。
	ServerLimit：自动调节时会创建新子进程，但不能超过该限制
	ThreadLimit：自动调节时会创建新子线程，但也不能超过这指令指定的数量。

**events模式：**