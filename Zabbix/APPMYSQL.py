#!/usr/bin/env python
#_*_coding:utf-8_*_

import os,commands,sys
import datetime,time


IP = 'localhost'
#Username = 'zabbix'
#Password = 'zabbix_201#ysT_sY'
Port = sys.argv[1]
Username = 'zabbixmonitor'
Password = 'ysten@32123'
print '=' * 56

Date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
ISOTIMEFORMAT = '%Y-%m-%d %X'
TimeStamp = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))

Tmp_File_Path = '/tmp/Monitor/MYSQL/status_%s' %Port   #指定监控值输出文件
print "Tmp_File_Path------>",Tmp_File_Path



def Monitor_MySQL():
    
    # 查询change_db
    Status,MySQL_Change_Db = commands.getstatusoutput(''' mysql -N -u%s -p%s -e "show global status" |grep '^Com_change_db' | awk -F' ' '{ print $2 }' ''' %(Username,Password))

    # 查询select
    Status,MySQL_Select = commands.getstatusoutput(''' mysql -N -u%s -p%s -e "show global status" |grep '^Com_select' |awk -F' ' '{ print $2 }' ''' %(Username,Password))

    # 查询insert
    Status,MySQL_Insert = commands.getstatusoutput(''' mysql -N -u%s -p%s -e "show global status" |grep '^Com_insert' | grep -v '^Com_insert_'|awk -F' ' '{ print $2 }' ''' %(Username,Password))
    print "MySQL_Insert",MySQL_Insert
 
    # 查询update
    Status,MySQL_Update = commands.getstatusoutput(''' mysql -N -u%s -p%s -e "show global status" |grep '^Com_update' | grep -v '^Com_update_'|awk -F' ' '{ print $2 }' ''' %(Username,Password))

    # 查询delete
    Status,MySQL_Delete = commands.getstatusoutput(''' mysql -N -u%s -p%s -e "show global status" |grep '^Com_delete' | grep -v '^Com_delete_'|awk -F' ' '{ print $2 }' ''' %(Username,Password))

    # 每秒钟获得的查询数量
    Status,MySQL_Queries = commands.getstatusoutput(''' mysql -N -u%s -p%s -e "show global status" |grep '^Queries' | awk -F' ' '{ print $2 }' ''' %(Username,Password))
    
    # 查询缓存被访问的次数
    Status,MySQL_Qcache_Hits = commands.getstatusoutput(''' mysql -N -u%s -p%s -e "show global status" |grep '^Qcache_hits'| awk -F' ' '{ print $2 }' ''' %(Username,Password))
 
    # 查询缓存被访问的次数
    Status,MySQL_Qcache_Inserts = commands.getstatusoutput(''' mysql -N -u%s -p%s -e "show global status" |grep '^Qcache_inserts'| awk -F' ' '{ print $2 }' ''' %(Username,Password))
    
    # 查询主从延迟时间
    Status,MySQL_mysqlslave_delaytime = commands.getstatusoutput(''' mysql  -u%s -p%s -e "show slave status\G;" | egrep "Seconds_Behind_Master" | awk -F' ' '{print $2}' ''' %(Username,Password))
    
    # 创建用来处理连接的线程数
    Status,MySQL_Threads_created = commands.getstatusoutput(''' mysql -N -u%s -p%s -e "show global status" |grep '^Threads_created'| awk -F' ' '{ print $2 }' ''' %(Username,Password))

    # 试图连接到(不管是否成功)MySQL服务器的连接数
    Status,MySQL_Connections = commands.getstatusoutput(''' mysql -N -u%s -p%s -e "show global status" |grep '^Connections'| awk -F' ' '{ print $2 }' ''' %(Username,Password))

    # 数据库主从状态
    Status,MySQL_Slave_Running = commands.getstatusoutput(''' mysql -N -u%s -p%s -e "show status like 'Slave_running';" ''' %(Username,Password))
    Status,MySQL_Slave_Status = commands.getstatusoutput(''' mysql -N -u%s -p%s -e "show slave status\G;" | egrep "Slave_SQL_Running|Slave_IO_Running" ''' %(Username,Password))
    if ("ON" in MySQL_Slave_Running) and ("NO" not in MySQL_Slave_Status):
        MySQL_Master_Slave_Status = 1
    else:
        MySQL_Master_Slave_Status = 0

    # set start command 
    mkdir_command = "mkdir -p /tmp/Monitor/MYSQL"

    #Run the start_command
    if os.system(mkdir_command)==0:
        print 'Successful mkdir'
        print "mkdir command------->>",mkdir_command
        #把 key值信息写到一个临时文件
        with open(Tmp_File_Path,'wb') as f:
            #f.write('=' * 86 + '\n')
            f.write('%s:%s\n'%('change_db',MySQL_Change_Db))
            f.write('%s:%s\n'%('select',MySQL_Select))
            f.write('%s:%s\n'%('insert',MySQL_Insert))
            f.write('%s:%s\n'%('update',MySQL_Update))
            f.write('%s:%s\n'%('mysqlslave_delaytime',MySQL_mysqlslave_delaytime))
            f.write('%s:%s\n'%('delete',MySQL_Delete))
            f.write('%s:%s\n'%('queries',MySQL_Queries))
            f.write('%s:%s\n'%('qcache_hits',MySQL_Qcache_Hits))
            f.write('%s:%s\n'%('qcache_inserts',MySQL_Qcache_Inserts))
            f.write('%s:%s\n'%('threads_created',MySQL_Threads_created))
            f.write('%s:%s\n'%('connections',MySQL_Connections))
            f.write('%s:%s\n'%('master_slave_status',MySQL_Master_Slave_Status))


if __name__=='__main__':
    Monitor_MySQL()