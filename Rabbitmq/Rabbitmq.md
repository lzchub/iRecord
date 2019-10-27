## 1.搭建rabbitmq集群

[rabbit下载](https://www.rabbitmq.com/install-rpm.html)

[socat下载](http://www.rpmfind.net/linux/rpm2html/search.php?query=socat(x86-64))

[erlang下载](https://packagecloud.io/rabbitmq/erlang/packages/el/7/erlang-20.3.8.9-1.el7.centos.x86_64.rpm)

## 实验准备

	~]# systemctl stop firewalld
	~]# systemctl disable firewalld

	~]# sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/sysconfig/selinux
	~]# setenforce 0

#### 共用步骤

	~]# cat /etc/hosts		#分发到集群三台服务器上
		...
		192.168.164.165 rabbitmq-node1
		192.168.164.166 rabbitmq-node2
		192.168.164.167 rabbitmq-node3

	~]# rpm -ivh erlang-20.3.8.9-1.el7.centos.x86_64.rpm 
	~]# rpm -ivh rabbitmq-server-3.7.17-1.el7.noarch.rpm 
	~]# rpm -ivh socat-1.7.3.2-2.el7.x86_64.rpm

	~]# erl			#测试erlang环境

	~]# systemctl start rabbitmq-server 	#开启rabbitmq
	
#### rabbitmq-node1 

	~]# ll -a /var/lib/rabbitmq/				#rabbitmq集群中需要公用一个cookie文件，rpm安装默认在/var/lib/rabbitmq下

	~]# scp /var/lib/rabbitmq/.erlang.cookie rabbitmq-node2:/var/lib/rabbitmq/		#将node1上的cookie文件拷贝到node2、node3	
	~]# scp /var/lib/rabbitmq/.erlang.cookie rabbitmq-node2:/var/lib/rabbitmq/

	~]# systemctl rabbitmq-server start 			#启动服务

	~]# rabbitmqctl add_user admin admin						#创建远程管理用户	账号：admin 密码：admin
	~]# rabbitmqctl set_user_tags admin adminstrator			#标记为管理员
	~]# rabbitmqctl set_permissions -p "/" admin ".*" ".*" ".*"		#授予权限
	~]# rabbitmqctl list_permissions -p /						#查看所有账户权限
	~]# rabbitmqctl list_users									#列出所用用户

	#~]# rabbitmqctl  change_password  Username  Newpassword	#修改账户密码
	#~]# rabbitmqctl  clear_permissions  [-p VHostPath]  User	#清除账号的权限信息

	~]# rabbitmqctl delete_user guest							#删除默认用户，默认不能远程登录

	~]#	rabbitmq-plugins enable rabbitmq_management				#开启管理插件 http://IP:15672	访问
	
#### rabbitmq-node2/rabbitmq-node3
	
	~]# systemctl rabbitmq-server start							#启动服务
	
	~]# rabbitmqctl stop_app									#加入集群				
    ~]# rabbitmqctl join_cluster rabbit@rabbitmq-cluster-node1
    ~]# rabbitmqctl start_app

	~]#	rabbitmq-plugins enable rabbitmq_management				#开启管理插件

#### 修改配置（3节点都需配置）

**<font color=RED>修改配置文件：</font>**
	
	~]# cat /etc/rabbitmq/rabbitmq.config 			#修改配置，采用json格式，默认没有该文件需创建
		[
		{rabbit,[
		         {tcp_listeners,[5672]},							#mq默认监听端口
		         {loopback_user,["admin"]},							#允许远程登录
		         {vm_memory_high_watermark,0.80},					#使用 0.8*总内存，最大使用内存12G，erlang开始GC
				 {set_vm_memory_high_watermark_paging_ratio,1},		#默认0.5，1表示不写入磁盘 当 (0.8*总内存*1)，队列开始将消息导出到光盘来释放内存的高水位限制的值
		         {disk_free_limit,"20GB"}							#当磁盘剩余20G时阻止生产者发送消息
		        ]
		}
		].
	
**<font color=RED>修改环境配置文件：</font>**

	~]# mkdir /opt/rabbitmq/{data,log} -p			#创建数据、日志目录
	~]# chown -R rabbitmq:rabbitmq rabbitmq

	~]# cat /etc/tabbitmq/rabbitmq-env.conf			#环境配置文件
		RABBIRMQ_MNESIA_BASE=/opt/rabbitmq/data		#数据文件
		RABBITMQ_LOG_BASE=/opt/rabbitmq/log			#日志文件

#### 剔除节点

	~]# rabbitmqctl stop_app		#剔除节点
	~]# rabbitmqctl reset 
	~]# rabbitmqctl start_app

#### 常用操作

	~]# rabbitmqctl cluster_status	#查看集群信息
		Cluster status of node rabbit@rabbitmq-node1 ...
		[{nodes,[{disc,['rabbit@rabbitmq-node1','rabbit@rabbitmq-node2',
		                'rabbit@rabbitmq-node3']}]},
		 {running_nodes,['rabbit@rabbitmq-node3','rabbit@rabbitmq-node2',
		                 'rabbit@rabbitmq-node1']},
		 {cluster_name,<<"rabbit@rabbitmq-node1">>},
		 {partitions,[]},
		 {alarms,[{'rabbit@rabbitmq-node3',[]},
		          {'rabbit@rabbitmq-node2',[]},
		          {'rabbit@rabbitmq-node1',[]}]}]
		

## 2.使用haproxy负载rabbitmq