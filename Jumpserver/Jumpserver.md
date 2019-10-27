# 基础环境：
	系统：CentOS 7.6
	目录：/opt
	数据库：Mariadb
	缓存：Redis
	代理：Nginx

# Jumpserver安装

	~]# systemctl stop firewalld 
	~]# systemctl disable firewalld
	~]# setenforce 0
	~]# sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/sysconfig/selinux  

	~]# yum -y install wget gcc git vim		#安装
	
	~]# wget https://mirrors.aliyun.com/epel/epel-release-latest-7.noarch.rpm	
	~]# rpm -ivh epel-release-latest-7.noarch.rpm
	
	
	~]# yum -y install redis
	~]# systemctl enable redis			#安装 Redis, Jumpserver 使用 Redis 做 cache 和 celery broke
	~]# systemctl start redis		
	~]# ss -tnl
		LISTEN     0      128      127.0.0.1:6379     *:*    

	
	~]# yum -y install mariadb mariadb-devel mariadb-server MariaDB-shared		#安装 MySQL, 如果不使用 Mysql 可以跳过相关 Mysql 安装和配置, 支持sqlite3, mysql, postgres等
	~]# systemctl enable mariadb
	~]# systemctl start mariadb
	~]# mysql
	mysql> set password=password("517na.com");
	mysql> create database jumpserver default charset 'utf8';
	mysql> grant all on jumpserver.* to jumpserver@localhost identified by 'jumpserver';
	mysql> flush privileges;

	~]# yum -y install python36 python36-devel	#安装 Python3.6
	~]# cd /opt/
	~]# python3.6 -m venv py3				#配置并载入 Python3 虚拟环境
	~]# source /opt/py3/bin/activate				#进入虚拟环境  deactivete退出虚拟环境

	~]# git clone --depth=1 https://github.com/jumpserver/jumpserver.git	
	~]# yum -y install $(cat /opt/jumpserver/requirements/rpm_requirements.txt)		# 安装依赖 RPM 包

	~]# pip install --upgrade pip setuptools									# 安装 Python 库依赖
	~]# pip install -r /opt/jumpserver/requirements/requirements.txt
	~]# cd /opt/jumpserver
	~]# cp config_example.yml config.yml

	~]# SECRET_KEY=`cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 50`
	~]# BOOTSTRAP_TOKEN=`cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 16`
	~]# echo "BOOTSTRAP_TOKEN=$BOOTSTRAP_TOKEN" >> ~/.bashrc

	~]# sed -i "s/SECRET_KEY:/SECRET_KEY: $SECRET_KEY/g" /opt/jumpserver/config.yml
	~]# sed -i "s/BOOTSTRAP_TOKEN:/BOOTSTRAP_TOKEN: $BOOTSTRAP_TOKEN/g" /opt/jumpserver/config.yml
	~]# sed -i "s/# DEBUG: true/DEBUG: false/g" /opt/jumpserver/config.yml
	~]# sed -i "s/# LOG_LEVEL: DEBUG/LOG_LEVEL: ERROR/g" /opt/jumpserver/config.yml 
	~]# sed -i "s/# SESSION_EXPIRE_AT_BROWSER_CLOSE: false/SESSION_EXPIRE_AT_BROWSER_CLOSE: true/g" /opt/jumpserver/config.yml
	~]# sed -i "s/DB_PASSWORD: /DB_PASSWORD: 517na.com/g" /opt/jumpserver/config.yml	#数据库不在本机需要修改数据库IP等等

	#~]# ./jms start -d	#启动服务 

	~]# wget -O /usr/lib/systemd/system/jms.service https://demo.jumpserver.org/download/shell/centos/jms.service
	~]# chmod 755 /usr/lib/systemd/system/jms.service
	~]# systemctl start jms			#监听8080端口
	~]# systemctl enable jms  # 配置自启

	
	~]# cd /etc/yum.repos.d/
	~]# wget https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
	~]# yum install -y docker-ce		# 安装 docker 部署 coco 与 guacamole
	~]# systemctl start docker
	~]# systemctl enable docker

	~]# Server_IP=`ip addr | grep inet | egrep -v '(127.0.0.1|inet6|docker)' | awk '{print $2}' | tr -d "addr:" | head -n 1 | cut -d / -f1`			#获取宿主机IP
	~]# docker run --name jms_koko -d -p 2222:2222 -p 127.0.0.1:5000:5000 -e CORE_HOST=http://$Server_IP:8080 -e BOOTSTRAP_TOKEN=$BOOTSTRAP_TOKEN --restart=always jumpserver/jms_koko:1.5.2			#启动koko容器
	~]# docker run --name jms_guacamole -d -p 127.0.0.1:8081:8081 -e JUMPSERVER_SERVER=http://$Server_IP:8080 -e BOOTSTRAP_TOKEN=$BOOTSTRAP_TOKEN --restart=always jumpserver/jms_guacamole:1.5.2		#启动guacamole容器
	~]# docker ps
		CONTAINER ID    IMAGE                            COMMAND             CREATED          STATUS        PORTS                                              NAMES
		2a86160707c3    jumpserver/jms_guacamole:1.5.2   "entrypoint.sh"     2 hours ago      Up 2 hours    127.0.0.1:8081->8081/tcp                           jms_guacamole
		d193f7be07d6    jumpserver/jms_koko:1.5.2        "./entrypoint.sh"   2 hours ago      Up 2 hours    0.0.0.0:2222->2222/tcp, 127.0.0.1:5000->5000/tcp   jms_koko

	~]# cd /opt
	~]# wget https://github.com/jumpserver/luna/releases/download/1.5.2/luna.tar.gz		# 安装 Web Terminal 前端: Luna  需要 Nginx 来运行访问 访问(https://github.com/jumpserver/luna/releases)下载对应版本的 release 包, 直接解压, 不需要编译

	# 如果网络有问题导致下载无法完成可以使用下面地址
	#~]# wget https://demo.jumpserver.org/download/luna/1.5.2/luna.tar.gz

	~]# tar xf luna.tar.gz
	~]# chown -R root:root luna

	# 配置 Nginx 整合各组件
	~]# cat /etc/yum.repo.d/nginx.repo 
		[nginx]
		name=nginx repo
		baseurl=http://nginx.org/packages/centos/7/$basearch/
		gpgcheck=0
		enabled=1
			
	~]# yum -y install nginx

	~]# rm -f /etc/nginx/conf.d/default.conf 
	~]# cat /etc/nginx/conf.d/jumpserver.conf
		server {
		    listen 80;
		
		    client_max_body_size 100m;  # 录像及文件上传大小限制
		
		    location /luna/ {
		        try_files $uri / /index.html;
		        alias /opt/luna/;  # luna 路径, 如果修改安装目录, 此处需要修改
		    }
		
		    location /media/ {
		        add_header Content-Encoding gzip;
		        root /opt/jumpserver/data/;  # 录像位置, 如果修改安装目录, 此处需要修改
		    }
		
		    location /static/ {
		        root /opt/jumpserver/data/;  # 静态资源, 如果修改安装目录, 此处需要修改
		    }
		
		    location /socket.io/ {
		        proxy_pass       http://localhost:5000/socket.io/;
		        proxy_buffering off;
		        proxy_http_version 1.1;
		        proxy_set_header Upgrade $http_upgrade;
		        proxy_set_header Connection "upgrade";
		        proxy_set_header X-Real-IP $remote_addr;
		        proxy_set_header Host $host;
		        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		        access_log off;
		    }
		
		    location /coco/ {
		        proxy_pass       http://localhost:5000/coco/;
		        proxy_set_header X-Real-IP $remote_addr;
		        proxy_set_header Host $host;
		        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		        access_log off;
		    }
		
		    location /guacamole/ {
		        proxy_pass       http://localhost:8081/;
		        proxy_buffering off;
		        proxy_http_version 1.1;
		        proxy_set_header Upgrade $http_upgrade;
		        proxy_set_header Connection $http_connection;
		        proxy_set_header X-Real-IP $remote_addr;
		        proxy_set_header Host $host;
		        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		        access_log off;
		    }
		
		    location / {
		        proxy_pass http://localhost:8080;
		        proxy_set_header X-Real-IP $remote_addr;
		        proxy_set_header Host $host;
		        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		    }
		}

	~]# systemctl start nginx
	~]# systemctl enable nginx

	访问 http://IP 
	初始账号：admin
	初始密码：admin
	