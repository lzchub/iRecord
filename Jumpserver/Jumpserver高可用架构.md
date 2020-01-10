## 实验准备

	Centos 7.6 * 4
		192.168.5.10		MySQL Redis LVS KeepAlived glusterfs
		192.168.5.11		MySQL LVS KeepAlived glusterfs
		192.168.5.15		Nginx（jumpserver + coco + guacamole）
		192.168.5.16		Nginx（jumpserver + coco + guacamole）
	MySQL VIP：192.168.5.100
	MySQL-5.7
	glusterfs-6.5
	redis-3.2

## 架构图
![](./picture/1.png)


## 环境准备

	~]# systemctl stop firewalld
	~]# systemctl disable firewalld
	~]# sed -i 's/SELINUX=enable/SELINUX=disabled/g' /etc/sysconfig/selinux 
	~]# setenforce 0

	~]# cat /etc/hosts
	
	~]# cat /etc/hosts
		...
		192.168.5.10 glusterfs01
		192.168.5.11 glusterfs02

## 1.glusterfs集群搭建

	可通过至少两块盘，或者两个分区

	通过两块盘额外步骤：
	glusterfs01：
		~]# mkfs.xfs /dev/sdb
		~]# mkdir -p /data/jumpserver
		~]# echo '/dev/sdb /data/jumpserver xfs defaults 0 0' >> /etc/fstab
		~]# mount -a && mount

	glusterfs02：
		~]# mkfs.xfs /dev/sdb
		~]# mkdir -p /data/jumpserver
		~]# echo '/dev/sdb /data/jumpserver xfs defaults 0 0' >> /etc/fstab
		~]# mount -a && mount
	
	安装软件（以下操作两节点一致）
		~]# yum install centos-release-gluster -y
		~]# yum install -y glusterfs glusterfs-server glusterfs-fuse glusterfs-rdma
		~]# rpm -q glusterfs
			glusterfs-6.5-1.el7.x86_64

	启动服务
		~]# systemctl start glusterd.service 
		~]# systemctl status glusterd.service 

	配置互信（可信池）
		~]# gluster peer probe glusterfs02		#glusterfs01上操作		
		~]# gluster peer probe glusterfs01		#glusterfs02上操作	

	检查对等状态
		~]# gluster peer status 

	建立一个GlusterFS卷
		~]# mkdir -p /data/jumpserver/g_jump

		~]# gluster volume create g_jump replica 2 glusterfs01:/data/jumpserver/g_jump glusterfs02:/data/jumpserver/g_jump		#任意一个节点执行即可，若有报错，需在最后添加 force 参数（在使用分区做时会发生此错误）

	启用存储卷
		~]# gluster volume start g_jump		#任意一个节点执行即可

	查看信息
		~]# gluster volume info	

#### 客户端测试

	挂载测试（请先做好hosts）
		~]# yum install centos-release-gluster -y
		~]# yum install -y glusterfs glusterfs-fuse

		~]# mount.glusterfs  glusterfs01:/g_jump /opt

		~]# echo "glusterfs01:/g_jump /opt glusterfs defaults 0 0" >> /etc/fstab		#永久生效
	
## KVM搭建

	virt-install --name virt-jumpserver1410 --ram 8192 --vcpus 4 --disk path=/data/vm-image/virt-jumpserver1410.img,size=100 --network bridge=br0 --cdrom /data/iso/CentOS-7-x86_64-DVD-1810.iso --vnclisten=192.168.5.10 --vncport=6901 --vnc


## 2.MySQL数据库主主搭建配置

	~]# yum -y install ncurses-devel cmake gcc gcc-c++ perl*
	~]# perl -v 		#检查perl是否能用，若没有版本信息输出，卸掉后重新yum安装
	~]# cd ~
	~]# tar zxvf mysql-boost-5.7.26.tar.gz -C /usr/src/

	~]# mkdir /data/mysql -p
	~]# useradd -M -s /sbin/nologin mysql
	~]# cd /usr/src/mysql-5.7.26/
	~]# cmake 					\
		-DCMAKE_INSTALL_PREFIX=/data/mysql 	\
		-DMYSQL_DATADIR=/data/mysql/data 	\
		-DSYSCONFDIR=/etc 					\
		-DWITH_MYISAM_STORAGE_ENGINE=1		\
		-DWITH_INNOBASE_STORAGE_ENGINE=1 	\
		-DWITH_MEMORY_STORAGE_ENGINE=1		\
		-DMYSQL_TCP_PORT=3306 				\
		-DMYSQL_USER=mysql 					\
		-DDEFAULT_CHARSET=utf8 				\
		-DDEFAULT_COLLATION=utf8_general_ci \
		-DWITH_BOOST=boost

	~]# make && make install

	~]# cat /etc/profile.d/mysql.sh 
		MYSQL_HOME=/data/mysql
		PATH=$MYSQL_HOME/bin:$PATH
	
	~]# . /etc/profile.d/mysql.sh 
	
	~]# mv /etc/my.cnf /etc/my.cnf.bak
	~]# mysqld --initialize --user=mysql --basedir=/data/mysql --datadir=/data/mysql/data		#记住生成的随机密码		 	
	~]# cp /data/mysql/support-files/mysql.server /etc/init.d/mysqld			

	~]# cat /etc/my.cnf
		[mysqld]
		datadir=/data/mysql/data
		basedir=/data/mysql
		socket=/tmp/mysql.sock

		symbolic-links=0				
			
		[mysqld_safe]
		log-error=/data/mysql/log/error.log
		pid-file=/data/mysql/data/mysql.pid
			
		!includedir /etc/my.cnf.d
 
	~]# mkdir -p /data/mysql/log
	~]# touch /data/mysql/log/error.log
	~]# chown -R mysql:mysql /data/mysql/log    


	~]# service mysqld start	

	~]# mysql -uroot -p		#初始化生成的密码

	mysql> set password=password("www.517la.com");
	mysql> exit

	还需配置
	~]# chkconfig --del mysqld
	~]# chkconfig --add mysqld	

#### MySQL主主配置

**MySQL master：**
	
	~]# cat /etc/my.cnf
		[mysqld]
		datadir=/data/mysql/data
		basedir=/data/mysql
		socket=/tmp/mysql.sock
		
		symbolic-links=0
		
		read_only = 1		#启动都是只读
		
		skip_name_resolve=1
		
		slave_skip_errors = 1062
		
		server_id = 1
		log-bin = /data/mysql/log/binary-log
		relay-log = /data/mysql/log/relay-log
		binlog_format = mixed
		sync_binlog = 1
		auto-increment-increment = 2
		auto-increment-offset = 1
		
		binlog-ignore-db = mysql
		binlog-ignore-db = sys 
		binlog-ignore-db = performance_schema
		binlog-ignore-db = information_schema 
		
		replicate-ignore-db = mysql
		replicate-ignore-db = sys 
		replicate-ignore-db = performance_schema
		replicate-ignore-db = information_schema
		
		gtid_mode=on
		enforce_gtid_consistency=on
		
		[mysqld_safe]
		log-error=/data/mysql/log/error.log
		pid-file=/data/mysql/data/mysql.pid
		
		!includedir /etc/my.cnf.d	
	
	~]# service mysqld restart
	~]# mysql -uroot -p

	mysql> grant replication slave on *.* to 'sync'@'192.168.164.148' identified by 'sync';		#创建同步用户

	~]# yum install -y keepalived
	~]# cat /etc/keepalived/keepalived.conf
		! Configuration File for keepalived
		
		global_defs {
		   router_id node1
		}
		
		vrrp_instance mysql {
		    state BACKUP			#设置为非抢占模式，除了nopreempt参数外，state都要设置为backup
		    interface br0
		    virtual_router_id 51
		    priority 100
		    advert_int 1
		    nopreempt		#不使用抢占模式
		
		    authentication {
		        auth_type PASS
		        auth_pass 517la.com
		    }
		
		    virtual_ipaddress {
		        192.168.5.100
		    }
		
		    notify_master /etc/keepalived/scripts/mysql_master.sh		#切换为master时执行脚本        
		    notify_backup /etc/keepalived/scripts/mysql_backup.sh  		#切换为backup时执行脚本
		}
		
		virtual_server 192.168.5.100 3306 {
		    delay_loop 6
		    #lb_algo rr		centos7一定要注释这两行，我遇到其他机器上能 ping通 192.168.5.100，但是telnet都不通
		    #lb_kind NAT
		    persistence_timeout 50
		    protocol TCP
		
		    real_server 127.0.0.1 3306 {
		        weight 1
		        notify_down /etc/keepalived/scripts/mysql.sh		#检测到down时执行脚本
		
		        TCP_CHECK {
		            connect_timeout 3
		            nb_get_retry 3
		            delay_before_retry 3
		            connect_port 3306		#检测的端口
		       }
		    }
		}
	

**MySQL backup：**

	~]# cat /etc/my.cnf
		[mysqld]
		datadir=/data/mysql/data
		basedir=/data/mysql
		socket=/tmp/mysql.sock
		
		symbolic-links=0
		
		read_only = 1
		
		skip_name_resolve=1
		
		slave_skip_errors = 1062
		
		server_id = 2
		log-bin = /data/mysql/log/binary-log
		relay-log = /data/mysql/log/relay-log
		binlog_format = mixed
		sync_binlog = 1
		auto-increment-increment = 2
		auto-increment-offset = 2
		
		binlog-ignore-db = mysql
		binlog-ignore-db = sys 
		binlog-ignore-db = performance_schema
		binlog-ignore-db = information_schema 
		
		replicate-ignore-db = mysql
		replicate-ignore-db = sys 
		replicate-ignore-db = performance_schema
		replicate-ignore-db = information_schema
		
		gtid_mode=on
		enforce_gtid_consistency=on
		
		[mysqld_safe]
		log-error=/data/mysql/log/error.log
		pid-file=/data/mysql/data/mysql.pid
		
		!includedir /etc/my.cnf.d

	~]# service mysqld restart
	~]# mysql -uroot -p

	mysql> grant replication slave on *.* to 'sync'@'192.168.164.148' identified by 'sync';		#创建同步用户

	~]# yum install -y keepalived
	~]# cat /etc/keepalived/keepalived.conf
		! Configuration File for keepalived

		global_defs {
		   router_id node2
		}
		
		vrrp_instance mysql {
		    state BACKUP
		    interface br0
		    virtual_router_id 51
		    priority 90
		    advert_int 1
		    nopreempt
		
		    authentication {
		        auth_type PASS
		        auth_pass 517la.com
		    }
		
		    virtual_ipaddress {
		        192.168.5.100
		    }
		
		    notify_master /etc/keepalived/scripts/mysql_master.sh        
		    notify_backup /etc/keepalived/scripts/mysql_backup.sh  
		}
		
		virtual_server 192.168.5.100 3306 {
		    delay_loop 6
		    #lb_algo rr
		    #lb_kind NAT
		    persistence_timeout 50
		    protocol TCP
		
		    real_server 127.0.0.1 3306 {
		        weight 1
		        notify_down /etc/keepalived/scripts/mysql.sh
		
		        TCP_CHECK {
		            connect_timeout 3
		            nb_get_retry 3
		            delay_before_retry 3
		            connect_port 3306
		       }
		    }
		}


**使用到的脚本：**

	~]# mkdir /etc/keepalived/scripts
	~]# mkdir /var/log/keepalived
	~]# cd /etc/keepalived/scripts
	~]# cat mysql.sh 
		#!/bin/sh
		
		LOGFILE="/var/log/keepalived/keepalived-mysql-state.log" 
		echo "[KILL]" >> $LOGFILE           
		date >> $LOGFILE  
		
		systemctl restart keepalived

	~]# cat mysql_master.sh 
		#!/bin/bash
		#MYSQLCLI="mysql -uroot -pwww.517la.com -e 'set global read_only=OFF;'"
		
		LOGFILE="/var/log/keepalived/keepalived-mysql-state.log" 
		echo "[master]" >> $LOGFILE
		           date >> $LOGFILE
		echo "Being master...." >> $LOGFILE 2>&1
		echo "set global read_only=OFF; cmd .." >> $LOGFILE
		
		#$MYSQLCLI -e "set global read_only=OFF;" >> $LOGFILE 2>&1   
		#$MYSQLCLI
		
		mysql -S /tmp/mysql.sock -pwww.517la.com -e "set global read_only=OFF;" >>$LOGFILE 2>&1

	~]# cat mysql_backup.sh 
		#!/bin/bash
		#MYSQLCLI="mysql -uroot -pwww.517la.com -e 'set global read_only=ON;'"
		LOGFILE="/var/log/keepalived/keepalived-mysql-state.log" 
		echo "[backup]" >> $LOGFILE
		           date >> $LOGFILE
		echo "Being backup...." >> $LOGFILE 2>&1   
		echo "set global read_only=ON; cmd .." >> $LOGFILE
		
		#$MYSQLCLI -e "set global read_only=ON;" >> $LOGFILE 2>&1
		
		#$MYSQLCLI


**开启同步：**

	master：

		mysql> change master to
			   master_host='192.168.5.11',
		   	   master_port=3306,
		   	   master_auto_position=1;


		mysql> start slave user='sync' password='sync';
	
		mysql> show slave status\G;		#IO 线程与 SQL线程起来即可
		mysql> show processlist;

	backup：

		mysql> change master to
			   master_host='192.168.5.10',
		   	   master_port=3306,
		   	   master_auto_position=1;


		mysql> start slave user='sync' password='sync';
	
		mysql> show slave status\G;		#IO 线程与 SQL线程起来即可
		mysql> show processlist;

## 3.Redis搭建

	由于Redis在这儿是做缓存，所以我只搭了单机，可优化为主从或集群

	~]# wget https://mirrors.aliyun.com/epel/epel-release-latest-7.noarch.rpm	
	~]# rpm -ivh epel-release-latest-7.noarch.rpm
	
	~]# yum -y install redis
	
	~]# vi /etc/redis.conf
		...
		# bind 127.0.0.1  # 注释这行, 新增如下内容
		bind 0.0.0.0
		maxmemory-policy allkeys-lru  # 清理策略, 优先移除最近未使用的key

	~]# systemctl enable redis			#安装 Redis, Jumpserver 使用 Redis 做 cache 和 celery broke
	~]# systemctl start redis		
	~]# ss -tnl
		LISTEN     0      128      *:6379     *:*    

## 4.Jumpserver双机搭建

	~]# yum -y install wget gcc git vim		#安装
	
	~]# wget https://mirrors.aliyun.com/epel/epel-release-latest-7.noarch.rpm	
	~]# rpm -ivh epel-release-latest-7.noarch.rpm

	mysql> create database jumpserver default charset 'utf8';		#在任意一台数据库上即可
	mysql> grant all on jumpserver.* to jumpserver@'192.168.5.%' identified by 'jumpserver';	#由于我们默认没有同步该库，所以两台都需配置，此为jumpserver访问数据库的用户
	mysql> flush privileges;
	
	~]# yum -y install python36 python36-devel	#安装 Python3.6
	~]# cd /opt/
	~]# python3.6 -m venv py3					#配置并载入 Python3 虚拟环境
	~]# source /opt/py3/bin/activate			#进入虚拟环境  deactivete退出虚拟环境,以后起程序需要到虚拟环境

	~]#  cd /opt/
	~]# git clone https://github.com/jumpserver/jumpserver.git	#克隆慢可以先拉到码云在克隆
	~]# cd /opt/jumpserver
	~]# git checkout 1.4.8		#由于挂载的分布式文件系统，只需要一台上克隆安装即可，备机会自动同步

	~]# yum -y install $(cat /opt/jumpserver/requirements/rpm_requirements.txt)		# 安装依赖 RPM 包

	~]# pip install --upgrade pip setuptools					# 安装 Python 库依赖,一台上操作
	~]# pip install -r /opt/jumpserver/requirements/requirements.txt		# 安装Python依赖模块

	~]# cd /opt/jumpserver
	~]# cp config_example.yml config.yml		#一台上操作

	~]# export SECRET_KEY=`cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 50`				#在一台上随机生成，其余机器保持一致
	~]# echo "SECRET_KEY=$SECRET_KEY" >> ~/.bashrc								#在一台上随机生成，其余机器保持一致
	~]# export BOOTSTRAP_TOKEN=`cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 16`			#在一台上随机生成，其余机器保持一致
	~]# echo "BOOTSTRAP_TOKEN=$BOOTSTRAP_TOKEN" >> ~/.bashrc						#在一台上随机生成，其余机器保持一致
	
	~]# sed -i "s/SECRET_KEY:/SECRET_KEY: $SECRET_KEY/g" /opt/jumpserver/config.yml
	~]# sed -i "s/BOOTSTRAP_TOKEN:/BOOTSTRAP_TOKEN: $BOOTSTRAP_TOKEN/g" /opt/jumpserver/config.yml
	~]# sed -i "s/# DEBUG: true/DEBUG: false/g" /opt/jumpserver/config.yml
	~]# sed -i "s/# LOG_LEVEL: DEBUG/LOG_LEVEL: ERROR/g" /opt/jumpserver/config.yml 
	~]# sed -i "s/# SESSION_EXPIRE_AT_BROWSER_CLOSE: false/SESSION_EXPIRE_AT_BROWSER_CLOSE: true/g" /opt/jumpserver/config.yml
	
	~]# cat config.yml | grep -E "DB|REDIS" | grep -v "#"	#查看数据库以及redis信息是否修改正确
		DB_ENGINE: mysql
		DB_HOST: 192.168.5.100
		DB_PORT: 3306
		DB_USER: jumpserver
		DB_PASSWORD: jumpserver
		DB_NAME: jumpserver
		REDIS_HOST: 192.168.5.10
		REDIS_PORT: 6379

	~]# vi /usr/lib/systemd/system/jms.service
		[Unit]
		Description=jms
		After=network.target mariadb.service redis.service docker.service
		Wants=mariadb.service redis.service docker.service
		
		[Service]
		Type=forking
		Environment="PATH=/opt/py3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin"
		ExecStart=/opt/jumpserver/jms start all -d
		ExecReload=
		ExecStop=/opt/jumpserver/jms stop
		
		[Install]
		WantedBy=multi-user.target

	~]# vi /opt/start_jms.sh			#启动

		#!/bin/bash
		set -e
		
		export LANG=zh_CN.UTF-8
		
		systemctl start jms
		docker start jms_coco
		docker start jms_guacamole
		
		exit 0

	~]# vi /opt/stop_jms.sh				#停止

		#!/bin/bash
		set -e
		
		export LANG=zh_CN.UTF-8
		
		docker stop jms_coco
		docker stop jms_guacamole
		systemctl stop jms
		
		exit 0
	
	~]# chmod +x /etc/rc.d/rc.local
	~]# if [ "$(cat /etc/rc.local | grep start_jms.sh)" == "" ]; then echo "sh /opt/start_jms.sh" >> /etc/rc.local; fi

	~]# systemctl start jms			#监听8080端口
	~]# systemctl enable jms  # 配置自启

	~]# cd /etc/yum.repos.d/
	~]# wget https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
	~]# yum install -y docker-ce		# 安装 docker 部署 coco 与 guacamole
	~]# systemctl start docker
	~]# systemctl enable docker

	~]# export Server_IP=`ip addr | grep inet | egrep -v '(127.0.0.1|inet6|docker)' | awk '{print $2}' | tr -d "addr:" | head -n 1 | cut -d / -f1`			#获取宿主机IP
	~]# docker run --name jms_coco -d -p 2222:2222 -p 5000:5000 -e CORE_HOST=http://$Server_IP:8080 -e BOOTSTRAP_TOKEN=$BOOTSTRAP_TOKEN jumpserver/jms_coco:1.4.8			#启动koko容器
	~]# docker run --name jms_guacamole -d -p 8081:8081 -e JUMPSERVER_SERVER=http://$Server_IP:8080 -e BOOTSTRAP_TOKEN=$BOOTSTRAP_TOKEN jumpserver/jms_guacamole:1.4.8		#启动guacamole容器

	~]# docker container ps   #查看容器是否起来
		CONTAINER ID    IMAGE                            COMMAND             CREATED          STATUS        PORTS                                              NAMES
		2a86160707c3    jumpserver/jms_guacamole:1.4.8  "entrypoint.sh"     2 hours ago      Up 2 hours    127.0.0.1:8081->8081/tcp                           jms_guacamole
		d193f7be07d6    jumpserver/jms_koko:1.4.8        "./entrypoint.sh"   2 hours ago      Up 2 hours    0.0.0.0:2222->2222/tcp, 127.0.0.1:5000->5000/tcp   jms_koko

	~]# cd /opt
	~]# wget https://github.com/jumpserver/luna/releases/download/1.4.8/luna.tar.gz		# 安装 Web Terminal 前端: Luna  需要 Nginx 来运行访问 访问(https://github.com/jumpserver/luna/releases)下载对应版本的 release 包, 直接解压, 不需要编译

	# 如果网络有问题导致下载无法完成可以使用下面地址
	#~]# wget https://demo.jumpserver.org/download/luna/1.4.8/luna.tar.gz

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

	自此，我们双机jumpserver就已经搭建完成了，可分别登录两台jumpserver进行测试，在一台上进行写入操作，查看另一台是否进行同步！

## 5.通过LVS负载后端nginx

	jumpserver通过nginx整合了所有web组件，然后我们通过LVS来负载后端两台nginx

	采用LVS nat模式，VIP最好使用虚拟IP绑定在一张网卡上，而不要单独使用一张网卡，这儿通过keepalived创建VIP

	~]# yum install -y keepalived ipvsadm


	~]# cat /etc/keepalived/keepalived.conf		#实例配置，此为master配置，backup只需修改优先级即可
		
		vrrp_instance lvs_nginx {
	    state BACKUP
	    interface br0
	    virtual_router_id 52
	    priority 100
	    advert_int 1
	    nopreempt
	
	    authentication {
	        auth_type PASS
	        auth_pass lvsnginx
	    }
	
	    virtual_ipaddress {
	        192.168.5.20
	    }
	
	    #notify_master /etc/keepalived/scripts/nginx_master.sh        
	    #notify_backup /etc/keepalived/scripts/nginx_backup.sh  
	}

	~]# systemctl start keepalived

	#打开核心转发功能
	~]# echo 1 >/proc/sys/net/ipv4/ip_forward

	~]# ipvsadm -A -t 192.168.5.20:80 -s dh			#采用轮询算法
	~]# ipvsadm -a -t 192.168.5.20:80 -r 192.168.5.15:80 -m		#将后端服务器加入负载组  
	~]# ipvsadm -a -t 192.168.5.20:80 -r 192.168.5.16:80 -m 		
	~]# ipvsadm -ln
		IP Virtual Server version 1.2.1 (size=4096)
		Prot LocalAddress:Port Scheduler Flags
		  -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
		TCP  192.168.5.20:80 dh
		  -> 192.168.5.15:80              Masq    1      0          0         
		  -> 192.168.5.16:80              Masq    1      0          0   

	~]# route add default gw 192.168.5.20		#后端服务器上设置默认网关

	~]# ipvsadm -d -t 192.168.5.20:80 -r 192.168.5.16   #如何剔除后端服务器

	~]# ipvsadm -D -t 192.168.5.20:80

#故障解决

	1.若出现宿主机可以访问网络，但是宿主机上的KVM虚拟机出现网络不通，先看看br0网桥，需要把vnet0连接上br0网桥上
	
	~]# brctl addif br0 vnet0      #网桥一般默认设为br0，将vnet0接口加入网桥

	2.LVS采用nat模式时，若后端设置默认网关为LVS director 的vip时，且后端能ping通vip，则是LVS上的路由转发未打开
	~]# cat /proc/sys/net/ipv4/ip_forward
	0
	~]# echo 1 >/proc/sys/net/ipv4/ip_forward
	
	3.若堡垒机连接不上linux服务器，检查后端coco容器是否正常启动，实在不行，杀掉重启容器
	~]# docker container ps      #查看容器ID
	~]# docker container rm ID   #根据容器ID删除容器
	
	4若堡垒机连接不上windows服务器，检查后端guacamole容器是否正常启动，处理方法同上
	
	5.重启各种服务
	~]# source /opt/py3/bin/activate    #进入Python虚拟环境
	~]#  ./jms start -d              #启动jumpserver  会监听 8080 端口
	~]# systemctl start docker
	~]# docker run --name jms_coco -d -p 2222:2222 -p 5000:5000 -e CORE_HOST=http://$Server_IP:8080 -e BOOTSTRAP_TOKEN=$BOOTSTRAP_TOKEN jumpserver/jms_coco:1.4.8         #启动coco 会监听 2222  5000 端口
	~]# docker run --name jms_guacamole -d -p 8081:8081 -e JUMPSERVER_SERVER=http://$Server_IP:8080 -e BOOTSTRAP_TOKEN=$BOOTSTRAP_TOKEN jumpserver/jms_guacamole:1.4.8     #启动guacamole 会监听8081 端口
	~]# systemcat start nginx          #启动nginx 会监听80端口
	
	
	注：以上重启容器以及jumpserver的服务，需在 Python虚拟环境 下进行

	

	      

	

	

	

	