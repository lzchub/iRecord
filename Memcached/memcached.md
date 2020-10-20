# 1.Memcached安装

## 1.1 yum安装

## 1.2 编译安装

**1.安装libevent**

libevent各版本地址：http://libevent.org/old-releases.html 

```c
~]# wget https://github.com/downloads/libevent/libevent/libevent-2.0.21-stable.tar.gz
~]# tar -zxvf libevent-2.0.21-stable.tar.gz 
~]# cd ibevent-2.0.21-stable
~]# ./configure --prefix=/usr/local/libevent-2.0.21-stable 
~]# make
~]# make install

检查是否安装成功：    
~]# ls -al /usr/local/libevent-2.0.21-stable/lib | grep libevent    
```

**也可以直接yum安装：**

```c
~]# yum install -y libevent libevent-devel 
```

**2.安装memcached**

memcached各版本下载地址：https://github.com/memcached/memcached/wiki/ReleaseNotes 

```c
~]# wget http://memcached.org/files/memcached-1.5.0.tar.gz 
~]# tar -zxvf memcached-1.5.0.tar.gz 
~]# cd memcached-1.5.0
# yum安装可省略 --with-libevent参数    
~]# ./configure --with-libevent=/usr/local/libevent-2.0.21-stable/ --prefix=/usr/local/memcached-1.5.0
	
~]# make & make install
```

# 2.Memcached常用命令参数

**1.启动服务**

```c
~]# ./usr/local/bin/memcached -d -u root  -l 192.168.1.197 -m 2048 -p 12121

-p <num>      设置TCP端口号(默认设置为: 11211)
-U <num>      UDP监听端口(默认: 11211, 0 时关闭) 
-l <ip_addr>  绑定地址(默认:所有都允许,无论内外网或者本机更换IP，有安全隐患，若设置为127.0.0.1就只能本机访问)
-c <num>      max simultaneous connections (default: 1024)
-d            以daemon方式运行
-u <username> 绑定使用指定用于运行进程<username>
-m <num>      允许最大内存用量，单位M (默认: 64 MB)
-P <file>     将PID写入文件<file>，这样可以使得后边进行快速进程终止, 需要与-d 一起使用
```

**2.测试服务是否启动**

```c
~]# telnet 192.168.1.197 11211
stats
....    
```

# 3.Memcached使用账号密码登录认证

**1、确认memcache服务器是否已经安装cyrus-sasl服务**

```c
~]# rpm-qa|grepcyrus-sasl
#如果机器没有安装的话可以执行yum安装
~]# yum install -y cyrus-sasl-devel cyrus-sasl-plain cyrus-sasl cyrus-sasl-lib
```

**2、修改默认的密码验证机制为shadow**

```c
~]# cat /etc/sysconfig/saslauthd | grep MECH
MECH=shadow    
```

**3、启动saslauthd服务并添加开机自启**

```c
~]# systemctl start saslauthd
~]# systemctl enable saslauthd
```

**4、为memcached进程添加用户及账号**

```c
~]# saslpasswd2 -a memcached -c memcache
~]# sasldblistusers2 	#查看账号是否创建成功
```

**5、修改存放虚拟账号的文件权限，方便memcache普通用户访问**

```c
chmod644/etc/sasldb2
```

**6、停掉现有memcache服务并备份编译目录**

**7、重新编译memcache**

```c
~]# cd /root/memcached-1.5.0/
~]# ./configure --prefix=/usr/local/memcached-1.5.0 --enable-sasl
~]# make && make install
```

**8、启动memcache服务**

```c
~]# ./usr/local/memcached-1.5.0/bin/memcached -u memcache -I 4194304 -p 11211 -m 2048m -d -S -U 0
```

<font color=red>**注**：若服务器上不存在memcache账号需要创建</font>

```c
~]# useradd memcache 
```

