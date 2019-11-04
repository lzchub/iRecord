#1.编译安装ipvsadm
	
	# 下载ipvsadm
	~]# wget http://www.linuxvirtualserver.org/software/kernel-2.6/ipvsadm-1.26.tar.gz -P /tmp
	~]# cd /tmp
	# 安装依赖包
	~]# yum -y install libnl* popt* gcc
	# 安装ipvsadm，注意不需要./configure
	~]# tar xf ipvsadm-1.26.tar.gz 
	~]# cd ipvsadm-1.26
	~]# make && make install

	注：可直接yum安装，yum install -y ipvsadm


#2.vs/nat模式
![](./picture/6.png)

**director:**

	#打开核心转发功能
	~]# echo 1 >/proc/sys/net/ipv4/ip_forward
	
	~]# ipvsadm -A -t 192.168.1.10:80 -s wrr
	~]# ipvsadm -a -t 192.168.1.10:80 -r 192.168.179.111 -m -w 2 
	~]# ipvsadm -a -t 192.168.1.10:80 -r 192.168.179.113 -m -w 3
	~]# ipvsadm -Ln
	
	~]# curl http://192.168.1.10

**RS1:**

	~]# yum install -y httpd
	~]# echo 'RS1 test page' >> /var/www/html/index.html
	~]# systemctl start httpd
	
	#将默认网关指向DIP
	~]# route add default gw 192.168.179.110

#3.vs/tun模式


#4.vs/dr模式
![](./picture/7.png)

**RS：**

	# (1).提供web服务和测试页面
	~]# yum -y install httpd
	~]# echo "from RS1:192.168.179.51" >/var/www/html/index.html  # 在RS1上操作
	~]# echo "from RS2:192.168.179.52" >/var/www/html/index.html  # 在RS2上操作
	~]# systemctl start httpd
	
	# (2).设置arp参数
	~]# echo 1 >/proc/sys/net/ipv4/conf/all/arp_ignore
	~]# echo 2 >/proc/sys/net/ipv4/conf/all/arp_announce
	
	# (3).设置VIP
	~]# ifconfig lo:0 192.168.31.213 netmask 255.255.255.255 up
	~]# route add -host 192.168.31.213 dev lo:0
	
	# (4).修改RS数据包流出的网关为Router，以保证能和外界客户端通信
	~]# route del default
	~]# route add default gw 192.168.179.53

**Director：**

	~]# ipvsadm -C
	~]# ipvsadm -A -t 172.16.31.213:80 -s wrr
	~]# ipvsadm -a -t 172.16.31.213:80 -r 192.168.179.51:80 -g -w 1
	~]# ipvsadm -a -t 172.16.31.213:80 -r 192.168.179.52:80 -g -w 2
	~]# ipvsadm -a -t 172.16.31.213:80 -r 127.0.0.1:80 -g -w 2
	
	# 提供本地RS
	~]# yum -y install httpd
	~]# echo "from RS3:127.0.0.1" >/var/www/html/index.html
	~]# systemctl start httpd
	
	# 添加目标地址为CIP的路由，以便调度到本地RS时，数据包能经过Router转发，而非Director直接返回给Client
	~]# route add -host 192.168.31.203 gw 192.168.31.72

**Router：**

	# 打开核心转发
	~]# echo 1 > /proc/sys/net/ipv4/ip_forward
	
	# 将Router上和RS通信的接口rp_filter设置为2
	~]# echo 2 >/proc/sys/net/ipv4/conf/ens37/rp_filter

注：Client-->Router-->Director给出了虚线，是因为这里CIP和VIP同网段，它会直接和Director通信，而不会经过Router，但这并不影响结果。

**参数解析：**

	arp_ignore	：只有arp请求包的目标ip与流入接口一致时，才返回arp应答包。值为1时，用于屏蔽RS的vip返回arp应答包.
	arp_announce  ：arp应答包可以通过不通接口流出，如eth0(ip0)上流出源地址为eth1(ip1)的广播包，此时源ip为ip1，源mac为mac0。值为2时.
	rp_filter	 ：是否检查ip与mac不匹配，0或2.用于RS给Client应答数据包时


#5.keepalived+LVS(高可用+健康状态检查）
![](./picture/8.png)
**Router:**

	~]# echo 1 >/proc/sys/net/ipv4/ip_forward

**Director(master):**

	yum install -y keepalived
	~]# route del default
	~]# route add default gw 192.168.100.51
	~]# cp /etc/keepalived/keepalived.conf /etc/keepalived/keepalived.conf.bak
	~]# vim /etc/keepalived/keepalived.conf
	! Configuration File for keepalived
	
	global_defs {
	   router_id node1
	}
	
	vrrp_instance VI_1 {
	    state MASTER
	    interface ens33
	    virtual_router_id 50
	    priority 100
	    advert_int 1
	    authentication {
	        auth_type PASS
	        auth_pass 11112222
	    }
	    virtual_ipaddress {
	        192.168.179.10/32 dev ens33 label ens33:0
	    }
	}
	
	virtual_server 192.168.179.10 80 {
	    delay_loop 6
	    lb_algo wrr
	    lb_kind DR
	    #persistence_timeout 50
	    protocol TCP
	
	    real_server 192.168.179.52 80 {
	        weight 1
	        TCP_CHECK {
	            connect_port 80
	            connect_timeout 3
	            nb_get_retry 3
	            delay_before_retry 3
	        }
	    }
	    real_server 192.168.179.53 80 {
	        weight 2
	        TCP_CHECK {
	            connect_port 80
	            connect_timeout 3
	            nb_get_retry 3
	            delay_before_retry 3
	        }
	    }
	}

	~]# systemctl start httpd


**Director(bacup):**

	~]# cat /etc/keepalived/keepalived.conf 
	! Configuration File for keepalived
	
	global_defs {
	   router_id node2 
	}
	
	vrrp_instance VI_1 {
	    state BACKUP
	    interface ens33
	    virtual_router_id 51
	    priority 90
	    advert_int 1
	    authentication {
	        auth_type PASS
	        auth_pass 11112222
	    }
	    virtual_ipaddress {
	        192.168.179.10/32 dev ens33 label ens33:0
	    }
	}
	
	virtual_server 192.168.179.10 80 {
	    delay_loop 6
	    lb_algo wrr
	    lb_kind DR
	    #persistence_timeout 50
	    protocol TCP
	
		sorry_server 127.0.0.1 80	#当RS全部宕机后调用
	
	    real_server 192.168.179.52 80 {
	        weight 1
	        TCP_CHECK {
	            connect_port 80
	            connect_timeout 3
	            nb_get_retry 3
	            delay_before_retry 3
	        }
	    }
	    real_server 192.168.179.53 80 {
	        weight 2
	        TCP_CHECK {
	            connect_port 80
	            connect_timeout 3
	            nb_get_retry 3
	            delay_before_retry 3
	        }
	    }
	}

**RS:**

	~]# yum -y install httpd
	~]# echo "rs1:192.168.179.52" > /var/www/html/index.html  # RS1上操作
	~]# echo "rs1:192.168.100.53" > /var/www/html/index.html  # RS2上操作
	~]# systemctl start httpd
	
	~]# echo 1 >/proc/sys/net/ipv4/conf/all/arp_ignore
	~]# echo 2 >/proc/sys/net/ipv4/conf/all/arp_announce
	
	~]# ifconfig lo:0 192.168.179.10 netmask 255.255.255.255 up
	~]# route add -host 192.168.179.10 dev lo
	
	~]# route add default gw 192.168.100.54

#6.LVS十种调度算法

##静态算法
####1.轮叫调度（RR，Round-Robin Scheduling）

	这种算法就是以轮叫的方式依次将请求调度不同的服务器，算法的优点是其简洁性，它无需记录当前所有连接的状态，所以它是一种无状态调度。轮叫调度算法假设所有服务器处理性能均相同，不管服务器的当前连接数和响应速度。该算法相对简单，不适用于服务器组中处理性能不一的情况，而且当请求服务时间变化比较大时，轮叫调度算法容易导致服务器间的负载不平衡。
	
####2.加权轮叫调度（WRR，Weighted Round-Robin Scheduling）

	这种算法可以解决服务器间性能不一的情况，它用相应的权值表示服务器的处理性能，服务器的缺省权值为1。假设服务器A的权值为1，B的 权值为2，则表示服务器B的处理性能是A的两倍。加权轮叫调度算法是按权值的高低和轮叫方式分配请求到各服务器。权值高的服务器先收到的连接，权值高的服 务器比权值低的服务器处理更多的连接，相同权值的服务器处理相同数目的连接数。

####3.目标地址散列调度（DH，Destination Hashing Scheduling）

	此算法先根据请求的目标IP地址，作为散列键（Hash Key）从静态分配的散列表找出对应的服务器，若该服务器是可用的且未超载，将请求发送到该服务器，否则返回空。

####4.源地址散列调度（SH，Source Hashing Scheduling）

	此算法根据请求的源IP地址，作为散列键（Hash Key）从静态分配的散列表找出对应的服务器，若该服务器是可用的且未超载，将请求发送到该服务器，否则返回空。它采用的散列函数与目标地址散列调度算法 的相同。它的算法流程与目标地址散列调度算法的基本相似。

##动态算法

####5.最小连接调度（LC，Least-Connection Scheduling）

	这种算法是把新的连接请求分配到当前连接数最小的服务器。最小连接调度是一种动态调度算法，它通过服务器当前所活跃的连接数来估计服务器的负载情况。调度器需要记录各个服务器已建立连接的数目，当一个请求被调度到某台服务器，其连接数加1；当连接中止或超时，其连接数减1。当各个服务器有相同的处理性能时，最小连接调度算法能把负载变化大的请求分布平滑到各个服务器上，所有处理时间比较长的请求不可能被发送到同一台服务器上。但是，当各个服务器的处理能力不同时，该算法并不理想，因为TCP连接处理请求后会进入TIME_WAIT状态，TCP的TIME_WAIT一般为2分钟，此时连接还占用服务器的资源，所以会出现这样情形，性能高的服务器已处理所收到的连接，连接处于TIME_WAIT状态，而性能低的服务器已经忙于处理所收到的连接，还不断地收到新的连接请求。

	计算方式：连接数=活动连接数*256 + 非活动连接数

####6.加权最小连接调度（WLC，Weighted Least-Connection Scheduling）

	这种算法是最小连接调度的超集，各个服务器用相应的权值表示其处理性能。服务器的缺省权值为1，系统管理员可以动态地设置服务器的权 值。加权最小连接调度在调度新连接时尽可能使服务器的已建立连接数和其权值成比例。

	计算方式：连接数=(活动连接数*256 + 非活动连接数)/权重

####7.最少期望延迟调度（SED，Shortest Expected Delay Scheduling）

	WLC调度算法有一定的缺陷。当请求量比较少的时候，该算法的计算结果是将请求更多的指向了权重低的服务器，即性能较差的服务器；而我们希望在请求少的时候将请求尽可能转发到性能高的服务器上。sed这种调度算法为了解决WLC的缺点而生，它不再考虑非活动连接。这种算法在请求量较少的时候也能实现类似加权轮询调度的效果。

	计算方式：连接数=(活动连接数+1)*256/权重

####8.永不排队调度（NQ，Never Queue Scheduling）

	无需队列，如果有台realserver的连接数等于0就直接分配过去，不需要在进行sed运算。

####9.基于局部性的最少链接（LBLC，Locality-Based Least Connections Scheduling）

	这种算法是请求数据包的目标 IP 地址的一种调度算法，该算法先根据请求的目标 IP 地址寻找最近的该目标 IP 地址所有使用的服务器，如果这台服务器依然可用，并且有能力处理该请求，调度器会尽量选择相同的服务器，否则会继续选择其它可行的服务器
	这种算法本质就是LC算法或理解为WLC算法。但是该算法的特性是，注意实现目标是要和静态调度算法中的DH算法一样，用于将同一类请求转发到一个固定节点，因此常用于缓存服务器的场景。但是DH算法因为是静态调度算法，不会考虑后端（缓存）服务器的当前连接数，但LBLC就是在DH算法的基础上考虑后端服务器当前的连接数。如果（缓存）服务器使用了集群（如Memcached的主主复制），因为所有节点的缓存数据都相同，因此要使用负载均衡算法来实现请求按照当前服务器的负载进行转发。而如果后端的每个缓存服务器的内容不同，使用LBLC就会破坏命中率并且导致多个缓存节点缓存了相同的数据，因此为了提高缓存命中率以及防止多个节点缓存相同的数据，一般就不采用LBLC而直接采用DH。所以，要提高负载均衡效果就要破坏缓存命中率以及多个缓存节点会缓存相同数据；要提高缓存命中率已经防止多个节点缓存相同的数据，就会降低负载均衡效果。所以这需要找到一个平衡点，根据实际需要来决定。

####10.带复制的基于局部性最少链接（LBLCR，Locality-Based Least Connections with Replication Scheduling）

	这种算法先根据请求的目标IP地址找出该目标IP地址对应的服务器组；按“最小连接”原则从该服务器组中选出一台服务器，若服务器没有超载， 将请求发送到该服务器；若服务器超载；则按“最小连接”原则从整个集群中选出一台服务器，将该服务器加入到服务器组中，将请求发送到该服务器。同时，当该 服务器组有一段时间没有被修改，将最忙的服务器从服务器组中删除，以降低复制的程度。

	为了解决LBLC算法的缺陷，即提高缓存命中率且防止多个缓存节点缓存相同数据，并且保证负载均衡效果。就需要使用这里的调度算法。
	LBLC就是一个DH+LC的算法，并不会考虑缓存命中率而只考虑尽可能的负载均衡。LBLCR这种算法中，了可以理解为后端多个缓存服务器可以通过内容交换协议实现缓存共享。因此无论请求哪个缓存节点，如果该节点没有数据，它不会直接到Web服务器上查询，而是试图到另一个缓存节点中查询，如果有则将其拿过来并放入当前的缓存服务器，这样就实现一定程度的缓存复制功能，可以提高缓存命中率。注意，这里的缓存共享并不是完全的Replication，而是仅仅当请求的节点没有需要的数据时去其他缓存节点查询所请求的缓存数据。但是这种机制因为要到其他缓存节点查询，所以性能会比直接使用DH差一些。

	这种算法也不会防止多个节点缓存相同的数据，而只能保证缓存命中率。
