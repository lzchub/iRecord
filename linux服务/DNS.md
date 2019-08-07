#1.配置DNS服务（正向，反向解析）
1.安装
```
~]# yum info bind
	...
	Name        : bind
	Arch        : x86_64
	Epoch       : 32
	Version     : 9.9.4
	Release     : 61.el7_5.1
	Size        : 1.8 M
	Repo        : updates/7/x86_64
	...
~]# yum install -y bind
```
2.配置
```
~]# vim /etc/named.conf
	...
	listen-on port 53 { 192.168.179.110; };
	allow-query     { any; };
	...

~]# cat /etc/named.rfc1912.zones
	zone "chuan.com" IN {			#正向解析
	        type master;
	        file "chuan.com.zone";
	};	

	zone "179.168.192.in-addr.arpa" IN {	#反向解析
        type master;
        file "179.168.192.in-addr.zone";
        allow-update { none; };
	};

~]# cat chuan.com.zone 
$TTL 1D
@       IN SOA  ns1.chuan.com. mail.chuan.com. (
                                        0       ; serial
                                        1D      ; refresh
                                        1H      ; retry
                                        1W      ; expire
                                        3H )    ; minimum
        NS      ns1.chuan.com.
ns1     A       192.168.179.110 
www     A       192.168.179.111
web     CNAME   www	

]# cat 179.168.192.in-addr.zone 
$TTL 1D
@       IN SOA  ns1.chuan.com mail.chuan.com. (
                                        0       ; serial
                                        1D      ; refresh
                                        1H      ; retry
                                        1W      ; expire
                                        3H )    ; minimum
        NS      ns1.chuan.com.
110     PTR     ns1.chuan.com.
111     PTR     www.chuan.com.
111     PTR     web.chuan.com.


~]# chown root:named chuan.com.zone
~]# chmod 640 chuan.com.zone

~]# chown root:named 179.168.192.in-addr.zone
~]# chmod 640 179.168.192.in-addr.zone

~]# named-checkconf		#默认检查 named.conf 和 named.rfc1912.zones 文件
~]# named-checkzone chuan.com chuan.com.zone 

~]# systemctl start named
~]# ss -unl
State Recv-Q Send-Q    Local Address:Port            Peer Address:Port              
UNCONN   0    0        192.168.179.110:53                    *:*                                   
UNCONN   0    0                    ::1:53                    :::*   
```


#2.DNS主从
master：

```
~]# cat chuan.com.zone 
	zone "chuan.com" IN {
        type master;
        file "chuan.com.zone";
        allow-transfer { 192.168.179.111; };	#表示允许谁来同步数据，不设置默认任意主机都可以来同步
	};

~]# cat /var/named/chuan.com.zone
...
        NS      ns1
        NS      ns2	
ns1     A       192.168.179.110
ns2     A       192.168.179.113
...

```
slave：
```
~]# vim /etc/named.conf
	...
	listen-on port 53 { 192.168.179.110; };
	allow-query     { any; };
	...

~]# cat /etc/named.rfc1912.zones 
zone "chuan.com" IN {
        type slave;
        file "slaves/chuan.com.zone";
        masters { 192.168.179.110; };
};
```
#3.子域授权
master：
```
...
ftp     NS      ftp.ns3.chuan.com.
ftp.ns3	A		192.168.179.113
...

```
子域master：
```

```