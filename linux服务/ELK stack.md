#1.ELK Stack
以下实验均使用5.5.1版本
##1.1 elasticsearch集群搭建
	~]# cat /etc/hosts
		...
		192.168.179.110 node1
		192.168.179.111 node2
		192.168.179.113 node3

	9200端口：数据端口
	9300端口：集群端口

	~]# yum install -y java-1.8.0-openjdk
    ~]# rpm -ivh elasticsearch-5.5.1.rpm
	~]# grep ^[^#] /etc/elasticsearch/elasticsearch.yml 
		cluster.name: myels
		node.name: node3
		path.data: /els/data
		path.logs: /els/logs
		network.host: 192.168.179.113
		http.port: 9200
		discovery.zen.ping.unicast.hosts: ["node1", "node2", "node3"]
		discovery.zen.minimum_master_nodes: 2 
	~]# vim jvm.options 
		-Xms1g	#初始化使用堆内存
		-Xmx1g	#最大使用堆内存
	~]# mkdir /els/{data,logs} -pv
	~]# chown -R elasticsearch.elasticsearch /els
    ~]# systemctl restart elasticsearch

	~]# curl -XGET http://node1:9200/_cat/nodes

	注：scp的配置文件注意权限问题



###1.2 elasticsearch-head搭建

	9100端口
	
	elasticsearch-head 	es的图形界面插件，托管于GitHub

	安装npm：
	~]# wget https://nodejs.org/dist/v6.9.5/node-v6.9.5-linux-x64.tar.xz
	~]# tar -xvf node-v6.9.5-linux-x64.tar.xz
	~]# mv node-v6.9.5-linux-x64 /usr/local/node
	~]# ln -s /usr/local/node/bin/node /usr/local/bin/node
	~]# ln -s /usr/local/node/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm	


	~]# git clone git://github.com/mobz/elasticsearch-head.git
	~]# cd elasticsearch-head
	~]# /usr/local/bin/npm install
	~]# nohup npm run start &	

	~]# vim /etc/elasticsearch/elasticsearch.yml
		http.cors.enabled: true
		http.cors.allow-origin: "*"
	~]# systemctl restart elasticsearch  

	http://localhost:9100/

	注：以上方法会有一些报错，但仍可使用

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

#1.3 kibana安装

	5601端口

	~]# rpm -ivh kibana-5.5.1-x86_64.rpm
	~]# grep ^[^#] /etc/kibana/kibana.yml   
		server.port: 5601
		server.host: "192.168.179.110"
		server.name: "node1.kibana"
		elasticsearch.url: "http://192.168.179.110:9200"
	~]# systemctl restart kibana


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
		
#1.4 filebeat安装

	无监听端口

	~]# rpm -ivh filebeat-5.5.1-x86_64.rpm
	~]# vim /etc/filebeat/filebeat.yml
	
	#采集数据文件
	- input_type: log
	  paths:
    	- /var/log/nginx/access.log

	#输出给es
	output.elasticsearch:
	  hosts: ["node1:9200"]

	#输出给logstash
	output.logstash:
	  hosts: ["node3:5044"]

	#输出给redis（最好关闭redis持久化）
	output.redis:
	  hosts: ["localhost"]
	  password: "chuan"
	  key: "filebeat"
	  db: 5
	  timeout: 5

	注：若要注释，需全部注释，否则会出错。如：
	#output.elasticsearch:
  	  #hosts: ["node1:9200"]
	注：若在一台服务器上收集多个日志，需在每个input后面定义document_type: xxxxxx，用于在logstash中判断写入哪个索引

#1.5 logstash安装

	9600端口

	~]# yum install -y java-1.8.0-openjdk
	~]# rpm -ivh logstash-5.5.1.rpm

	~]# vim /etc/filebeat/conf.d/test.conf

	input {
	#    beats {
	#       host => "0.0.0.0"
	#       port => 5044
	#    }
	
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
