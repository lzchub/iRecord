#1.二进制部署prometheus监控系统
##1.1 Prometheus

	https://prometheus.io/download/

	~]# tar xf prometheus-2.16.0.linux-amd64.tar.gz -C /usr/local/prometheus-2.16.0
	~]# cat /usr/lib/systemd/system/prometheus.service
		[Unit]
		Description=promrtheus
		After=network.target 
		
		[Service]
		ExecStart=/usr/local/prometheus-2.16.0/prometheus --config.file=/usr/local/prometheus-2.16.0/prometheus.yml
		Restart=on-failure
		
		[Install]
		WantedBy=multi-user.target

	~]# systemctl daemon-reload
	~]# systemctl start prometheus		#默认监听9090端口
	~]# systemctl enable prometheus

	~]# cat /etc/profile.d/prometueus.sh 
		PROM_HOME=/usr/local/prometheus-2.16.0/
		PATH=$PATH:$PROM_HOME

	~]# cat prometheus.yml

		# my global config
		global:
		  scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
		  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
		  # scrape_timeout is set to the global default (10s).
		
		# Alertmanager configuration
		alerting:
		  alertmanagers:
		  - static_configs:
		    - targets:
		      # - alertmanager:9093
		
		# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
		# 告警规则
		rule_files:
		  # - "first_rules.yml"
		  # - "second_rules.yml"
		
		# A scrape configuration containing exactly one endpoint to scrape:
		# Here it's Prometheus itself.
		scrape_configs:
		  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
		  - job_name: 'prometheus'
		
		    # metrics_path defaults to '/metrics'
		    # scheme defaults to 'http'.
		
			#主机静态发现
		    static_configs:
		    - targets: ['192.168.100.51:9090']
			  # 给当前配置下的机器定义标签    
			  labels:
	        	apps: node
			# 克隆标签，将原标签克隆并以target标签命名
			relabel_configs:	
			- action: replace
			  source_labels: ['job']
			  regex: (.*)
			  replacement: $1
			  target_labels: idc

			#主机动态发现，动态发现匹配文件写法与上 - targets 相同
			file_sd_configs:
			- files: ['/usr/local/prometheus-2.16.0/sd_config/*.yml']
			  refresh_interval: 5s

	~]# promtool check config prometheus.yml			#检查配置文件语法
	~]# kill -hup PID 	#动态跟新配置

## 1.2 node_exporter

	https://prometheus.io/download/#node_exporter

	~]# tar xf node_exporter-0.18.1.linux-amd64.tar.gz -C /usr/local/
	~]# cd /usr/local/
	~]# mv node_exporter-0.18.1.linux-amd64/ node_exporter-0.18.1
	~]# cd node_exporter-0.18.1

	~]# cat /usr/lib/systemd/system/node_exporter.service 
		[Unit]
		Description=node exporter
		After=network.target 
		
		[Service]
		# 监控Centos7的 systemd 服务
		ExecStart=/usr/local/node_exporter-0.18.1/node_exporter --collector.systemd --collector.systemd.unit-whitelist=(sshd|docker|kubelet).service
		Restart=on-failure
		
		[Install]
		WantedBy=multi-user.target

	~]# systemctl daemon-reload
	~]# systemctl start node_exporter
	~]# systemctl enable node_exporter	

## 1.3 grafana

## 1.4 Alertmanager
	
	https://prometheus.io/download/#node_exporter

	~]# tar xf alertmanager-0.20.0.linux-amd64.tar.gz -C /usr/local/
	~]# cd /usr/local/
 
	~]# mv alertmanager-0.20.0.linux-amd64/ alertmanager-0.20.0
	~]# cd alertmanager-0.20.0

	~]# cat alertmanager.yml 	#配置发送右键告警
		global:
		  resolve_timeout: 5m
		  smtp_smarthost: 'smtp.163.com:25'
		  smtp_from: "youjiangaojing@163.com"
		  smtp_auth_username: 'youjiangaojing@163.com'
		  smtp_auth_password: '1030827997Asd'
		  smtp_require_tls: false
		
		route:
		  group_by: ['alertname']		# 以标签进行分组
		  group_wait: 10s				# 发送告警的延迟时间，用于合并告警
		  group_interval: 10s			# 发送告警的时间间隔
		  repeat_interval: 1m			# 重复告警时间间隔
		  receiver: 'mail'
		
		receivers:
		- name: 'mail'
		  email_configs:
		  - to: 'lzc7970@163.com'
		
		#receivers:
		#- name: 'web.hook'
		#  webhook_configs:
		#  - url: 'http://127.0.0.1:5001/'
		#inhibit_rules:
		#  - source_match:
		#      severity: 'critical'
		#    target_match:
		#      severity: 'warning'
		#    equal: ['alertname', 'dev', 'instance']

	~]# ./amtool check-config alertmanager.yml 

	~]# cat /usr/lib/systemd/system/alertmanager.service 
 
	~]# systemctl daemon-reload
	~]# systemctl start alertmanager
	~]# systemctl status alertmanager


#2.监控不同对象
##2.1 Docker

	https://github.com/google/cadvisor

	# 默认监听8080端口
	~]# docker run  \	
	    --volume=/:/rootfs:ro \
	    --volume=/var/run:/var/run:ro \
	    --volume=/sys:/sys:ro \
	    --volume=/var/lib/docker/:/var/lib/docker:ro \
	    --volume=/dev/disk/:/dev/disk:ro \
		--publish=8080:8080 \
	    --detach=true \
	    --name=cadvisor \
	    registry.cn-hangzhou.aliyuncs.com/quay-image/cadvisor:v0.35.0

##2.2 Kubernetes Pod

	kubelet节点使用cAdvisor提供的metrics接口获取该节点所有容器相关的性能指标数据

	暴露接口地址：
	https://nodeIP:10255/metrics/cadvisor
	https://nodeIP:10250/metrics/cadvisor

	集群资源监控：3119
	资源状态监控：6417
	node监控：9276
 
		