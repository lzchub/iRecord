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

