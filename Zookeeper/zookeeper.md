#架构图:

![](./picture/1.png)


## Zookeeper写数据过程：

	a)、比如 Client 向 ZooKeeper 的 Server1 上写数据，发送一个写请求。
	b)、如果Server1不是Leader，那么Server1 会把接受到的请求进一步转发给Leader，因为每个ZooKeeper的Server里面有一个是Leader。这个Leader 会将写请求广播给各个Server，比如Server1和Server2， 各个Server写成功后就会通知Leader。
	c)、当Leader收到大多数 Server 数据写成功了，那么就说明数据写成功了。如果这里三个节点的话，只要有两个节点数据写成功了，那么就认为数据写成功了。写成功之后，Leader会告诉Server1数据写成功了。
	d)、Server1会进一步通知 Client 数据写成功了，这时就认为整个写操作成功。

## Zookeeper角色：

	领导者 leader：领导者负责进行投票的发起和决议，更新系统状态
	跟随者 follower：follower 用于接收客户端请求并向客户端返回结果，在选主过程中参与投票
	观察者 observer：observer可以接收客户端连接，将写请求转发给leader节点，但observer不参与投票过程。只同步leader的状态，observer的目的是为了扩展系统，提高读取速度


## Zookeeper配置：
### 最低配置

	clientPort：服务的监听端口
	
	dataDir：用于存放内存数据快照的文件夹，同时用于集群的myid文件也存在这个文件夹里
	
	tickTime：2000：Zookeeper的时间单元。Zookeeper中所有时间都是以这个时间单元的整数倍去配置的。例如，session的最小超时时间是2*tickTime。（单位：毫秒）
	
	dataLogDir：事务日志写入该配置指定的目录，而不是“ dataDir ”所指定的目录。这将允许使用一个专用的日志设备并且帮助我们避免日志和快照之间的竞争
	
	globalOutstandingLimit：1,000：最大请求堆积数。默认是1000。Zookeeper运行过程中，尽管Server没有空闲来处理更多的客户端请求了，但是还是允许客户端将请求提交到服务器上来，以提高吞吐性能。当然，为了防止Server内存溢出，这个请求堆积数还是需要限制下的。 
	
	preAllocSize：64M：预先开辟磁盘空间，用于后续写入事务日志。默认是64M，每个事务日志大小就是64M。如果ZK的快照频率较大的话，建议适当减小这个参数。
	
	snapCount：100,000：每进行snapCount次事务日志输出后，触发一次快照， 此时，Zookeeper会生成一个snapshot.*文件，同时创建一个新的事务日志文件log.*。默认是100,000.
	
	traceFile：用于记录所有请求的log，一般调试过程中可以使用，但是生产环境不建议使用，会严重影响性能。
	
	maxClientCnxns：最大并发客户端数，用于防止DOS的，默认值是10，设置为0是不加限制
	
	clientPortAddress / maxSessionTimeout：对于多网卡的机器，可以为每个IP指定不同的监听端口。默认情况是所有IP都监听 clientPort 指定的端口
	
	minSessionTimeout：Session超时时间限制，如果客户端设置的超时时间不在这个范围，那么会被强制设置为最大或最小时间。默认的Session超时时间是在2 *  tickTime ~ 20 * tickTime 这个范围 
	
	fsync.warningthresholdms：1000：事务日志输出时，如果调用fsync方法超过指定的超时时间，那么会在日志中输出警告信息。默认是1000ms。
	
	autopurge.snapRetainCount：参数指定了需要保留的事务日志和快照文件的数目。默认是保留3个。和autopurge.purgeInterval搭配使用
	
	autopurge.purgeInterval：在3.4.0及之后版本，Zookeeper提供了自动清理事务日志和快照文件的功能，这个参数指定了清理频率，单位是小时，需要配置一个1或更大的整数，默认是0，表示不开启自动清理功能
	
	syncEnabled：Observer写入日志和生成快照，这样可以减少Observer的恢复时间。默认为true。

### 集群配置

	electionAlg：之前的版本中， 这个参数配置是允许我们选择leader选举算法，但是由于在以后的版本中，只有“FastLeaderElection ”算法可用，所以这个参数目前看来没有用了。

	initLimit：10：Observer和Follower启动时，从Leader同步最新数据时，Leader允许initLimit * tickTime的时间内完成。如果同步的数据量很大，可以相应的把这个值设置的大一些。

	leaderServes：yes：默认情况下，Leader是会接受客户端连接，并提供正常的读写服务。但是，如果你想让Leader专注于集群中机器的协调，那么可以将这个参数设置为 no，这样一来，会大大提高写操作的性能。一般机器数比较多的情况下可以设置为no，让Leader不接受客户端的连接。默认为yes

	server.x=[hostname]:nnnnn[:nnnnn] ：“x”是一个数字，与每个服务器的myid文件中的id是一样的。hostname是服务器的hostname，右边配置两个端口，第一个端口用于Follower和Leader之间的数据同步和其它通信，第二个端口用于Leader选举过程中投票通信。  
	
	syncLimit：表示Follower和Observer与Leader交互时的最大等待时间，只不过是在与leader同步完毕之后，进入正常请求转发或ping等消息交互时的超时时间。
	
	group.x=nnnnn[:nnnnn] ：“x”是一个数字，与每个服务器的myid文件中的id是一样的。对机器分组，后面的参数是myid文件中的ID
	
	weight.x=nnnnn：“x”是一个数字，与每个服务器的myid文件中的id是一样的。机器的权重设置，后面的参数是权重值
	
	cnxTimeout：5s：选举过程中打开一次连接的超时时间，默认是5s
	
	standaloneEnabled：当设置为false时，服务器在复制模式下启动

### 认证和授权选项

	zookeeper.DigestAuthenticationProvider.superDigest：disabled：启用超级管理员的用户去访问znode.可以使用org.apache.zookeeper.server.auth.DigestAuthenticationProvider来生成一个 superDigest，参数格式为："super:<password>"，一旦当前连接addAuthInfo超级用户验证通过，后续所 有操作都不会checkACL。

### 性能调整选项（只有在3.5.0之后才支持）

	zookeeper.nio.numSelectorThreads：NIO选择器的线程数量。建议使用多个选择器线程来扩大客户端的连接数，默认值是（CPU核心数/2）

	zookeeper.nio.numWorkerThreads：NIO工作线程数。如果工作线程数设置为0，那么选择器线程就可以直接输出。默认值是（CPU核心数 * 2）
	
	zookeeper.commitProcessor.numWorkerThreads：提交处理器工作线程数。如果该工作线程数设置为0，那么主线程就直接处理请求。默认是（CPU核心数）

### AdminServer配置

	admin.enableServer：true：设置为“false”禁用AdminServer。默认情况下，AdminServer是启用的。对应java系统属性是：zookeeper.admin.enableServer

	admin.serverPort：8080：Jetty服务的监听端口，默认是8080。对应java系统属性是：zookeeper.admin.serverPort

	admin.commandURL："/commands"：访问路径


https://blog.csdn.net/qianshangding0708/article/details/50067483

## Zookeeper四字命令

	yum install -y nc 

### stat

	#查看zk的状态信息，以及是否mode （集群还是单例）
	~]# echo stat | nc 192.168.5.60 2181
		Zookeeper version: 3.4.14-4c25d480e66aadd371de8bd2fd8da255ac140bcf, built on 03/06/2019 16:18 GMT
		Clients:
		 /192.168.5.60:52966[0](queued=0,recved=1,sent=0)
		
		Latency min/avg/max: 0/1/47
		Received: 98
		Sent: 97
		Connections: 1
		Outstanding: 0
		Zxid: 0x200000006
		Mode: follower
		Node count: 4

### ruok

	#查看当前zkServer是否启动，返回imok  可以理解为are you ok?
	~]# echo ruok | nc 192.168.5.60 2181
		imok

### dump

	#列出未经处理的会话和临时节点
	~]# echo dump | nc 192.168.5.60 2181
		SessionTracker dump:
		org.apache.zookeeper.server.quorum.LearnerSessionTracker@3276d62e
		ephemeral nodes dump:
		Sessions with Ephemerals (0):

### conf

	#查看服务器配置
	~]# echo conf | nc 192.168.5.60 2181
		clientPort=2181
		dataDir=/usr/local/zookeeper-3.4.14/data/version-2
		dataLogDir=/usr/local/zookeeper-3.4.14/log/version-2
		tickTime=2000
		maxClientCnxns=60
		minSessionTimeout=4000
		maxSessionTimeout=40000
		serverId=0
		initLimit=10
		syncLimit=5
		electionAlg=3
		electionPort=3888
		quorumPort=2888
		peerType=0

### cons
	
	#展示连接到服务器的客户端信息
	~]# echo cons | nc 192.168.5.60 2181
		/192.168.5.60:52974[0](queued=0,recved=1,sent=0)

### envi

	#查看zk的环境变量
	~]# echo envi | nc 192.168.5.60 2181
		Environment:
		zookeeper.version=3.4.14-4c25d480e66aadd371de8bd2fd8da255ac140bcf, built on 03/06/2019 16:18 GMT
		host.name=elk-node1
		java.version=1.8.0_202
		java.vendor=Oracle Corporation
		java.home=/usr/java/jdk1.8.0_202-amd64/jre
		java.class.path=/usr/local/zookeeper-3.4.14/bin/../zookeeper-server/target/classes:/usr/local/zookeeper-3.4.14/bin/../build/classes:/usr/local/zookeeper-3.4.14/bin/../zookeeper-server/target/lib/*.jar:/usr/local/zookeeper-3.4.14/bin/../build/lib/*.jar:/usr/local/zookeeper-3.4.14/bin/../lib/slf4j-log4j12-1.7.25.jar:/usr/local/zookeeper-3.4.14/bin/../lib/slf4j-api-1.7.25.jar:/usr/local/zookeeper-3.4.14/bin/../lib/netty-3.10.6.Final.jar:/usr/local/zookeeper-3.4.14/bin/../lib/log4j-1.2.17.jar:/usr/local/zookeeper-3.4.14/bin/../lib/jline-0.9.94.jar:/usr/local/zookeeper-3.4.14/bin/../lib/audience-annotations-0.5.0.jar:/usr/local/zookeeper-3.4.14/bin/../zookeeper-3.4.14.jar:/usr/local/zookeeper-3.4.14/bin/../zookeeper-server/src/main/resources/lib/*.jar:/usr/local/zookeeper-3.4.14/bin/../conf:
		java.library.path=/usr/java/packages/lib/amd64:/usr/lib64:/lib64:/lib:/usr/lib
		java.io.tmpdir=/tmp
		java.compiler=<NA>
		os.name=Linux
		os.arch=amd64
		os.version=3.10.0-957.el7.x86_64
		user.name=root
		user.home=/root
		user.dir=/	

### mntr

	#查看zk健康信息
	~]# echo mntr | nc 192.168.5.60 2181
		zk_version      3.4.14-4c25d480e66aadd371de8bd2fd8da255ac140bcf, built on 03/06/2019 16:18 GMT
		zk_avg_latency  1
		zk_max_latency  47
		zk_min_latency  0
		zk_packets_received     104
		zk_packets_sent 103
		zk_num_alive_connections        1
		zk_outstanding_requests 0
		zk_server_state follower
		zk_znode_count  4
		zk_watch_count  0
		zk_ephemerals_count     0
		zk_approximate_data_size        27
		zk_open_file_descriptor_count   31
		zk_max_file_descriptor_count    4096
		zk_fsync_threshold_exceed_count 0

### wchs

	#展示watch的信息
	~]# echo wchs | nc 192.168.5.60 2181
		0 connections watching 0 paths
		Total watches:0
	



	