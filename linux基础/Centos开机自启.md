# CentOS 7 开机自启

	1.写成 centos6 的 service 服务
		
	~]# ll /etc/init.d/mysqld			#文件放到此目录下，且具有执行权限
	~]# chmad a+x mysqld

	~]# chkconfig --list

	~]# chkconfig --add mysqld
	~]# chkconfig mysqld on

	2.写成 centos7 的 Systemd 服务
	
	~]# ll /usr/lib/systemd/system/mysqld

	~]# systemctl enable mysqld

	~]# systemctl is-enabled mysqld


	3.写入rc.local

	~]# cat /etc/rc.d/rc.local

	~]# chmod a+x /etc/rc.d/rc.local

	~]# echo "/app/tomcat/start.sh"		#把自启命令写入即可

	~]# su - tomcat -c "/app/tomcat/start.sh"	#自启默认会用root，若需要其他用户启动可使用此命令 



