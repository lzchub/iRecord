#1.统计一下/var/log/nginx/access.log 日志中访问量最多的前十个IP?
```
~]# cat access_log | awk ‘{print $1}’ | uniq -c |sort -rn | head -10

~]# awk '{print $1}' /var/log/nginx/access.log| sort | uniq -c | sort -nr -k1 | head -n 10
```
#2.批量创建10个系统账号user01-user10并设置密码(密码为随机8位字符串)。
```
产生01-10: 
	1 echo {01..10}
	2 seq -w 10
产生随机数:
	1 $RANDOM|md5sum|cut -c 1-8
	2 openssl rand -base64 8
	3 date +%s%N
	4 head /dev/urandom |cksum		#生成的随机数串
	5 cat /proc/sys/kernel/random/uuid 


#!/bin/bash

. /etc/init.d/functions

for i in `seq -w 10`
do
    pass="`echo $RANDOM | md5sum | cut -c 2-9`"
    echo "$pass" >> /tmp/userpass.txt
    useradd user$i &> /dev/null
    echo $pass | passwd --stdin user$i &> /dev/null
    if [ $? -eq 0 ];then
        action "useradd user$i" /bin/true
    else
        action "useradd user$i" /bin/false
    fi
done
```
#3.将/opt目录下的大于15KB的文件都移到/tmp目录下
```
~]# find /opt -size +15k -exec mv {} /tmp/ \; 
```

#4.现有A文件，编写shell脚本判断A文件中大于5的数字，并输出
```
~]# for num in `sed 's/[^0-9]/ /g' file | sed 's/ /\n/g'`;do [ $num -gt 5 ]&&echo $num;done 
~]# cat file |  tr '[a-zA-Z]' ' ' | sed 's/ /\n/g'`;do [ $num -gt 5 ]&&echo $num;done 
 
```
#5.在bash shell中$?,$#,$*代表什么,其中$#和$*的区别
```
$? 是显示最后命令的退出状态，0表示没有错误，其他表示有错误

$# 是传给脚本的参数个数

$@ 同$*

$* 显示所有向脚本传递的参数

所以，$#是一个数字，而$*是一个字符串。
```

#6.把/home目录下的大于10k的普通文件删除 
```
find /home -type f -size +10k -exec rm -f {} \;
```

#7.$符号
```
1.$0 这个程式的执行名字
2.$n 这个程式的第n个参数值，n=1..9
3.$* 这个程式的所有参数,此选项参数可超过9个。
4.$# 这个程式的参数个数
5.$$ 这个程式的PID(脚本运行的当前进程ID号)
6.$! 执行上一个背景指令的PID(后台运行的最后一个进程的进程ID号)
7.$? 执行上一个指令的返回值 (显示最后命令的退出状态。0表示没有错误，其他任何值表明有错误)
8.$- 显示shell使用的当前选项，与set命令功能相同
9.$@ 跟$*类似，但是可以当作数组用
10.awk -F {print$3} 脚本名
```

#8.查看http的并发请求数与其TCP连接状态
```
netstat -tn | awk '/^tcp/ {b[$NF]++} END {for(a in b) print a,b[a]}'
```

#9.查看/var/log下的普通文件数
```
ls /var/log/ -lR | grep '^-' | wc -l
```

#10.每天晚上 12 点，打包站点目录/var/www/html 备份到/data 目录下（最好每次备份按时间生成不同的备份包）
```
~]# vim a.sh

#!/bin/bash

cd /var/www && tar czvf /data/html-`date +%Y%m%d`.tar.gz html/

~]# crontab -e
0 0 * * * /bin/sh /root/a.sh

```

#11.请执行命令取出 linux 中 ens33 的 IP 地址(请用 cut，有能力者也可分别用 awk,sed 命令答)
```
~]# ifconfig | sed -n '2p' | awk '{print $2}'

~]# ifconfig | sed -n '2p' | cut -d ' ' -f 10

~]# ifconfig | awk 'NR==2' | awk '{print $2}'
```

#12.用正则表达式匹配IP地址
```
ifconfig | grep -o '[1-9]\{1\}[0-9]\{0,2\}\.[0-9]\{1,3\}.[0-9]\{1,3\}\.[0-9]\{1,3\}' 
fconfig | grep -o -E "([0-9]\.|[1-9][0-9]\.|1[0-9][0-9]\.|2[0-9][0-9]\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-9]{2})"
```

#13.检测httpd文件内容是否被篡改
```
在网站文件上线时先给所有文件生成MD5值
1 find /var/www/html -type f | xargs md5sum >> /tmp/md5list
2 md5sum -c /tmp/md5list   #检测文件是否被篡改
3 find /var/www/html -type f | wc -l #检测是否恶意增减文件

DIR=/var/www/html
MD5=/tmp/md5list
#dir is exist
[ ! -d $DIR ]&&{
        echo "$DIR is not exist"| mail -s "httpd alarm" root@localhost
}

if [ `md5sum -c $MD5 | grep "FAILED" | wc -l` -ne 0 ];then
        echo "httpd file is danger"
else
        echo "httpd file is OK"
fi
```

#14.取变量或字符串长度方法
```
#!/bin/bash
a=abcdef

echo $a | wc -c		#包含了\0，实际应该减少1
echo ${#a}			
expr length "$a"
```
#15.如何进行整数的计算
```
1.expr a++
2.((a++))
3.let a++
4.echo 5+3.5|bc
```

#16.使用一条命令输出1+2+3+4+5+6+7+8+9+10=55
```
1 echo `echo {1..10} | tr " " "+"`=`echo {1..10} | tr " " "+" | bc`
2 echo `seq -s "+" "10"`=`seq -s "+" "10" | bc`
```

#17.判断网站url是否正常
```
#!/bin/bash

RETVAL=0

[ ! -f /etc/init.d/functions ]&&{
        echo "/etc/init.d/functions is not exist"
        exit 1
}
. /etc/init.d/functions

usage()
{
        echo "Usage:$0 url"
        exit 1
}
#check url func
check_url()
{
        wget -T 10 --spider -t 2 $1 &> /dev/null
        #curl -s -o /dev/null www.baidu.com
        #curl -m 3 --head www.baiu.com | grep 200 &> /dev/null 
        RETVAL=$?
        if [ $RETVAL -eq 0 ];then
                action "$1 url" /bin/true
        else
                action "$1 url" /bin/false
        fi
}

main() 
{
        if [ $# -ne 1 ];then
                usage
        fi
        check_url $1
}

main $*
```
https://cloud.tencent.com/developer/article/1150915

#18.输出颜色字符
```
#!/bin/bash

RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
PINK="\033[35m"
RES="\033[0m"

usage()
{
        echo "USAGE:$0 |red|green|yellow|blue|pink"
        exit 1
}

if [ $# -ne 1 ];then
        usage
fi

case $1 in
        red)
                echo -e "$RED hello red $RES"
                ;;
        green)
                echo -e "$GREEN hello green $RES"
                ;;
        yellow)
                echo -e "$YELLOW hello yellow $RES"
                ;;
        blue)
                echo -e "$BLUE hello blue $RES"
                ;;
        pink)
                echo -e "$PINK hello pink $RES"
                ;;
        *)
                usage
esac
```

#19.从文件逐行读取内容
```
方法一:
while read line
do
    echo $line
done < filename

方法二:
exec < filename
while read line
do
    echo $line
done
```

#20.批量创建文件,随机八个字符，以_finsh.html结尾，且批量修改文件名称
```
#!/bin/bash

DIR=~/test

[ ! -d $DIR ]&&{
        mkdir -p $DIR
        echo "$DIR mkdir success."
}

#create file.html
for i in `seq 10`
do
        touch $DIR/`echo $RANDOM | md5sum | cut -c 1-8`_finsh.html
        [ $? -eq 0 ]&&{
                echo "file create success."
        }
done

#change file_finsh.html to file.jpg
for j in `ls $DIR/*.html`
do
       mv $j `echo $j | sed 's/_finsh.html/.jpg/g'`
#      ls | awk -F '_' '{print "mv " $0,$1".jpg"}' | bash
#      rename "_finsh.html" ".jpg" $i
done
```

#21.当内存小于等于100M时报警，并发送邮件给管理员
```
#!/bin/bash
#mem alarm
#get mem

mem=`free -m|grep "Mem"|awk '{print $NF}'`
#compare
if [ $mem -gt 100 ];then
        echo "mem is ok"
else
        echo "current mem is $mem."|mail -s "mem alarm" root@localhost
fi
```

#22.写一个脚本解决DOS攻击生产案例
```
提示：根据web日志或者或者网络连接数，监控当某个IP并发连接数或者短时内PV达到100，即调用防火墙命令封掉对应的IP，监控频率每隔3分钟。
防火墙命令为：iptables -I INPUT -s 10.0.1.10 -j DROP。

#!/bin/bash

FILE_LOG=/var/log/httpd/access_log
#cat $FILE_LOG | awk '{print $1}' | sort | uniq -c > /tmp/ip.txt
exec < /tmp/ip.txt
while read line
do
    pv=`echo $line | awk '{print $1}'` 
    ip=`echo $line | awk '{print $2}'`
    if [ $pv -gt 100 -a `iptables -L | grep -w "$ip" | wc -l` -eq 0 ];then
        iptables -I INPUT -s $ip -j DROP
        [ $? -eq 0 ]&&{
                echo "drop $ip success."
        }
    fi
done
```

#23.已知下面的字符串是通过RANDOM随机数变量md5sum|cut-c 1-8截取后的结果，请破解这些字符串对应的md5sum前的RANDOM对应数字？
```
21029299
00205d1c
a3da1677
暴力破解，由于random随机生成1-32000多

#!/bin/bash

for n in `seq 33000`
do
    md5=`echo $RANDOM | md5sum | cut -c 1-8`
    if [ "$md5" == "$1" ];then
        echo "$n yes"       
        exit
    fi
        echo "$n no"
done
```

#24.实现mysql数据库的分库分表备份
```
#!/bin/bash

USER=root
PASS=960711
SOCKET=/var/lib/mysql/mysql.sock
CMD="mysql -u$USER -p$PASS -S $SOCKET"
DUMP="mysqldump -u$USER -p$PASS"
DBLIST=`$CMD -e "show databases;" | sed 1d | egrep -v "schema"`
DIR=/tmp

. /etc/init.d/functions

for dbname in $DBLIST
do
#   $DUMP $dbname > $DIR/${dbname}_`date +%F`.sql
    TLIST=`$CMD -e "show tables from $dbname;" | sed 1d`    
    for tname in $TLIST
    do
        [ ! -d $DIR/$dbname ] && mkdir -p $DIR/$dbname
        $DUMP $dbname $tname > $DIR/$dbname/${tname}_`date +%F`.sql
        if [ $? -eq 0 ];then
            action "$dbname $tname dump" /bin/true
        else
            action "$dbnaem $tname dump" /bin/false
        fi
    done
done
```

#25.排序
```
1、按单词出现频率降序排序！
2、按字母出现频率降序排序！
The months of learning in Old Boy education are the few months that I think the time efficient is the most.I had also studied at other training institutions before,but I was hard to understand what the tutor said and hard to follow.It was just too much to learn with no outline.


string=The months of learning in Old Boy education are the few months that I think the time efficient is the most.I had also studied at other training institutions before, but I was hard to understand what the tutor said and hard to follow. It was just too much to learn with no outline.
方法很多，大家自己试验
1. echo $string | sed 's/ /\n/g' | tr ".|," " " | sort | uniq -c | sort -nr
2. echo $string | sed 's/[ ,.]//g' | grep -o "." | sort | uniq -c | sort -nr
```

#26.处理以下文件内容,将域名取出并进行计数排序,如处理:(百度和sohu面试题)
```
http://www.etiantian.org/index.html
http://www.etiantian.org/1.html
http://post.etiantian.org/index.html
http://mp3.etiantian.org/index.html
http://www.etiantian.org/3.html
http://post.etiantian.org/2.html
将域名先放入文件 domain.txt

awk -F "/" '{S[$3]+=1}END{for(k in S) print k,S[k]}' domain.txt | sort -k2
```
#27.有如下文本:
```
a 1
b 3
c 2
d 7
b 5
a 3
g 2
f 6
f 9
d 9
输出为:
d 16
f 15
b 8
a 4
g 2
c 2

awk '{S[$1]+=$2}END{for(k in S) print k,S[k]}' test.txt | sort -nr -k2
```

#27.删除一个文件中行号为奇数的行
```
sed '1~2'd  file
```

#28.打印1-100奇数
```
seq 1 2 100
```