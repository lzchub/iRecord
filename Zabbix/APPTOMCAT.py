#!/usr/bin/env python
#_*_coding:utf-8_*_


import os,commands,sys
import datetime,time


IP = '127.0.0.1'
#Port = '8080'
Port = sys.argv[1]
print '=' * 56

Date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
ISOTIMEFORMAT = '%Y-%m-%d %X'
TimeStamp = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))


Tmp_File_Path = '/tmp/Monitor/TOMCAT/status_%s' %Port   #指定监控值输出文件
print "Tmp_File_Path------>",Tmp_File_Path



def Monitor_Tomcat():


    #占用的CPU百分比
    Status,Tomcat_CPU_Percentage = commands.getstatusoutput(''' ps aux |grep %s |egrep -v 'python|grep' | awk '{ print $3 }' '''%(Port))

    #占用内存的百分比
    Status,Tomcat_Mem_Percentage = commands.getstatusoutput(''' ps aux |grep %s |egrep -v 'python|grep' | awk '{ print $4 }' '''%Port)

    #VSZ表示如果一个程序完全驻留在内存的话需要占用多少内存空间;
    Status,Tomcat_VSZ = commands.getstatusoutput(''' ps aux |grep %s |egrep -v 'python|grep' | awk '{ print $5 }' '''%Port)
    #Tomcat_VSZ = str(int(Tomcat_VSZ) / 1024)

    #RSS指明了当前实际占用了多少内存;
    Status,Tomcat_RSS = commands.getstatusoutput(''' ps aux |grep %s |egrep -v 'python|grep' | awk '{ print $6 }' '''%Port)
    #Tomcat_RSS = str(int(Tomcat_RSS) / 1024)


    # set start command 
    mkdir_command = "mkdir -p /tmp/Monitor/TOMCAT"

    #Run the start_command
    if os.system(mkdir_command)==0:
        print 'Successful mkdir'
        print "mkdir command------->>",mkdir_command

        #把 key值信息写到一个临时文件
        with open(Tmp_File_Path,'wb') as f:
            #f.write('=' * 86 + '\n')
            f.write('%s:%s\n'%('tomcat_cpu_percentage',Tomcat_CPU_Percentage))
            f.write('%s:%s\n'%('tomcat_mem_percentage',Tomcat_Mem_Percentage))
            f.write('%s:%s\n'%('tomcat_vsz',Tomcat_VSZ))
            f.write('%s:%s\n'%('tomcat_rss',Tomcat_RSS))


if __name__=='__main__':
    Monitor_Tomcat()

