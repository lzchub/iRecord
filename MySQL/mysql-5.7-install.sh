#!/bin/bash
Softwarepath=/data/tools
mysqldatapath=/data/data
mysqlinstallpath=/usr/local/mysql


#----------创建数据库存放目录
mkdir -p $Softwarepath
mkdir -p $mysqldatapath


#----------获取安装二进制包和配置文件
echo "开始下载mysql二进制包"
wget http://221.131.123.245:10088/tmp/mysql-5.7.25.tar -P $Softwarepath
if [ $? == 0 ] ;then
	echo "二进制包下载成功"
fi


#----------新增Mysql用户和组
groupadd mysql
useradd mysql -g mysql -s /sbin/nologin



#-----------修改my.cnf中innodb_buffer_pool_size参数
cd $Softwarepath
tar xvf mysql-5.7.25.tar
chmod 644 *
B=`free | tr [:blank:] \\\n | grep [0-9] | sed -n '1p'`
B=$[B *5/10/1024/1024]
sed -i "s/innodb_buffer_pool_size.*/innodb_buffer_pool_size=${B}G/g" my.cnf
sed -i "s/server-id =105/server-id =106/g" my.cnf
cat /$Softwarepath/my.cnf |tr -s "\r" "\n" >my1.cnf
rm -rf my.cnf



#-----------替换配置文件my.cnf
A=`ls /etc/ |grep my.cnf |grep -v my.cnf.d|wc -l`
if [ $A = 1 ];then
 mv /etc/my.cnf /etc/mybak.cnf
 mv $Softwarepath/my1.cnf /etc/my.cnf
else
   mv $Softwarepath/my1.cnf /etc/my.cnf
fi


#----------解压二进制包并安装
echo "开始安装Mysql"
tar zxvf mysql-5.7.25-linux-glibc2.12-x86_64.tar.gz
mv mysql-5.7.25-linux-glibc2.12-x86_64 /$mysqlinstallpath
cd $mysqlinstallpath 
mkdir mysql-files
chown -R mysql.mysql mysql-files/
chmod 750 mysql-files/

#-----------初始化数据库
echo "开始初始化数据库"
$mysqlinstallpath/bin/mysqld --initialize --user=mysql



#-----------复制启动项
chmod 755 $mysqldatapath/mysql
chmod 755 $mysqlinstallpath
cp $mysqlinstallpath/support-files/mysql.server /etc/init.d/mysql
sed -i 's/^basedir\=$/basedir\=\/usr\/local\/mysql/g' /etc/init.d/mysql
sed -i 's/^datadir\=$/datadir\=\/data\/data\/mysql/g' /etc/init.d/mysql
echo 'export PATH=$PATH:/usr/local/mysql/bin' >>/etc/profile
source /etc/profile




#-----------启动mysql
/etc/init.d/mysql start
C=`more /data/data/mysql/mysql-error.log |grep Note |awk '{print $11}' |more`
echo MySQL登陆密码为:"$C"
