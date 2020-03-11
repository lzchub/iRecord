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