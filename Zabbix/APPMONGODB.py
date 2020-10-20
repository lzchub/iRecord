#!/usr/bin/env python
#_*_coding:utf-8_*_

import os,commands,sys
import datetime,time

Mongodb_mongostat_dir = '/usr/local/zabbix/bin/mongostat'
Mongodb_master_slave_status = '/usr/local/zabbix/bin/mongo'
IP = '127.0.0.1'
#Port = '27017'
Port = sys.argv[1]
print '=' * 56

Date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
ISOTIMEFORMAT = '%Y-%m-%d %X'
TimeStamp = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))

Tmp_File_Path = '/tmp/Monitor/MONGODB/status_%s' %Port   #指定监控值输出文件
print "Tmp_File_Path------>",Tmp_File_Path


def Monitor_MongoDB():


    #inserts/s 每秒插入次数
    Status,Mongodb_Inserts = commands.getstatusoutput(''' %s -n 1 |sort|awk '{ print $1 }' |grep -v '^$' |sed -n '1p' |awk -F"*" '{ print $2 }' ''' %Mongodb_mongostat_dir)

    #query/s 每秒查询次数
    Status,Mongodb_Query = commands.getstatusoutput(''' %s -n 1 |sort|awk '{ print $2 }' |grep -v '^$' |sed -n '1p' ''' %Mongodb_mongostat_dir)

    #update/s 每秒更新次数
    Status,Mongodb_Update = commands.getstatusoutput(''' %s -n 1 |sort|awk '{ print $3 }' |grep -v '^$' |sed -n '1p' |awk -F"*" '{ print $2 }' ''' %Mongodb_mongostat_dir)

    #delete/s 每秒删除次数
    Status,Mongodb_Delete = commands.getstatusoutput(''' %s -n 1 |sort|awk '{ print $4 }' |grep -v '^$' |sed -n '1p' |awk -F"*" '{ print $2 }' ''' %Mongodb_mongostat_dir)

    #getmore/s 每秒执行getmore次数
    Status,Mongodb_Getmore = commands.getstatusoutput(''' %s -n 1 |sort|awk '{ print $5 }' |grep -v '^$' |sed -n '1p' ''' %Mongodb_mongostat_dir)

    #flushes/s 每秒执行fsync将数据写入硬盘的次数。
    Status,Mongodb_Flushes = commands.getstatusoutput(''' %s -n 1 |sort|awk '{ print $9 }' |grep -v '^$' |sed -n '1p' ''' %Mongodb_mongostat_dir)

    #res 物理内存使用量，单位MB
    Status,Mongodb_Res = commands.getstatusoutput(''' %s -n 1 |sort|awk '{ print $11 }' |grep -v '^$' |sed -n '1p' |awk '{sub(/.$/,"")}1' ''' %Mongodb_mongostat_dir)

    #q t|r|w 当Mongodb接收到太多的命令而数据库被锁住无法执行完成，它会将命令加入队列。这一栏显示了总共、读、写3个队列的长度，都为0的话表示mongo毫无压力。高并发时，一般队列值会升高。
    Status,Mongodb_Q_T_R_W_qr = commands.getstatusoutput(''' %s -n 1 |sort|awk '{ print $12 }'|grep -v '^$' |sed -n '1p' |awk -F"|" '{print $1}' ''' %Mongodb_mongostat_dir)
    Status,Mongodb_Q_T_R_W_qw = commands.getstatusoutput(''' %s -n 1 |sort|awk '{ print $12 }'|grep -v '^$' |sed -n '1p' |awk -F"|" '{print $2}' ''' %Mongodb_mongostat_dir)

    #ar|aw 活动用户的读|写
    Status,Mongodb_Ar = commands.getstatusoutput(''' %s -n 1 |sort|awk '{ print $13 }'|grep -v '^$' |sed -n '1p' |awk -F"|" '{ print $1 }' ''' %Mongodb_mongostat_dir)
    Status,Mongodb_Aw = commands.getstatusoutput(''' %s -n 1 |sort|awk '{ print $13 }'|grep -v '^$' |sed -n '1p' |awk -F"|" '{ print $2 }' ''' %Mongodb_mongostat_dir)

    #netIn 网络流入的带宽（bit）
    Status,Mongodb_NetIn = commands.getstatusoutput(''' %s -n 1 |sort|awk '{ print $14 }'|grep -v '^$' |sed -n '1p' |awk -F"b" '{ print $1 }' |awk '{sub(/.$/,"")}1' ''' %Mongodb_mongostat_dir)

    #netOut 网络流出的带宽（bit）
    Status,Mongodb_NetOut = commands.getstatusoutput(''' %s -n 1 |sort|awk '{ print $15 }'|grep -v '^$' |sed -n '1p' |awk -F"k" '{ print $1 }' |awk '{sub(/.$/,"")}1' ''' %Mongodb_mongostat_dir)

    #conn 当前连接数
    Status,Mongodb_Conn = commands.getstatusoutput(''' %s -n 1 |sort|awk '{ print $16 }'|grep -v '^$' |sed -n '1p' ''' %Mongodb_mongostat_dir)

    #主从状态
    Status,Mongodb_Master_Slave_Status = commands.getstatusoutput(''' %s --port %s --eval "db.printReplicationInfo()"|grep secs |tr -s [:space:] |awk '{ print $1 }' ''' %(Mongodb_master_slave_status,Port))


    # set start command 
    mkdir_command = "mkdir -p /tmp/Monitor/MONGODB"

    #Run the start_command
    if os.system(mkdir_command)==0:
        print 'Successful mkdir'
        print "mkdir command------->>",mkdir_command

    #把 key值信息写到一个临时文件
    with open(Tmp_File_Path,'wb') as f:
        #f.write('=' * 86 + '\n')
        f.write('%s:%s\n'%('inserts',Mongodb_Inserts))
        f.write('%s:%s\n'%('query',Mongodb_Query))
        f.write('%s:%s\n'%('update',Mongodb_Update))
        f.write('%s:%s\n'%('delete',Mongodb_Delete))
        f.write('%s:%s\n'%('getmore',Mongodb_Getmore))
        f.write('%s:%s\n'%('flushes',Mongodb_Flushes))
        f.write('%s:%s\n'%('res',Mongodb_Res))
        f.write('%s:%s\n'%('qr',Mongodb_Q_T_R_W_qr))
        f.write('%s:%s\n'%('qw',Mongodb_Q_T_R_W_qw))
        f.write('%s:%s\n'%('ar',Mongodb_Aw))
        f.write('%s:%s\n'%('aw',Mongodb_Aw))
        f.write('%s:%s\n'%('netIn',Mongodb_NetIn))
        f.write('%s:%s\n'%('netOut',Mongodb_NetOut))
        f.write('%s:%s\n'%('conn',Mongodb_Conn))
        f.write('%s:%s\n'%('msstat',Mongodb_Master_Slave_Status))


if __name__=='__main__':
  Monitor_MongoDB()


