# 升级Centos7 内核版本

```
~]# rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org 
~]# rpm -ivh http://www.elrepo.org/elrepo-release-7.0-2.el7.elrepo.noarch.rpm   
~]# yum --enablerepo=elrepo-kernel install -y kernel-ml 
~]# awk -F\' '$1=="menuentry " {print $2}' /etc/grub2.cfg 
    CentOS Linux (5.8.9-1.el7.elrepo.x86_64) 7 (Core)
    CentOS Linux (3.10.0-1062.el7.x86_64) 7 (Core)
    CentOS Linux (0-rescue-111402abe8974cb39586b38761b9f512) 7 (Core)

~]# grub2-set-default 0 # -->> 根据上面的结果选择，重启服务器即可生效，默认从0开始排号
```



# 本地升级内核

```c
下载指定版本 kernel： http://rpm.pbone.net/index.php3?stat=3&limit=1&srodzaj=3&dl=40&search=kernel

下载指定版本 kernel-devel：http://rpm.pbone.net/index.php3?stat=3&limit=1&srodzaj=3&dl=40&search=kernel-devel

官方 Centos 6: http://elrepo.org/linux/kernel/el6/x86_64/RPMS/

官方 Centos 7: http://elrepo.org/linux/kernel/el7/x86_64/RPMS/

 
将kernel-4.9.86-30.el7.x86_64.rpm、kernel-devel-4.9.86-30.el7.x86_64.rpm拷贝到机器任意目录，此目录下
~]# yum -y install kernel-devel-4.9.86-30.el7.x86_64.rpm
~]# yum -y install kernel-4.9.86-30.el7.x86_64.rpm

~]# awk -F\' '$1=="menuentry " {print $2}' /etc/grub2.cfg 
    CentOS Linux (5.8.9-1.el7.elrepo.x86_64) 7 (Core)
    CentOS Linux (3.10.0-1062.el7.x86_64) 7 (Core)
    CentOS Linux (0-rescue-111402abe8974cb39586b38761b9f512) 7 (Core)

~]# grub2-set-default 0 # -->> 根据上面的结果选择，重启服务器即可生效，默认从0开始排号
```

