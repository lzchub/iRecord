## 实验环境： ##

	CentOS 7.6
		node1：192.168.164.150
		node2：192.168.164.151
		node3：192.168.164.152
	JDK-1.8.0
	
	elasticsearch-6.3.0
	kibana-6.3.0
	logstash-6.3.0

## 架构图 ##

![](./picture/29.png)

# 初始化准备 #

**1.按需关闭防火墙、SELinux**
	
	~]# systemctl stop firewalld
	~]# systemctl disable firewalld
	~]# setenforce 0
	~]# sed -i '/SELINUX/s/enforcing/disabled/g' /etc/sysconfig/selinux

**2.同步系统时间**
		
	1.安装ntpdate工具
	~]# yum -y install ntp ntpdate
			
	2.设置系统时间与网络时间同步
	~]# ntpdate cn.pool.ntp.org
			
	3.将系统时间写入硬件时间
	~]# hwclock --systohc

**3.修改host**

	~]# cat /etc/hosts
	...
	192.168.179.110 node1
	192.168.179.111 node2
	192.168.179.113 node3

#1.安装JDK 8
[https://www.oracle.com/technetwork/java/javase/downloads/java-archive-javase8-2177648.html](https://www.oracle.com/technetwork/java/javase/downloads/java-archive-javase8-2177648.html)

	~]# yum install jdk-8u202-linux-x64.rpm -y
	~]# echo "JAVA_HOME=/usr/java/latest" > /etc/profile.d/jdk.sh
    ~]# echo "PATH=$JAVA_HOME/bin:$PATH" >> /etc/profile.d/jdk.sh
    ~]# source /etc/profile.d/jdk.sh
    ~]# java -version
	java version "1.8.0_202"
	Java(TM) SE Runtime Environment (build 1.8.0_202-b08)
	Java HotSpot(TM) 64-Bit Server VM (build 25.202-b08, mixed mode)


#2.elasticsearch集群搭建

	~]# rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch

	~]# cat /etc/yum.repos.d/elk.repo 
		[ELK-6.x]
		name=ELK repository for 6.x packages
		baseurl=https://artifacts.elastic.co/packages/6.x/yum
		gpgcheck=1
		gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
		enabled=1
		autorefresh=1
		type=rpm-md

	9200端口：数据端口
	9300端口：集群端口

    ~]# yum install -y elasticsearch-6.3.0
	~]# grep ^[^#] /etc/elasticsearch/elasticsearch.yml 
		cluster.name: myes			#集群名称，一定要一致，当集群内节点启动的时候，默认使用组播（多播），寻找集群中的节点
		node.name: node1											#节点名称
		path.data: /els/data										#数据目录,一般需较大磁盘		
		path.logs: /els/log											#日志目录
		#bootstrap.memory_lock: true									#服务启动是锁定内存
		network.host: 192.168.164.150								#本机IP
		http.port: 9200												#开放端口
		discovery.zen.ping.unicast.hosts: ["node2", "node3"]		#集群中其他成员
		discovery.zen.minimum_master_nodes: 2						#成为master
	~]# vim jvm.options 
		-Xms1g	#初始化使用堆内存
		-Xmx1g	#最大使用堆内存

	~]# mkdir /els/{data,log} -pv
	~]# chown -R elasticsearch.elasticsearch /els

	~]# vim /etc/sysctl.conf										#调整系统虚拟内存
		vm.max_map_count=262144
	~]# sysctl -p

	~]# vim /etc/security/limits.conf 								#修改tcp连接数 #锁定内存
	~]# tail -n 2 /etc/security/limits.conf
		* soft nofile 65536
		* hard nofile 65536
		* soft memlock unlimited 									
		* hard memlock unlimited 

    ~]# systemctl start elasticsearch

	~]# curl -XGET http://node1:9200/_cat/nodes

	注：scp的配置文件注意权限问题

#3.elasticsearch-head搭建

	9100端口

	elasticsearch-head简介：
		1.ElasticSearch-head是一个H5编写的ElasticSearch集群操作和管理工具，可以对集群进行傻瓜式操作。
		2.显示集群的拓扑,并且能够执行索引和节点级别操作
		3.搜索接口能够查询集群中原始json或表格格式的检索数据
		4.能够快速访问并显示集群的状态
		5.有一个输入窗口,允许任意调用RESTful API。这个接口包含几个选项,可以组合在一起以产生有趣的结果
		6.es的图形界面插件，托管于GitHub,使用9100端口

	安装NodeJS，root用户
		~]# wget https://nodejs.org/dist/v8.11.3/node-v8.11.3-linux-x64.tar.gz
		~]# tar xf node-v8.11.3-linux-x64.tar.gz -C /usr/src/
		~]# cd /usr/local/
		~]# ln -sv /usr/src/node-v8.11.3-linux-x64/ node
		~]# ln -sv /usr/local/node/bin/node /usr/local/bin/node
		~]# ln -sv /usr/local/node/bin/npm /usr/local/bin/npm
		~]# yum install -y git
		~]# cd ~
		~]# git clone git://github.com/mobz/elasticsearch-head.git
		~]# cd elasticsearch-head/
		~]# npm install
		~]# nohup npm run start &

	注：以上方法会有一些报错，但仍可使用

	~]# vim /etc/elasticsearch/elasticsearch.yml
		http.cors.enabled: true
		http.cors.allow-origin: "*"
	~]# systemctl restart elasticsearch  

	http://localhost:9100/

	docker安装：
	~]# yum install docker -y
	~]# systemctl start docker && systemctl enable docker
	# docker load < /usr/local/src/elasticsearch-head-docker.tar.gz
	~]# docker run -d -p 9100:9100 docker.io/mobz/elasticsearch-head:5
	~]# docker images	
	~]# docker run -d -p 9100:9100 mobz/elasticsearch-head:5
	
	~]# vim /etc/elasticsearch/elasticsearch.yml
		http.cors.enabled: true
		http.cors.allow-origin: "*"
	~]# systemctl restart elasticsearch  

#4.kibana安装

	5601端口

	~]# yum install -y kibana-6.3.0-x86_64.rpm
	~]# grep ^[^#] /etc/kibana/kibana.yml   
		server.port: 5601
		server.host: "192.168.179.150"
		server.name: "node1.kibana"
		elasticsearch.url: "http://192.168.179.150:9200"
	~]# systemctl start kibana
		
#5.filebeat安装

	beats:
		1.Packetbeat（搜集网络流量数据）
		2.Metricbeat（搜集系统、进程和文件系统级别的 CPU 和内存使用情况等数据。通过从操作系统和服务收集指标，帮助您监控服务器及其托管的服务。）
		3.Filebeat（搜集文件数据）
		4.Winlogbeat（搜集 Windows 事件日志数据）

	无监听端口

	~]# yum install filebeat-6.3.0 -y
	~]# vim /etc/filebeat/filebeat.yml
	
		#采集数据文件
		- input_type: log
		  paths:
	    	- /var/log/nginx/access.log
	
		#输出给es
		output.elasticsearch:
		  hosts: ["es-node:9200"]
	
		#输出给logstash
		output.logstash:
		  hosts: ["logstash-node:5044"]
	
		#输出给redis（最好关闭redis持久化）
		output.redis:
		  hosts: ["redis-node"]
		  password: "chuan"
		  key: "filebeat"
		  db: 5
		  timeout: 5

		#输出给kafka
		output.kafka:
	  	  hosts: ["kafka1:9092","kafka2:9092","kafka3:9092"]
	  	  topic: nginx-messages
	  	  keep_alive: 10s

	注：若要注释，需全部注释，否则会出错。如：
	#output.elasticsearch:
  	  #hosts: ["node1:9200"]
	注：若在一台服务器上收集多个日志，需在每个input后面定义document_type: xxxxxx，用于在logstash中判断写入哪个索引

#6.logstash安装

	9600端口

	~]# yum install -y logstash-6.3.0



**redis->logstash->elasticsearch:**

	~]# vim /etc/filebeat/conf.d/test.conf

	input {
	    redis {
	        data_type => "list"
	        key => "filebeat"
	        password => "chuan"
	        db => 5
	    }
	}
	
	filter {
	    grok {
	        match => {
	            "message" => "%{IPORHOST:clientip} %{HTTPDUSER:ident} %{USER:auth} \[%{HTTPDATE:datetime}\] \"%{WORD:verb} %{URIPATHPARAM:request} HTTP/%{NUMBER:httpversion}\" %{NUMBER:http_status_code} %{NUMBER:bytes} \"(?<http_referer>\S+)\" \"(?<http_user_agent>\S+)\" \"(?<http_x_forwarded_for>\S+)\""
	                }
	        }
	}
	
	output {
	#    elasticsearch {
	#       hosts => ["192.168.179.110:9200","192.168.179.111:9200"]
	#       index => "logstash-ngxlog-%{+YYYY.MM.dd}"
	#    }
	
	    stdout {
	        codec => rubydebug
	    }
	}


	//注：需要在logstash用户下测试该配置，logstash默认为不可登陆用户
	~]# usermod -s /bin/bash logstash
	~]# su - logstash
	~]# /usr/share/logstash/bin/logstash  -f /etc/logstash/conf.d/test.conf 

#7.redis集群搭建

#8.nginx负载kibana

	配置代理：nginx

	server {
		listen 80;
		server_name kibana.test.com
		location / {
			proxy_pass http://127.0.0.1:5601
			proxy_http_version 1.1;
			proxy_set_header Upgrade $http_upgrade;
			proxy_set header Connection 'upgrade';
			proxy_set_header Host $host;
			proxy_cache_bypass $http_upgrade;
		}
	}

#收集nginx日志

	    input {
            beats {
                port => "5244"
            }
        }
        
        filter {
          	grok {
                match => {  "message" => "%{IPORHOST:clientip}  %{NOTSPACE:remote_user} \[%{HTTPDATE:logtimestamp}\] %{IPORHOST:hostname}%{NOTSPACE:request} %{WORD:verb} %{WORD:sendbytes} %{NUMBER:responseTime} %{NOTSPACE:referer} %{QS:serverIpPort} %{QS:serverCacheStatus} %{QS:useragent}" }
            }
        
          	date {
                match => [ "logtimestamp" , "dd/MMM/YYYY:HH:mm:ss Z" ]
                target => "@timestamp"
                "locale" => "cn"
            }
        
         	mutate {
                convert => [ "verb" , "integer" ]
                convert => [ "sendbytes" , "integer" ]
                convert => [ "responseTime" , "float" ]
            }
        
            urldecode { all_fields => true }
        }
        
        output {
            elasticsearch {
                hosts => ["172.21.51.31:9200"]
                manage_template => true
                index => "517la-nginx-access-%{+YYYY-MM-dd}"
           }
        }