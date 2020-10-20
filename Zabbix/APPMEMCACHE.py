#!/usr/bin/env python
#_*_coding:utf-8_*_

import os,commands,sys
import datetime,time
#import memcache

IP = '127.0.0.1'
#Port = '11211'
Port = sys.argv[1]
print '=' * 56

Date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
ISOTIMEFORMAT = '%Y-%m-%d %X'
TimeStamp = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))

Tmp_File_Path = '/tmp/Monitor/MEMCACHE/status_%s' %Port   #指定监控值输出文件
print "Tmp_File_Path------>",Tmp_File_Path


def Moniter_Memcached():


    #curr_items	服务器当前存储的items数量
    Status,Memcached_Curr_Items = commands.getstatusoutput(''' echo -e "stats\nquit" | nc %s %s | grep "STAT $1" |grep curr_items|awk '{print $3}' '''%(IP,Port))

    #total_items 从服务器启动以后存储的items总数量
    Status,Memcached_Total_Items = commands.getstatusoutput(''' echo -e "stats\nquit" | nc %s %s | grep "STAT $1" |grep total_items|awk '{print $3}' '''%(IP,Port))

    #bytes 当前服务器存储items占用的字节数
    Status,Memcached_Bytes = commands.getstatusoutput(''' echo -e "stats\nquit" | nc %s %s | grep "STAT $1" |grep '^STAT bytes ' |awk '{print $3}' '''%(IP,Port))

    #bytes_read	总读取字节数（请求字节数）
    Status,Memcached_Bytes_Read = commands.getstatusoutput(''' echo -e "stats\nquit" | nc %s %s | grep "STAT $1" |grep 'bytes_read' |awk '{print $3}' '''%(IP,Port))

    #bytes_written	总发送字节数（结果字节数）
    Status,Memcached_Bytes_Written = commands.getstatusoutput(''' echo -e "stats\nquit" | nc %s %s | grep "STAT $1" |grep 'bytes_written' |awk '{print $3}' '''%(IP,Port))

    #limit_maxbytes	分配给memcache的内存大小（字节）
    Status,Memcached_Limit_Maxbytes = commands.getstatusoutput(''' echo -e "stats\nquit" | nc %s %s | grep "STAT $1" |grep 'limit_maxbytes' |awk '{print $3}' '''%(IP,Port))

    #curr_connections	当前打开着的连接数
    Status,Memcached_Curr_Connections = commands.getstatusoutput(''' echo -e "stats\nquit" | nc %s %s | grep "STAT $1" |grep 'curr_connections' |awk '{print $3}' '''%(IP,Port))

    #total_connections	从服务器启动以后曾经打开过的连接数
    Status,Memcached_Total_Connections = commands.getstatusoutput(''' echo -e "stats\nquit" | nc %s %s | grep "STAT $1" |grep 'total_connections' |awk '{print $3}' '''%(IP,Port))

    #connection_structures	服务器分配的连接构造数
    Status,Memcached_Connection_Structures = commands.getstatusoutput(''' echo -e "stats\nquit" | nc %s %s | grep "STAT $1" |grep 'connection_structures' |awk '{print $3}' '''%(IP,Port))

    #cmd_get	get命令（获取）总请求次数
    Status,Memcached_Cmd_Get = commands.getstatusoutput(''' echo -e "stats\nquit" | nc %s %s | grep "STAT $1" |grep 'cmd_get' |awk '{print $3}' '''%(IP,Port))

    #cmd_set	set命令（保存）总请求次数
    Status,Memcached_Cmd_Set = commands.getstatusoutput(''' echo -e "stats\nquit" | nc %s %s | grep "STAT $1" |grep 'cmd_set' |awk '{print $3}' '''%(IP,Port))

    #get_hits	总命中次数
    Status,Memcached_Get_Hits = commands.getstatusoutput(''' echo -e "stats\nquit" | nc %s %s | grep "STAT $1" |grep 'get_hits' |awk '{print $3}' '''%(IP,Port))

    #get_misses	总未命中次数
    Status,Memcached_Get_Misses = commands.getstatusoutput(''' echo -e "stats\nquit" | nc %s %s | grep "STAT $1" |grep 'get_misses' |awk '{print $3}' '''%(IP,Port))

    #threads	当前线程数
    Status,Memcached_Threads = commands.getstatusoutput(''' echo -e "stats\nquit" | nc %s %s | grep "STAT $1" |grep 'threads' |awk '{print $3}' '''%(IP,Port))


    # set start command 
    mkdir_command = "mkdir -p /tmp/Monitor/MEMCACHE"

    #Run the start_command
    if os.system(mkdir_command)==0:
        print 'Successful mkdir'
        print "mkdir command------->>",mkdir_command

        #把 key值信息写到一个临时文件
        with open(Tmp_File_Path,'wb') as f:
            #f.write('=' * 86 + '\n')
            f.write('%s:%s\n'%('curr_items',Memcached_Curr_Items))
            f.write('%s:%s\n'%('total_items',Memcached_Total_Items))
            f.write('%s:%s\n'%('bytes',Memcached_Bytes))
            f.write('%s:%s\n'%('bytes_read',Memcached_Bytes_Read))
            f.write('%s:%s\n'%('bytes_written',Memcached_Bytes_Written))
            f.write('%s:%s\n'%('limit_maxbytes',Memcached_Limit_Maxbytes))
            f.write('%s:%s\n'%('curr_connections',Memcached_Curr_Connections))
            f.write('%s:%s\n'%('total_connections',Memcached_Total_Connections))
            f.write('%s:%s\n'%('connection_structures',Memcached_Connection_Structures))
            f.write('%s:%s\n'%('cmd_get',Memcached_Cmd_Get))
            f.write('%s:%s\n'%('cmd_set',Memcached_Cmd_Set))
            f.write('%s:%s\n'%('get_hits',Memcached_Get_Hits))
            f.write('%s:%s\n'%('get_misses',Memcached_Get_Misses))
            f.write('%s:%s\n'%('threads',Memcached_Threads))


if __name__=='__main__':
    Moniter_Memcached()

