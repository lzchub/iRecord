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
	
	# 将Router上和RS通信的接口rp_filter设置为2。
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
