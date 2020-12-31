# OpenSSH 升级

## 1. centos 7

```c
~]# openssl version			#升级前
OpenSSL 1.0.2k-fips  26 Jan 2017
    
~]# ssh -V			#升级前
OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017
    
1.安装依赖
~]# yum -y install gcc zlib zlib-devel make pam pam-devel
    
2.编译安装dropbear
~]# tar xvfj dropbear-2020.80.tar.bz2
~]# cd dropbear-2020.80  
~]# mkdir /opt/dropbear
~]# ./configure --prefix=/opt/dropbear/
~]# make && make install

3.启动dropbear作为备用ssh
~]# mkdir /etc/dropbear
~]# /opt/dropbear/bin/dropbearkey -t rsa -s 2048 -f /etc/dropbear/dropbear_rsa_host_key
~]# /opt/dropbear/sbin/dropbear -p 51213
~]# iptables -I INPUT -p tcp -m state --state NEW --dport 51213  -j ACCEPT

通过dropbear登录主机：ssh -p 51213 账号@IP

4.升级openssl
~]# openssl version
~]# tar xvfz openssl-1.1.1i.tar.gz
~]# cd openssl-1.1.1i
~]# ./config --prefix=/usr/ shared
~]# make
~]# make install
~]# openssl version

5.安装编译openssh
~]# cd ..
~]# tar xvfz openssh-8.4p1.tar.gz
~]# cd openssh-8.4p1/
~]# ./configure --prefix=/usr --sysconfdir=/etc/ssh --with-pam --with-zlib --with-md5-passwords
#屏蔽ssh版本：
~]# vim /home/xuwei_cmsc19/openssh-8.4p1/version.h 
#define SSH_VERSION     "OpenSSH_8.4"  改成    "YST-SSH" 
~]# make && make install
~]# netstat -ntpl
~]# ssh -V

```

