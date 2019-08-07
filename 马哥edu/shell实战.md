<strong>1.检测httpd文件内容是否被篡改</strong>
<pre>在网站文件上线时先给所有文件生成MD5值
1 find /var/www/html -type f | xargs md5sum >> /tmp/md5list
2 md5sum -c /tmp/md5list   #检测文件是否被篡改
3 find /var/www/html -type f | wc -l #检测是否恶意增减文件
<code>DIR=/var/www/html
MD5=/tmp/md5list
#dir is exist
[ ! -d $DIR ]&&{
        echo "$DIR is not exist"| mail -s "httpd alarm" root@localhost
}

if [ `md5sum -c $MD5 | grep "FAILED"|wc -l` -ne 0 ];then
        echo "httpd file is danger"
else
        echo "httpd file is OK"
fi</code></pre>

<strong>2.取变量或字符串长度方法</strong>
<pre>
<code>#!/bin/bash
a=abcdef

echo $a | wc -L
echo ${#a}
expr length "$a"</code>
</pre>

<strong>3.如何进行整数的计算</strong>
<pre><code>expr a++
((a++))
let a++
echo 5+3.5|bc</code>
</pre>

<strong>4.使用一条命令输出1+2+3+4+5+6+7+8+9+10=55</strong>
<pre><code>1 echo `echo {1..10} | tr " " "+"`=`echo {1..10} | tr " " "+" | bc`
2 echo `seq -s "+" "10"`=`seq -s "+" "10" | bc`</code>
</pre>

<strong>5.判断网站url是否正常</strong>
<pre><code>#!/bin/bash

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

main $*</code>
<a href="https://cloud.tencent.com/developer/article/1150915">https://cloud.tencent.com/developer/article/1150915</a></pre>

<strong>6.输出颜色字符</strong>
<pre><code>#!/bin/bash

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

</code></pre>

<strong>7.从文件逐行读取内容</strong>
<pre>
方法一:
<code>while read line
do
    echo $line
done < filename</code>
方法二:
exec < filename
while read line
do
    echo $line
done
</pre>

<strong>8.批量创建文件，且批量修改文件名称</strong>
<pre>
<code>#!/bin/bash

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
done</code>
</pre>

<strong>9.当内存小于等于100M时报警，并发送邮件给管理员</strong>
<pre><code>#!/bin/bash
#mem alarm
#get mem
mem=`free -m|grep "Mem"|awk '{print $NF}'`
#compare
if [ $mem -gt 100 ];then
        echo "mem is ok"
else
        echo "current mem is $mem."|mail -s "mem alarm" root@localhost
fi</code>
</pre>

<strong>10.写一个脚本解决DOS攻击生产案例
提示：根据web日志或者或者网络连接数，监控当某个IP并发连接数或者短时内PV达到100，即调用防火墙命令封掉对应的IP，监控频率每隔3分钟。防火墙命令为：iptables -I INPUT -s 10.0.1.10 -j DROP。</strong>
<pre>
<code>
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
</code>
</pre>

<strong>11.已知下面的字符串是通过RANDOM随机数变量md5sum|cut-c 1-8截取后的结果，请破解这些字符串对应的md5sum前的RANDOM对应数字？
21029299
00205d1c
a3da1677</strong>
<pre>
暴力破解，由于random随机生成1-32000多
<code>
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
</code>
</pre>

<strong>12.批量创建10个系统账号user01-user10并设置密码(密码为随机8位字符串)。</strong>
<pre>
产生01-10: 
1 echo {01..10}
2 seq -w 10
产生随机数:
1 $RANDOM|md5sum|cut -c 1-8
2 openssl rand -base64 8
3 date +%s%N
4 head /dev/urandom |cksum
5 cat /proc/sys/kernel/random/uuid 
<code>
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
</code>
</pre>

<strong>13.实现mysql数据库的分库分表备份</strong>
<pre>
<code>#!/bin/bash

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
done</code>
</pre>

<strong>14.1、按单词出现频率降序排序！
   2、按字母出现频率降序排序！
   The months of learning in Old Boy education are the few months that I think the time efficient is the most.I had also studied at other training institutions before,but I was hard to understand what the tutor said and hard to follow.It was just too much to learn with no outline.</strong>
<pre>
string=The months of learning in Old Boy education are the few months that I think the time efficient is the most.I had also studied at other training institutions before, but I was hard to understand what the tutor said and hard to follow. It was just too much to learn with no outline.
方法很多，大家自己试验
1. echo $string | sed 's/ /\n/g' | tr ".|," " " | sort | uniq -c | sort -nr
2. echo $string | sed 's/[ ,.]//g' | grep -o "." | sort | uniq -c | sort -nr
</pre>

<strong>15.处理以下文件内容,将域名取出并进行计数排序,如处理:(百度和sohu面试题)
 http://www.etiantian.org/index.html
 http://www.etiantian.org/1.html
 http://post.etiantian.org/index.html
 http://mp3.etiantian.org/index.html
 http://www.etiantian.org/3.html
 http://post.etiantian.org/2.html</strong>
<pre>
将域名先放入文件 domain.txt
<code>awk -F "/" '{S[$3]+=1}END{for(k in S) print k,S[k]}' domain.txt | sort -k2</code>
</pre>

<strong>16.有如下文本:
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
c 2</strong>
<pre><code>awk '{S[$1]+=$2}END{for(k in S) print k,S[k]}' test.txt | sort -nr -k2</code>