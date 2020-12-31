# logrotate 配置使用

```c
主流Linux发行版上都默认安装有logrotate包，如果出于某种原因，logrotate没有出现在里头，你可以使用apt-get或yum命令来安装。
    
debian:    
	~]# apt-get install logrotate cron 
    
centos:
	~]# yum install logrotate crontabs 

logrotate的配置文件是/etc/logrotate.conf，通常不需要对它进行修改。日志文件的轮循设置在独立的配置文件中，它（们）放在/etc/logrotate.d/目录下。
        
~]# cat /etc/logrotate.d/logfile
    /var/log/log-file {
        size=50M
        dateext
        monthly
        rotate 5
        compress
        delaycompress
        missingok
        notifempty
        create 644 root root
        postrotate
            /usr/bin/killall -HUP rsyslogd
        endscript
    }    
        
参数解析：
    
    size:表示日志文件达到多大进行切割
    dateext:让旧日志文件以创建日期命名
    monthly: 日志文件将按月轮循。其它可用值为‘daily’，‘weekly’或者‘yearly’。
    rotate 5: 一次将存储5个归档日志。对于第六个归档，时间最久的归档将被删除。
    compress: 在轮循任务完成后，已轮循的归档将使用gzip进行压缩。
    delaycompress: 总是与compress选项一起用，delaycompress选项指示logrotate不要将最近的归档压缩，压缩将在下一次轮循周期进行。这在你或任何软件仍然需要读取最新归档时很有用。
    missingok: 在日志轮循期间，任何错误将被忽略，例如“文件无法找到”之类的错误。
    notifempty: 如果日志文件为空，轮循不会进行。
    create 644 root root: 以指定的权限创建全新的日志文件，同时logrotate也会重命名原始日志文件。
    postrotate/endscript: 在所有其它指令完成后，postrotate和endscript里面指定的命令将被执行。在这种情况下，rsyslogd 进程将立即再次读取其配置并继续运行。
```

**logrotate 命令使用：**

```c
1.要调用为/etc/lograte.d/下配置的所有日志调用logrotate：
~]# logrotate /etc/logrotate.conf   
    
2.要为某个特定的配置调用logrotate：
~]# logrotate /etc/logrotate.d/log-file 
    
3.排障过程中的最佳选择是使用‘-d’选项以预演方式运行logrotate。要进行验证,不用实际轮循任何日志文件,模拟演练日志轮循并显示其输出。
~]# logrotate -d /etc/logrotate.d/log-file 
    
4.即使轮循条件没有满足，我们也可以通过使用‘-f’选项来强制logrotate轮循日志文件，‘-v’参数提供了详细的输出。
~]# logrotate -vf /etc/logrotate.d/log-file 
   
5.logrotate自身的日志通常存放于/var/lib/logrotate/status目录。如果处于排障目的，我们想要logrotate记录到任何指定的文件，我们可以指定像下面这样从命令行指定。
~]# logrotate -vf –s /var/log/logrotate-status /etc/logrotate.d/log-file
    

```

