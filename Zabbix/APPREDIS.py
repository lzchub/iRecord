#!/usr/bin/env python
#_*_coding:utf-8_*_

import os,commands,sys
import datetime,time


Redis_cli_dir = '/usr/local/zabbix/bin/redis-cli'
IP = '127.0.0.1'
#Port = '6379'
Port = sys.argv[1]
print '=' * 56

Date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
ISOTIMEFORMAT = '%Y-%m-%d %X'
TimeStamp = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))

Tmp_File_Path = '/tmp/Monitor/REDIS/status_%s' %Port   #指定监控值输出文件
print "Tmp_File_Path------>",Tmp_File_Path


def Monitor_Redis():
    # Redis存活状态
    Status,Redis_Status = commands.getstatusoutput(''' %s -h %s -p %s ping ''' %(Redis_cli_dir,IP,Port))
    
    # 连接的从库数
    Status,Redis_Connected_Slaves = commands.getstatusoutput(''' %s -h %s -p %s info |grep  "connected_slaves" ''' %(Redis_cli_dir,IP,Port))
    # 已连接客户端的数量（不包括通过从属服务器连接的客户端） 
    Status,Redis_Connected_Clients = commands.getstatusoutput(''' %s -h %s -p %s info |grep 'connected_clients' ''' %(Redis_cli_dir,IP,Port))

    # used_memory_rss 和 used_memory 之间的比率 
    Status,Redis_Mem_Fragmentation_Ratio = commands.getstatusoutput('''%s -h %s -p %s info |grep 'mem_fragmentation_ratio' ''' %(Redis_cli_dir,IP,Port))

    # 命中成功的值
    Status,Redis_Keyspace_Hits = commands.getstatusoutput('''%s -h %s -p %s info |grep 'keyspace_hit' ''' %(Redis_cli_dir,IP,Port))
   
    # 命中失败的值
    Status,Redis_Keyspace_Misses = commands.getstatusoutput('''%s -h %s -p %s info |grep 'keyspace_misses' ''' %(Redis_cli_dir,IP,Port))

    # 以人类可读的格式返回 Redis 分配的内存总量
    Status,Redis_Used_Memory = commands.getstatusoutput('''%s -h %s -p %s info |grep 'used_memory:' ''' %(Redis_cli_dir,IP,Port))

    # 以人类可读的格式返回 Redis 的内存消耗峰值
    Status,Redis_Used_Memory_Peak = commands.getstatusoutput('''%s -h %s -p %s info |grep 'used_memory_peak:' ''' %(Redis_cli_dir,IP,Port))

    # 主从状态
    Status,Redis_Master_Slave_Status = commands.getstatusoutput('''%s -h %s -p %s info |grep 'master_link_status:' ''' %(Redis_cli_dir,IP,Port))
    if "up" in Redis_Master_Slave_Status:
        Redis_Master_Slave_Status = 'master_link_status:1'
    else:
        Redis_Master_Slave_Status = 'master_link_status:0'

    # 最后一次同步在几秒钟以前
    Status,Redis_Master_Last_IO_Seconds_Ago = commands.getstatusoutput('''%s -h %s -p %s info |grep 'master_last_io_seconds_ago:' ''' %(Redis_cli_dir,IP,Port))

    # set start command 
    mkdir_command = "mkdir -p /tmp/Monitor/REDIS"

    #Run the start_command
    if os.system(mkdir_command)==0:
        print 'Successful mkdir'
        print "mkdir command------->>",mkdir_command
        #把 key值信息写到一个临时文件
        with open(Tmp_File_Path,'wb') as f:
            #f.write('=' * 86 + '\n')
            #f.write('[%s] %s\n%s\n'%(TimeStamp,'Redis_Keyspace_Hits',Redis_Keyspace_Hits))
            #f.write('[%s] %s\n%s\n'%(TimeStamp,'Redis_Keyspace_Misses',Redis_Keyspace_Misses))
            #f.write('%s\n'%(Redis_Status))
            f.write('status:%s\n'%(Redis_Status))
            f.write('%s\n'%(Redis_Connected_Slaves))
            f.write('%s\n'%(Redis_Connected_Clients))
            f.write('%s\n'%(Redis_Mem_Fragmentation_Ratio))
            f.write('%s\n'%(Redis_Keyspace_Hits))
            f.write('%s\n'%(Redis_Keyspace_Misses))
            f.write('%s\n'%(Redis_Used_Memory))
            f.write('%s\n'%(Redis_Used_Memory_Peak))
            f.write('%s\n'%(Redis_Master_Slave_Status))
            f.write('%s\n'%(Redis_Master_Last_IO_Seconds_Ago))



if __name__=='__main__':
    Monitor_Redis()

