# 1.搭建rabbitmq集群

[rabbitmq下载](https://www.rabbitmq.com/install-rpm.html)

[socat下载](http://www.rpmfind.net/linux/rpm2html/search.php?query=socat(x86-64))

[erlang下载](https://packagecloud.io/rabbitmq/erlang/packages/el/7/erlang-20.3.8.9-1.el7.centos.x86_64.rpm)

**实验准备：**

	~]# systemctl stop firewalld
	~]# systemctl disable firewalld
	
	~]# sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/sysconfig/selinux
	~]# setenforce 0

**共用步骤：**

	~]# cat /etc/hosts		#分发到集群三台服务器上
		...
		192.168.164.165 rabbitmq-node1
		192.168.164.166 rabbitmq-node2
		192.168.164.167 rabbitmq-node3
		
	~] 修改主机名
		
	https://github.com/rabbitmq/erlang-rpm/releases/tag/v21.2.3/erlang-21.2.3-1.el7
	~]# rpm -ivh erlang-20.3.8.9-1.el7.centos.x86_64.rpm 
	
	https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.7.28/rabbitmq-server-3.7.28-1.el7.noarch.rpm
	~]# rpm -ivh rabbitmq-server-3.7.17-1.el7.noarch.rpm 
	~]# rpm -ivh socat-1.7.3.2-2.el7.x86_64.rpm

	~]# erl			#测试erlang环境
	
	~]# systemctl start rabbitmq-server 	#开启rabbitmq
	~]# systemctl enable rabbitmq-server 

**rabbitmq-node1: master** 

	~]# ll -a /var/lib/rabbitmq/		#rabbitmq集群中需要公用一个cookie文件，rpm安装默认在/var/lib/rabbitmq下
	
	~]# scp /var/lib/rabbitmq/.erlang.cookie rabbitmq-node2:/var/lib/rabbitmq/	 #将node1上的cookie文件拷贝到node2、node3	
	~]# scp /var/lib/rabbitmq/.erlang.cookie rabbitmq-node3:/var/lib/rabbitmq/
	
	~]# systemctl rabbitmq-server start 			#启动服务
	
	~]# rabbitmqctl add_user admin admin						#创建远程管理用户	账号：admin 密码：admin
	~]# rabbitmqctl set_user_tags admin administrator			#标记为管理员
	~]# rabbitmqctl set_permissions -p "/" admin ".*" ".*" ".*"		#授予权限
	~]# rabbitmqctl list_permissions -p /						#查看所有账户权限
	~]# rabbitmqctl list_users									#列出所用用户
	
	#~]# rabbitmqctl  change_password  Username  Newpassword	#修改账户密码
	#~]# rabbitmqctl  clear_permissions  [-p VHostPath]  User	#清除账号的权限信息
	
	~]# rabbitmqctl delete_user guest							#删除默认用户，默认不能远程登录
	
	~]#	rabbitmq-plugins enable rabbitmq_management				#开启管理插件 http://IP:15672	访问

**rabbitmq-node2/rabbitmq-node3**

	~]# systemctl rabbitmq-server start							#启动服务
	
	~]# rabbitmqctl stop_app									#加入集群				
	~]# rabbitmqctl join_cluster rabbit@rabbitmq-node1
	~]# rabbitmqctl start_app
	
	~]#	rabbitmq-plugins enable rabbitmq_management				#开启管理插件

**修改配置（3节点都需配置）**

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
		RABBITMQ_MNESIA_BASE=/opt/rabbitmq/data		#数据文件,修改配置文件后，需重新加入集群且新建用户
		RABBITMQ_LOG_BASE=/opt/rabbitmq/log			#日志文件

**剔除节点**

**软删除：**

	~]# rabbitmqctl stop_app		#需要下线的节点
	~]# rabbitmqctl reset 
	~]# rabbitmqctl start_app

**硬删除：**

```c
~]# rabbitmqctl forget_cluster_node rabbit@rabbitmq-node2
```

# 2.常用操作

## 1.查看集群状态

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
	
	
	
	
	
	
	~]# rabbitmqctl  list_channels consumer_count
	~]# rabbitmqctl  list_channels consumer_count | wc
	
	 rabbitmqctl list_queues | wc
	 rabbitmqctl list_connections | wc
	 rabbitmqctl list_channels|wc 
	 rabbitmqctl list_exchanges | wc
	 rabbitmqctl status

## 2.用户管理

```c
~]# rabbitmqctl add_user {userName} {passWord} # 创建用户
~]# rabbitmqctl change_password {userName} {newPassword} # 修改密码
~]# rabbitmqctl clear_password {userName} # 清除用户密码
~]# rabbitmqctl authentiçate_user {userName} {passWord} # 验证用户
~]# rabbitmqctl delete_user {userName} # 删除用户
~]# rabbitmqctl llist_users # 罗列当前所有用户，和用户角色
~]# rabbitmqctl set_user_tags {userName} {tag ...} # 给用户设置角色，tag 参数用于设置 0个、1个或者多个的角色，设置之后任何之前现有的身份都会被删除。
    
    用户角色分为5中类型：
    none： 无任何角色。新创建的用户的角色默认为 none。
    management：可以访问web管理页面。
    policymaker：包含managerment的所有权限，并且可以管理策略(Policy)和参数(Parameter)。
    monitoring：包含management的所有权限，并且可以看到所有链接、信道及节点相关的信息。
    administartor：包含monitoring的所有权限，并且可以管理用户、虚拟机、权限、策略、参数等。(最高权限)
```

## 3.队列操作

```c
~]# rabbitmqctl add_vhost {vhostName}   #命令创建一个新的 vhost
~]# rabbitmqctl list_vhosts {name,tracing} #name：罗列出所有虚拟机,tracing：表示是否使用了RabbitMQ的trace功能
~]# rabbitmqctl delete_vhost {vhostName}	#删除一个vhost，同时也会删除其下所有的队列、交换器、绑定关系、用户权限、参数											 #和策略等信息。
~]# rabbitmqctl set permissions [-p vhostName] Username Conf Write Read # RabbitMQ中的授予权限是指在vhost级别对																			# 用户而言的权限授予。
    vhostName： 授予用户访问权限的 vhost 名称，可以设置为默认值，即 vhost 为 "/"。
    Username： 可以访问指定 vhost 的用户名。
    Conf： 一个用于匹配用户在哪些资源上拥有可配置权限的正则表达式。(交换机，队列，创建用户等)
    Write： 一个用于匹配用户在哪些资源上拥有可写权限的正则表达式。
    Read： 一个用于匹配用户在哪些资源上拥有可读权限的正则表达式。


~]# rabbitmqctl clear_permissions [-p vhostName] {userName} # 清除用户对某个虚拟机的权限。
~]# rabbitmqctl list_permissions [-p vhost] # 用来显示虚拟主机上的权限。
~]# rabbitmqctl list_user_permissions {userName} # 用来显示用户在已分配虚拟机上的权限。


实例：
    ~]# rabbitmqctl set_permissions -p vhost1 root ".*" ".*" ".*" 		#配置root用户在vhost1队列拥有所有权限
    
    ~]# rabbitmqctl set_permissions -p vhost2 root "^queue.*" ".*" ".*" #配置root用户在vhost2队列拥有以"queue"开																		 #头的资源上具备可配置权限，并在所有资源上有																		   #用读写权限
```

## 4.应用管理

```c
# 停止运行RabbitMQ的Erlang虚拟机和RabbitMQ服务应用，其中pid_file是通过rabbitmq-server 命令启动 RabbitMQ 服务时创建的，  默认情况下存放于mnesia 目录中。注意rabbitmq-server -detach 这个带有 -detach 后缀的命令来启动 RabbitMQ 服务则不会生成 pid_file 文件。指定pid_file会等待指定进程的结束。
~]# rabbitmqctl stop [pid_file] 	

# 停止运行 RabbitMQ 的 Erlang 虚拟机和 RabbitMQ 务应用。如果 RabbitMQ 没有成功关闭，则会返回一个非零值。这个命令和rabbitmqctl stop 不同的是，它不需要指定 pid_file 而可以阻塞等待指定进程的关闭。
~]# rabbitmqctl shutdown 

#停止 RabbitMQ 服务应用，但是 Erlang 虚拟机还是处于运行状态。此命令的执行优先于其 他管理操作，比如 rabbitmqctl reset。    
~]# rabbitmqctl stop_app 
    
# 启动 RabbitMQ 应用。命令 型的用途是在执行了其他管理操作之后，重新启动之前停 止的 RabbitMQ 应用，比 rabbi tmqctl reset。
~]# rabbitmqctl start_app 

# 等待 RabbitMQ 应用的启动。它会等到 pid_file 的创建，然后等待 pid_file 中所代表 的进程启动。当指定的进程没有启动 RabbitMQ 应用而关闭时将会返回失败。
~]# rabbitmqctl wait [pid_file] 

# 将RabbitMQ 节点重置还原到最初状态。包括从原来所在的集群中删除此节点，从管理数据库 中删除所有的配置数据，如己配置的用户、 vhost 等，以及删除所有的持久化消息。执行 rabbi tmqctl reset 命令前必须停止RabbitMQ 应用。
~]# rabbitmqctl reset 

# 强制将 RabbitMQ 节点重置还原到最初状态。不同于 rabbitmqctl reset 命令， rabbitmqctl force_reset 命令不论当前管理数据库的状态和集群配置是什么，都会无条件地重直节点。它只能在数据库或集群配置己损坏的情况下使用。与 rabbitmqctl reset 命令一样，执行 rabbitmqctl force_reset 命令前必须先停止 RabbitMQ 应用。
~]# rabbitmqctl force_reset 

# 指示 RabbitMQ 节点轮换日志文件。RabbitMQ 节点会将原来的日志文件中的内容追加到"原 始名称+后缀"的日志文件中，然后再将新的日志内容记录到新创建的日志中(与原日志文件同 名)。当目标文件不存在时，会重新创建。如果不指定后缀 suffix. 则日志文件只是重新打开 而不会进行轮换。    
~]# rabbitmqctl rotate_logs {suffix} 
```

## 5.集群命令

```c
~]# rabbitmqctl join_cluster {cluster_node} [--ram] #将节点加入指定集群,在命令执行前需要停止RabbitMQ应用并重置节点。

~]# rabbitmqctl cluster_status # 显示集群的状态。

~]# rabbitmqctl change_cluster_node_type {disc|ram}  #修改集群节点的类型。在这个命令执行前需要停止 RabbtMQ 应用。

~]# rabbitmqctl forget_cluster_node [--offiine] 	#将节点从集群中删除，允许离线执行 。

~]# rabbitmqctl update_ cluster_nodes {clusternode} # 在集群中的节点应用启动前咨询 clusternode 节点的最新信息，并更新相应的集群信息。这个和 join_cluster 不同，它不加入集群。考虑这样一种情况 节点A和节点B都在集群中，当节点A离线了，节点C又和节点B组成了一个集群，然后节点B又离开了集群，但A醒来的时候，他会尝试联系节点B，但是这样会失败，因为节点B已经不再集群中了。Rabbitmqctl update cluster nodes -n A C 可以解决这种场景下出现的问题。

~]# rabbitmqctl force_boot # 确保节点可以启动，即使它不是最后一个关闭的节点。通常情况下，当关闭整个 RabbitMQ 集群时，重启的第一个节点应该是最后关闭的节点，因为它可以看到其他节点所看不到的事情。 但是有时会有一些异常情况出现，比如整个集群都掉电而所有节点都认为它不是最后 个关闭 的。在这种情况下，可以调用 rabbitmqctl force_boot 命令，这就告诉节点可以无条件 地启动节点。在此节点关闭后，集群的任何变化，它都会丢失。如果最后 个关闭的节点永久 丢失了，那么需要优先使用 rabbitmqctl forget_cluster _node offline 命令，因 为它可以确保镜像队列的正常运转。

~]# rabbitmqctl sync_queue [-p vhost] {queue} # 指示未同步队列 queue的slave 镜像可以同步 maste 镜像行的内容。同步期间此队列会被 阻塞(所有此队列的生产消费者都会被阻塞)，直到同步完成。此条命令执行成功的前提是队列 queue 配置了镜像。注意 未同步队列中的消息被耗尽后 最终也会变成同步，此命令主要用 于未耗尽的队列。

~]# rabbitmqctl cancel_sync_queue [-p vhost] {queue} # 取消队列 queue 同步镜像的操作。

~]# rabbitmqctl set_cluster_name {name} # 设置集群名称。
```

# 3.服务端状态信息

## 1.查看队列信息

```c
~]# rabbitmqctl list_queues [-p vhost] [queueinfoitem ...] 		#此命令返回队列的详细信息，如果无[-p vhost]参数，																	将显示默认的vhost为"/"中的队列详情,queueinfoitem 																参数用于指示哪些队列的信息项会包含在结果集中，结果集													的列顺序将匹配参数的顺序。queueinfoitem 可以是下面列表中的任何值：

    name： 队列名称。
    durable：队列是否持久。
    auto_delete：队列是否自动删除。
    arguments：队列的参数。
    policy：应用到队列上的策略名称。
    pid：队列关联Er1ang进程的ID。
    owner_pid：处理排他队列连接的 Erlang 进程ID。如果此队列是非排他的，此值将为空。 
    exclusive：队列是否是排他的。
    exclusive_consumer_pid：订阅到此排他队列的消费者相关的信道关联的 Erlang 进程ID。如果此队列是非排他的，此值将为空
    exclusive_consumer_tag：订阅到此排他队列的消费者的 consumerTag 如果 此队列是非排他的，此值将为空。
    messages_ready：准备发送给客户端的消息个数。
    messages_unacknowledged：发送给客户端但尚未应答的消息个数。
    messages：准备发送给客户端和未应答消息的总和。
    messages_ready_ram：驻留在内存中 messages_ready 的消息个数。
    messages_unacknowledged_ram：驻留在内存中 messages_unacknowledged 的消息个数。
    messages_ram：驻留在内存中的消息总数。
    messages_persistent：队列中持久化消息的个数。对于非持久化队列来说总是0.
    messages_bytes：队列中所有消息的大小总和 这里不包括消息属性或者任何其他开销。
    messages_bytes_ready： 准备发送给客户端的消息的大小总和。
    messages_bytes_unacknowledged：发送给客户端但尚未应答的消息的大小总和。
    messages_bytes_ram：驻留在内存中的 messages_bytes。
    messages_bytes_persistent：队列中持久化的 messages_bytes。
    disk_reads：从队列启动开始，己从磁盘中读取该队列的消息总次数。
    disk_writes：从队列启动开始，己向磁盘队列写消息的总次数。
    consumer：消费者数目。
    consumer_utilisation：队列中的消息能够立刻投递给消费者的比率，介于0和1之间.这个受网络拥塞或者 Basic.Qos 的影响而小于1.
    memory：与队列相关的 Erlang 进程所消耗的内存字节数，包括械、堆及内部结构。
    slave_pids：如果队列是镜像的 ，列出所有 slave 镜像的 pid。
    synchronised_slave_pids：如果队列是镜像的，列出所有己经同步的 slave 镜像的pid。
    state：队列状态。正常情况下是running：如果队列正常同步数据可能会有"{syncing, MsgCount}"的状态;如果队列所在的节点掉线			   了，则队列显示状态为 down (此时大多数的 queueinfoitems 也将不可用)。

    

```

## 2.查看交换器的信息

```c
~]# rabbitmqctl list_exchanges [-p vhost] [exchangeinfoitem ...] 		# 返回交换器的详细细节。

exchangeinfoitem:
    name：交换器名称。
    type：交换器类型。
    durable：设置是否持久化。 
    auto_delete：是否自动删除。
    internal：是否内置的。
    arguments：其他的一些结构化参数。
    policy：交换器上的策略名称。    

```

## 3.查看绑定关系的信息

```c
~]# rabbitmqctl list_bindings [-p vhost] [bindinginfoitem ...]  	# 返回绑定关系的细节

bindinginfoitem:
	source_name：绑定中消息来源的名称。
    source_kind：绑定中消息来源的类别。
    destination_name：绑定中消息目的地的名称。
    destination_kind：绑定中消息目的地的种类。
    routing_key：绑定的路由键。
    arguments：绑定的参数。 
```

## 4.查看TCP连接统计信息

```c
~]# rabbitmqctl list_connections [connectioninfoitem ...] 	#返回TCP/IP连接的统计信息。

connectioninfoitem:
	pid：与连接相关的 Er1ang 进程 ID 
    name：连接的名称。
    port：服务器端口。
    host：返回反向 DNS 获取的服务器主机名称，或者 IP 地址，或者未启用。
    peer_port：服务器对端端口。当一个客户端与服务器连接时，这个客户端的端口就是peer_port。
    peer_host：返回反向 DNS 获取的对端主机名称，或者ip地址，或者未启用。
    ssl：是否启用 SSL
    ssl_protoco1：SSL 协议，如 tlsvl
    ssl_key_exchange：SSL 密钥交换算法，如 rsa 
    ssl_cipher：SSL 加密算法，如 aes 256 cbc 
    ssl_hash：SSL 哈希算法，如 sha
    peer_cert_subject：对端的 SSL 安全证书的主题，基于盯C4514 的形式。 
    peer_cert_issuer：对端 SSL 安全证书的发行者， 基于RFC4514 的形式 
    peer_cert_va1idity：对端 SSL 安全证书的有效期。
    state：连接状态，包括 starting tuning opening running flow blocking blocking closing closed 这几种。
    channe1s：该连接中的信道个数。
    protoco1：使用的AMQP协议的版本，当前是{0,9,1}或{0,8,0}。注意,若客户端请求的是AMQP 0-9的连接，RabbitMQ也将其视为0-9-1
    auth_mechanism：使用的 SASL 认证机制，如 PLAIN AMQPLAIN EXTERNAL RABBIT-CR-DEMO 等
    user：与连接相关的用户名。
    vhost：与连接相关的 vhost 的名称。
    timeout：连接超时/协商的心跳间隔，单位为秒。
    frame_max：最大传输帧的大小，单位为B
    channe1_max：此连接上信道的最大数量。如果值0，，则表示无上限，但客户端一般会将0转变为 65535
    c1ient_properties：在建立连接期间由客户端发送的信息属性。 
    recv_oct：收到的字节数。
    recv_cnt：收到的数据包个数。
    send_oct：发送的字节数。
    send_cnt：发送的数据包个数。
    send_pend：发送队列大小。
    connected_at：连接建立的时间戳。
```

## 5.查看信道信息

```c
~]# rabbitmqctl list_channels [channelinfoitem ...] 	# 返回当前所有信道的信息。

channelinfoitem:    
    pid：与连接相关的 Erlang 进程 ID
    connection：信道所属连接的 Erlang 进程 ID
    name：信道的名称。
    number：信道的序号。
    user：与信道相关的用户名称。
    vhost：与信道相关的 vhost
    transactional：信道是否处于事务模式。 
    confirm：信道是否处于 publisher confirm 模式。
    consumer_count：信道中的消费者的个数。
    messages_unacknowledged：己投递但是还未被 ack 的消息个数。
    messages_uncommitted：己接收但是还未提交事务的消息个数 
    acks_uncommitted：已ack 收到但是还未提交事务的消息个数
    messages_unconfirmed：己发送但是还未确认的消息个数 如果信道不处于 publisher confmn 模式下 ，则此值为0
    perfetch_count：新消费者的 Qos 个数限制 0表示无上限
    global_prefetch_count：: 整个信道的 Qos 个数限制，0表示无上限
```

## 6.其他信息统计

```c
~]# rabbitmqctl list_consumers [-p vhost] # 列举消费者信息 每行将显示由制表符分隔的己订阅队列的名称、相关信道的进程标识、consumerTag、是否需要消费端确认 prefetch_count 及参数列表这些信息。

~]# rabbitmqctl status 	# 显示 Broker 的状态，比如当前 Erlang 节点上运行的应用程序、RabbitMQ/Erlang的版本信息、os 的名称、内 存及文件描述符等统计信息。

~]# rabbitmqctl node_health_check 	# 对RabbitMQ 节点进行健康检查,确认应用是否正常运行、list_queues list_channels 是否能够正常返回等。

~]# rabbitmqctl environment # 显示每个运行程序环境中每个变量的名称和值。

~]# rabbitmqctl report #为所有服务器状态生成一个服务器状态报告,井将输出重定向到一个文件:rabbitmqctl report > report.txt

```

# 4.监控指标

https://support.huaweicloud.com/usermanual-rabbitmq/rabbitmq-ug-180413002.html

https://www.cnblogs.com/mldblue/articles/10974358.html

# 5.使用haproxy负载rabbitmq