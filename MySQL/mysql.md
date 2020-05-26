# 1. MySQL & MariaDB
## 1.1 二进制安装mysql

	~]# tar xf mysql-5.7.24-linux-glibc2.12-x86_64.tar.gz -C /usr/local/
	~]# ln -sv mysql-5.7.24-linux-glibc2.12-x86_64/ /usr/local/mysql
	~]# vim /etc/profile
		PATH=/usr/local/mysql/bin:$PATH
	~]# . /etc/profile
	~]# useradd -r mysql
	~]# cd /usr/local/mysql
	~]# mkdir /usr/local/mysql/{data,etc,logs}
	~]# vim /usr/local/mysql/etc/my.cnf
		[mysqld]
		datadir=/usr/local/mysql/data
		socket=/tmp/mysql.sock
		symbolic-links=0
		[mysqld_safe]
		log-error=/usr/local/mysql/logs/error.log
		pid-file=/usr/local/mysql/data/mysql.pid
		!includedir /usr/local/mysql/etc/my.cnf.d
	~]# mkdir /usr/local/mysql/etc/my.cnf.d
	~]# touch /usr/local/mysql/logs/error.log
	~]# chown -R mysql.mysql /usr/local/mysql/*
	~]# mysqld --initialize-insecure --user=mysql --datadir=/usr/local/mysql/data --basedir=/usr/local/mysql 
	~]# cp /usr/local/mysql/support-files/mysql.server /etc/init.d/mysqld
	~]# chkconfig --add mysqld
	~]# service mysqld start

注：socket文件不放在/tmp目录下回报错，不知道是什么原因

## 1.2 编译安装mysql

## 1.3 yum安装mariadb

```c
~]# yum install -y mariadb-server
~]# systemctl start mariadb
```

## 1.4 my.cnf 配置参数解析

```c

事务：
    innodb_log_files_in_group
    innodb_log_group_home_dir
    innodb_log_file_size
    innodb_mirrored_log_group
```

# 2. MySQL命令行操作

**mysql命令：**


	常用选项：
	    -h：服务端地址
	    -u：用户名
	    -p：密码
	    -P：服务端端口
	    --protocol={TCP|SOCKET|PIPE|MEMORY}：
	    本地通信：基于本地回环地址进行请求，将基于本地通信协议
	    Linux：SOCKET
	    Windows：PIPE，MEMORY
	    非本地通信：使用非本地回环地址进行的请求，TCP协议
	    --socket=path，-S path
	    ~]# mysql --socket=/tmp/mysql.sock
	    --database=db_name，-D db_name
	    -C：数据压缩传输
	    -e：非交互模式执行SQL语句
	    -E：查询结果纵向显示			
	
	1.命令行修改登录提示符
		prompt \u@chuan \r:\m:\s->
	2.修改my.cnf永久生效
		prompt=\\u@chuan \r:\m:\s->

# 3. SQL语句
## 3.1 DML-数据操作语言

### 1. insert

	定义表结构：
		mysql> create or replace table t(
		    id int primary key,
		    sex char(3) default('nv'),
		    name char(20)
		);
	
	mysql> insert into t values(1,'nan','longshuai1'); 			# 插入一行数据
	mysql> insert into t values(2,'nan','longshuai2'),(3,'nv','xiaofang1'); #一次性插入两行数据
	mysql> insert into t values(4,DEFAULT,'xiaofang2'); 			# sex字段使用默认值
	mysql> insert into t(id,name) values(5,'xiaofang3'); 			# 指定插入的字段
	mysql> insert into t(id,sex,name) values(6,'nv','xiaofang4'); # 等价于insert into t values()
	mysql> insert into t(name,id) values('xiaofang5',7); 		# 指定插入的字段，且改变字段顺序
	mysql> insert into t value(8,'nan','longshuai3'); 			# 使用value，而非values

### 2. update 

```c
mysql> UPDATE table_name SET column1 = value1, column2 = value2 WHERE id=100;
mysql> update book set bookcount=2 where bookname in ('ss') order by bookid limit 10;
mysql> update t set id=id+1 where id>5 order by id desc;
```

### 3. delete

```c
mysql> delete from t where id>6 and sex='nv';
mysql> delete from t order by id limit 2;
```

### 4. select

```c
mysql> select * from student;
mysql> select id,name from student;
mysql> select id,name from student limit 2;
mysql> select id,name from student limit 0,2;
mysql> select * from student where id=1;
mysql> select * from student where name='chuan';
mysql> select * from student where id=1 and name='chuan';
mysql> select * from student where id=1 or name='chuan';
mysql> select * from student where id>5 and id<10;
mysql> select * from test order by id asc/desc;
mysql> select * from student where id>5 order by id desc;
mysql> select ClassID from students where age  > (select avg(age) from students);
mysql> select ClassID，avg(age) FROM students GROUP BY ClassID;
mysql> select ClassID,avg(age) from students GROUP BY ClassID HANVING avg(age) > 25;
mysql> explain select * from student where age='20'\G; 		#查询是否走索引
    
    
查询执行路径：
	请求 --> 查询缓存
	请求 --> 查询缓存 --> 解析器 --> 预处理器 --> 优化器 --> 查询执行引擎 --> 存储引擎 --> 数据
    
select语句的执行流程：
	FROM --> WHERE --> Group By --> Having --> Order BY --> SELECT --> Limit
    
where：
    算数操作符：+，-，*，/，%
    比较操作符：=，<>，!=，<=>，>，>=，<，<=

    IS NULL，IS NOT NULL
    区间：BETWEEN min AND max
    IN：列表
    LIKE：模糊比较，%和_

    逻辑操作符：AND，OR，NOT

    group by：根据指定的字段把查询的结果进行分组，以用于聚合运算	
    	avg()，max()，min()，sum()，count()

    HAVING：对分组聚合后的结果进行条件过滤

    ORDER by：根据指定的字段把查询的结果进行排序
        升序：ASC
        降序：DESC

    LIMIT：对输出的结果进行数量限制
```

## 3.2 DDL-数据定义语言

### 1. create

```c
mysql> create table students(id int,name char(20));
```

### 2. alter

```c
mysql> alter user root@localhost identified by '123456';
```

### 3. drop

```c
mysql> drop database mydb;
```

## 3.3 DCL-数据控制语言

### 1.  grant

```c
mysql> grant all on *.* to 'chuan'@'localhost' identified by '123456';#授予任何库的所有权限
			
	权限列表:
		 SELECT       
		 INSERT
		 UPDATE       
		 DELETE       
		 CREATE       
		 DROP         
		 REFERENCES
		 INDEX
		 ALTER
		 CREATE TEMPORARY TABLES
		 LOCK TABLES
		 EXECUTE
		 CREATE VIEW
		 SHOW VIEW
		 CREATE ROUTINE
		 ALTER ROUTINE
		 EVENT
		 TRIGGER

```

### 2. revoke

### 3. rollback

### 4. commit

# 4. 数据库操作

## 4.1 密码修改

```c
~]# mysqladmin -u root password "123456" #没有密码的用户设置密码命令
~]# mysqladmin -uroot [-h ip] -p123456 password "654321"   #命令行修改
mysql> set password [for 'root'@'localhost'] =password('123456');		#数据库中修改
mysql> alter user root@localhost identified by '123456';
```

## 4.2 忘记密码

```c
管理员忘记密码：
	~]# /etc/init.d/mysqld stop   #必须先停止服务
	~]# mysqld_safe --skip-grant-tables --skip-networking & 	#忽略授权表启动 --skip-networking(跳过网络连接)
	~]# mysql  #可以直接登录
	mysql> update mysql.user set authentication_string=password('123456') where user='root';  
	mysql> exit
	~]# mysqladmin -uroot -p123456 shutdown
	~]# /etc/init.d/mysqld start   #然后就可正常登录
```

## 4.3 用户管理

	1.创建用户，赋予权限
		mysql> create user 'chuan'@'127.0.0.1' identified by '123456';	#无任何权限
		mysql> grant all on *.* to 'chuan'@'localhost' identified by '123456';#授予任何库的所有权限
				
		权限列表:
			 SELECT       
			 INSERT
			 UPDATE       
			 DELETE       
			 CREATE       
			 DROP         
			 REFERENCES
			 INDEX
			 ALTER
			 CREATE TEMPORARY TABLES
			 LOCK TABLES
			 EXECUTE
			 CREATE VIEW
			 SHOW VIEW
			 CREATE ROUTINE
			 ALTER ROUTINE
			 EVENT
			 TRIGGER
	
	2.修改用户名：
		mysql> rename user old_user to new_user;
		
	3.查看用户权限
		mysql> show grants for 'root'@'localhost';
		
	4.权限回收
		mysql> revoke select on test.* from 'chuan'@'192.168.100.1';
		mysql> revoke all on test.* from 'chuan'@'192.168.100.1';
	
		注：赋予权限的是哪个表，回收权限就只能指向哪个表，如这儿使用*.*将无法收回权限
		
	5.删除用户
		mysql> drop user 'username'@'hostname';
		mysql> delete from mysql.user where user='username';
		mysql> flush privileges;
## 4.4 数据库操作

```c
1.创建数据库
	mysql> create database test; 			#未指定字符集，会给默认的字符集
	mysql> create database test character set utf8; #设置为utf-8字符集
	mysql> show create database test\G; 	#查看创建信息

2.查询数据库	
	mysql> show databases;  	#查询所有数据库
	mysql> show databases like 'test%';  #查询特定的数据库
	mysql> select database();  	#查看当前所在数据库
        
3.删除数据库
    mysql> drop database test; #删除test数据库
        
4.查看当前数据库信息
    mysql> select version();	#查看当前数据库版本
    mysql> select user();		#查看当前数据库登录用户
    mysql> select now();		#查看当前时间
```

## 4.5 数据表操作

	1.创建表
		mysql> create table students(id int,name char(20));
		
	2.查看表属性
		mysql> desc students;
		mysql> show table status like 'students'\G;
		
	3.修改表名
		mysql> alter table students rename to student;
		
	4.删除表
		mysql> drop table if exists table_name1[,table_name2]...
		
	5.查看建表信息
		mysql> show create table student\G;

## 4.6 变量查询与修改

	1.查询
		mysql> select @@[global|session].sort_buffer_size;
		mysql> show [global|session] variables like "sort_buffer%";
	
	2.修改
		mysql> set [global|session] sort_buffer_size=32M;
		mysql> set @@[global|session].sort_buffer_size=32M;
	
	动态变量：能在运行过程中修改的变量称为动态变量
	静态变量：只能在数据库实例关闭状态下修改的变量称为静态变量或只读变量。

# 5. 存储引擎

```c
表类型：表级别概念，不建议在同一个库中的表上使用不同的ENGINE
    CREATE TABLE ... ENGINE[=]STORAGE_ENGINE_NAME ...
    SHOW TABLE STATUS

常见存储引擎：
    MyISAM,Aira,InnoDB,MRG_MYISAM,CSV,BLACKHOLE,MEMORY,PERFORMANCE_SCHEMA,ARCHIVE,FEDERATED
    
InnoDB：InnoBase
    Percona-XtraDB：Supports transaction,row-level,and foreign keys
    
    数据存储：存储于表空间中
    	(1) 所有数据库中的所有类型为InnoDB的表的数据和索引存储于同一个表中
    		表文件空间：datadir定义的目录中，文件：ibdata1,ibdata2 ...
    	(2) 设置参数　innodb_file_per_table=ON，意味着每个表使用单独的表空间文件
    		每个表的数据文件存储于自己专用的表空间文件中，datadir下：TBL_NAME.ibd
    
    	表结构的定义：在数据库目录，TNL_NAME.frm
    
    事务型存储索引，适合对事务要求较高的场景中，但适用于处理大量短期事务
    基于MVCC（Mutli Version Concurrency Cotorl）支持高并发，支持四个隔离级别，
    	默认级别是REPEATABLE-READ,间隙锁防止换掉幻读
    使用聚集索引（主键索引）
    支持"自适应Hash索引"
    锁粒度：行级锁，间隙锁
    
    总结：
    	数据存储：表空间
    	并发：ＭＶＣＣ，间隙锁，行级锁
    	索引：聚集索引，辅助索引
    	性能：预读操作、内存数据缓冲、内存索引缓存、自适应Hash索引、插入操作缓存区
    	备份：支持热备
    
    查看引擎状态：
    	mysql> SHOW ENGINE INNODB STATUS；
    
MyISAM：
    支持全文索引（FULLTEXT index）、压缩、空间函数（GIS）
    不支持事务
    锁粒度：表级锁
    崩溃无法保证表安全恢复 -> Aria 
    适用场景：独多写少的场景、较小的表（以保证崩溃后恢复的时间较短）
    
    数据存储：
    	文件：每个表有三个文件，存储于数据库目录中
    	TBL_NAME.frm：表格式文件
    	TBL_NAME.MYD：数据文件
    	TBL_NAME.MYL：索引文件
    
    总结：
    	加锁和并发：表级锁
    	修复：手动或自动修复，但可能会丢失数据
    	索引：非聚集索引
    	延迟索引更新
    	表压缩
    
```



# 6. 索引

	索引：提取索引的创建在表上的字段中的数据，构建出一个独特的数据结构
	
	索引的作用：加速查询操作，副作用：降低写操作性能
		表中数据子集：把表中某个或某些字段（where子句中用到的字段）的数据取出来另存为一个特定数据结构组织的数据
			
	索引类型：B+ TREE，HASH
		B+ TREE：顺序存储，每一个叶子节点到根节点的距离相同；左前缀索引，适合于范围类型的数据查询（最长为70字节左右）
			适用于B+ TREE索引的查询类型：全键值、键值范围或键前缀
				全值匹配：精确匹配某个值
					where column = ‘value’；
				最左前缀匹配：只精确匹配起头的部分
					where column like 'perfix%';
				范围匹配值：
					精确匹配某一列，范围匹配另一列
					只用访问索引的查询：范围索引
						index（name）；
						select name from students where name like ‘t%’；
			
			不适合B+ TREE索引：
				如果查询条件不是从最左侧列开始，索引无效
					index（age，name）
					where name = ‘tom’;
				不能跳过索引中的某列
					index（name，age，gender）
					where name=‘’ and age >30；  Y
					where age>30 and name=''; 	N
				如果查询中的某个列是为范围查询，那么其右侧的列都无法再使用索引优化查询
					where age>30 and name=‘’；
	
	1.在创建表时，可以增加建立索引的语句
		create table student(
			id int(4) not null AUTO_INCREMENT,
			name char(20) not null,
			age tinyint(2) not null default 0,
			dept varchar(16) default null
			primary key(id),    #主键
			KEY index_name(name)   #name字段普通索引
		);
	
	2.单列索引
		普通索引
			法一:CREATE INDEX IndexName ON TableName(字段名(length));
				eg: CREATE INDEX dept_index ON student(dept);  #创建索引
		    		DROP INDEX dept_index ON student;  #删除索引
			法二:ALTER TABLE TableName ADD INDEX IndexName(字段名(length));
				eg: ALTER TABLE student ADD INDEX dept_index(dept); #创建索引
		    		ALTER TABLE student DROP INDEX dept_index;  #删除索引
	
			注:如果是CHAR,VARCHAR,类型,length可以小于字段的实际长度,如果是BLOB和TEXT类型就必须指定长度.
		
		唯一索引
			法一:CREATE UNIQUE INDEX IndexName ON TableName(字段名(length)); 
				eg: CREATE UNIQUE INDEX dept_index ON student(dept);
			法二:ALTER TABLE TableName ADD UNIQUE(字段名(length)); 
				eg: ALTER TABLE student ADD UNIQUE(dept);
		
			注: 唯一索引,与普通索引类似,但是不同的是唯一索引要求所有的类的值是唯一的,这一点和主键索引一样.但是他允许有空值.
		
		主键索引
			主键索引,不允许有空值.主键索引建立的规则是 int优于varchar,一般在建表的时候创建,最好是与表的其他字段不相关的列或者是业务不相关的列.一般会设为 int 而且是 AUTO_INCREMENT自增类型的
		
			在创建表时未指定主键，可添加主键索引:
				alter table student change id id int primary key auto_increment;
		
	3.组合索引	
		CREATE INDEX IndexName On TableName(字段名(length),字段名(length),...);
			eg: CREATE INDEX union_index ON student(name,age,dept);
		
			注:如果你建立了 组合索引(union_index) 那么他实际包含的是3个索引(name),(name,age)(name,age,dept);
			最左前缀:where name=... 、 where name=.. and age=.. 等索引才能生效。 
		
	4.查询表中所有索引
		show index from student\G;
		explain select * from student where name='chuan'\G;  #查看是否使用索引
	
	高性能索引策略：
		（1）在where中独立使用列，尽量避免其参与运算
		（2）左前缀索引：索引构建于字段的最左侧的多少个字符，要通过索引选择性来评估
			索引选择性：不重复的索引值和数据表的记录总数的比值
		（3）多列索引：
			AND连接的多个查询条件更适合使用多列索引，而非多个单键索引
				index（gender）index（age）
				index（gender，age）		
		（4）选择合适的索引列次序：选择性最高的放左侧
	
	总结:
		1.要在表的列上创建索引。
		2.索引会加快查询速度，但会影响更新的速度，因为要维护索引。
		3.索引不是越多越好，要在频繁查询的where后的条件列上创建索引。
		4.小表或唯一值少的列上不建索引，要在大表以及不同内容多的列上创建索引。

# 7. 事务

## 7.1 ACID理论

	事务是一组原子性的SQL查询,或是一个或多个SQL语句组成的独立工作单元,一般来说,事务必须满足4个条件（ACID）：
		原子性（Atomicity，或称不可分割性）
		一致性（Consistency）
		隔离性（Isolation，又称独立性）
		持久性（Durability）
		
	原子性：一个事务（transaction）中的所有操作，要么全部完成，要么全部不完成，不会结束在中间某个环节。事务在执行过程中发生错误，会被回滚（Rollback）到事务开始前的状态，就像这个事务从来没有执行过一样。
	
	一致性：在事务开始之前和事务结束以后，数据库的完整性没有被破坏。这表示写入的资料必须完全符合所有的预设规则，这包含资料的精确度、串联性以及后续数据库可以自发性地完成预定的工作。
	
	隔离性：数据库允许多个并发事务同时对其数据进行读写和修改的能力，隔离性可以防止多个事务并发执行时由于交叉执行而导致数据的不一致。事务隔离分为不同级别，包括读未提交（Read uncommitted）、读提交（read committed）、可重复读（repeatable read）和串行化（Serializable）。
	
	持久性：事务处理结束后，对数据的修改就是永久的，即便系统故障也不会丢失。
	
	注：在 MySQL 中只有使用了 Innodb 数据库引擎的数据库或表才支持事务。在 MySQL 命令行的默认设置下，事务都是自动提交的，即执行 SQL 语句后就会马上执行 COMMIT 操作。


## 7.2 手动操作事务


	事务参数：
		mysql> show variables like 'autocommit';
		+---------------+-------+
		| Variable_name | Value |
		+---------------+-------+
		| autocommit    | ON    |
		+---------------+-------+
	
	显示启动事务：
		mysql> set @@session.autocommit=0;	#禁止自动提交事务,只禁止当前会话，@@global 为全局
		mysql> start transaction;	#手动开启事务
		mysql> savepoint p1;		#保存点
		mysql> rollback to p1;		#回滚到p1点
		mysql> release savepoint p1;#删除一个保存点
		mysql> commit;				#提交，一个事务完成
		
		mysql> show full processlist;		#查看所有用户执行情况

## 7.3 事物隔离级别

```c
READ-UNCOMMITTED：读未提交 --> 脏读
READ-COMMITTED	：读提交   --> 不可重复读,一个事务内
REPEATABLE-READ	：可重复读 --> 幻读，一个事务内
SERIALIZABLE	：串行化
    
mysql> show variables like 'tx_isolation';
mysql> select @@session.tx_isolation;
+---------------+-----------------+
| Variable_name | Value           |
+---------------+-----------------+
| tx_isolation  | REPEATABLE-READ |
+---------------+-----------------+
```

# 8. 锁

	锁类型：
		读锁：共享锁，可被多个读操作共享
		写锁：排它锁，独占锁
		
	锁粒度：
		表锁：在表级别施加锁，并发性较低
		行锁：在行级别施加锁，并发性较高，维持锁状态的成本较大
		
	锁策略：在锁粒度及数据安全性之间寻求一种平衡机制
		存储索引：级别以及何时施加或释放锁由存储引擎自行决定
		MySQL Server：表级别，可自行决定，也允许显示请求
		
	锁类型：
		显示锁：用户手动请求的锁
		隐式锁：存储引擎自行根据需要施加的锁
		
	显示锁的使用：
		(1) LOCK TABLES
			LOCK TABLES TBL_NAME READ|WRITE,TBL_NAME READ|WRITE ...
			
			UNLOCK TABLES
		
		(2) FLUSH TABLES		#将内存数据刷新进磁盘
			FLUSH TABLES TBL_NAME,...[WITH READ LOCK];
			
			UNLOCK TABLES
			
		(3) SELECT CLUASE [FOR UPDATE | LOCK IN SHARE MODE]

# 9. MySQL日志
**刷新日志**

	以下操作会刷新日志文件，刷新日志文件时会关闭旧的日志文件并重新打开日志文件。对于有些日志类型，如二进制日志，刷新日志会滚动日志文件，而不仅仅是关闭并重新打开。
		
	mysql> FLUSH LOGS;
	~]# mysqladmin flush-logs
	~]# mysqladmin refresh

## 9.1.错误日志

	记录信息：
		（1）mysqld启动和关闭过程输出的信息
		（2）mysqld运行中产生的错误信息
		（3）event scheduler运行时产生的信息
		（4）主从复制架构中，从服务器复制线程启动时产生的日志
		
	配置参数（相关变量）：
	log_error=/usr/local/mysql/logs/error.log | OFF					
	log_warning={ON|OFF}

## 9.2 查询日志

	在超时时间内完成的查询是一般查询，可以将其记录到一般查询日志中，但是建议关闭这种日志（默认是关闭的），超出时间的查询是慢查询，可以将其记录到慢查询日志中。
	
	配置参数（相关变量）：
	general_log={ON|OFF}			#是否启用查询日志
	general_log_file=HOSTNAME.log	#指定查询日志路径,不给定路径时默认文件名为 datadir/`hostname`.log 
	log_output={FILE|TABLE|NONE}	# TABLE表示记录日志到表中，FILE表示记录日志到文件中，NONE表示不记录日志。不指定时默认为file。表：table（mysql.general_log）

## 9.3 慢查询日志

	查询超出变量 long_query_time 指定时间值的为慢查询。但是查询获取锁(包括锁等待)的时间不计入查询时间内。
	
	配置参数（相关变量）：				
	long_query_time=10		 	#指定慢查询超时时长(默认10秒)，超出此时长的属于慢查询
	slow_query_log={ON|OFF} 	#也是是否启用慢查询日志，此变量和log_slow_queries修改一个另一个同时变化  slow_query_log_file=/usr/local/mysql/data/localhost-slow.log #默认路径为库文件目录下主机名加上-slow.log
	log_output={FILE|TABLE|NONE}	  #定义一般查询日志和慢查询日志的输出格式，默认为file
	log_queries_not_using_indexes=OFF #查询没有使用索引的时候是否也记入慢查询日志
	
	mysql5.7上没有该参数，mariadb上存在：
	log_slow_queries={ON|OFF}
	log_slow_filter=admin,filesort,filesort_on_disk,full_join,full_scan,query_cache,query_cache_miss,tmp_table,tmp_table_on_disk
	log_slow_rate_limit		#记录日志的速率
	log_slow_verbosity		#记录日志的详细程度

## 9.4 二进制日志

	二进制日志包含了引起或可能引起数据库改变(如delete语句但没有匹配行)的事件信息，但绝不会包括select和show这样的查询语句。语句以"事件"的形式保存，所以包含了时间、事件开始和结束位置等信息。
	
	二进制日志是以事件形式记录的，不是事务日志(但可能是基于事务来记录二进制日志)，不代表它只记录innodb日志，myisam表也一样有二进制日志。
	
	二进制日志只在事务提交的时候一次性写入(基于事务的innodb二进制日志)。

**1. 二进制日志配置**

```c
二进制日志格式：	
	binlog_format={STATEMENT|ROW|MIXED}
		STATEMENT：记录SQL语句
		ROW：行
		MIXED：混编

查看是否启用二进制日志：
    mysql> show global variables like 'log_bin';
    +---------------+-------+
    | Variable_name | Value |
    +---------------+-------+
    | log_bin       | ON    |
    +---------------+-------+
                 
查看二进制日志文件列表：
	mysql> SHOW MASTER|BINARY LOGS；
  
查看当前正在使用的二进制日志文件：
	mysql> SHOW MASTER STATUS；
            
查看二进制日志文件中的事件：
	mysql> SHOW BINLOG EVENTS [IN 'log_name'] [FROM pos] [LIMIT [offset,] row_count]；
        
将日志同步到磁盘并滚动二进制日志文件：
    mysql> flush logs;			#手动滚动，当文件到达1G时，会自动滚动
            
服务器变量：
	log-bin=/PATH/TO/BIN_LOG_FILE|OFF	#binlog
	sql_log_bin={ON|OFF}				#设置会话中是否记录binlog
	max_binlog_size=1073741824			#二进制日志最大大小，默认1G
	sync_binlog={1|0}					#只要有事务提交，立即同步到磁盘

注：出于安全和功能考虑，极不建议将二进制日志和datadir放在同一磁盘上。对于mysql 5.7，直接启动binlog可能会导致mysql服务启动失败，这时需要在配置文件中的mysqld为mysql实例分配server_id
```

**2.mysqlbinlog**


	mysqlbinlog：用于查看二进制日志
			
		mysqlbinlog [option] log-file1 log-file2...
	
		-d,--database=name：只查看指定数据库的日志操作
		-o,--offset=#：忽略掉日志中的前n个操作命令
		-r,--result-file=name：将输出的日志信息输出到指定的文件中，使用重定向也一样可以。
		-s,--short-form：显示简单格式的日志，只记录一些普通的语句，\
						 会省略掉一些额外的信息如位置信息和时间信息以及基于行的日志。\
						 可以用来调试，生产环境千万不可使用
		--set-charset=char_name：在输出日志信息到文件中时，在文件第一行加上set names char_name
		--start-datetime,--stop-datetime：指定输出开始时间和结束时间内的所有日志信息
		--start-position=#,--stop-position=#：指定输出开始位置和结束位置内的所有日志信息
		-v,-vv：显示更详细信息，基于row的日志默认不会显示出来，此时使用-v或-vv可以查看

**3.删除二进制日志**

	删除二进制日志有几种方法。不管哪种方法，都会将删除后的信息同步到二进制index文件中。
	
	1.reset master将会删除所有日志，并让日志文件重新从000001开始。
		mysql> reset master;
	
	2.PURGE { BINARY | MASTER } LOGS { TO 'log_name' | BEFORE datetime_expr }	
		#将会清空00000X之前的所有日志文件。
		mysql> purge master logs to "binlog_name.00000X"； 
		#将会删除指定日期之前的所有日志。但是若指定的时间处在正在使用中的日志文件中，将无法进行purge。
		mysql> purge master logs before 'yyyy-mm-dd hh:mi:ss'； 
	
	3.使用--expire_logs_days=N选项指定过了多少天日志自动过期清空。

**4.二进制日志相关参数**

	log_bin={on|off|base_name} #指定是否启用记录二进制日志或者指定一个日志路径(路径不能加.否则.后的被忽略)
	sql_log_bin={on|off}			#设置会话中是否记录binlog，只有在log_bin开启的时候才有效
	expire_logs_days=				#指定自动删除二进制日志的时间，即日志过期时间
	binlog_do_db= 					#明确指定要记录日志的数据库
	binlog_ignore_db= 					#指定不记录二进制日志的数据库
	log_bin_index=	 					#指定mysql-bin.index文件的路径
	binlog_format={mixed|row|statement}	#指定二进制日志基于什么模式记录
	binlog_rows_query_log_events={1|0} 	#MySQL5.6.2添加了该变量，当binlog format为row时，\
										 默认不会记录row对应的SQL语句,设置为1或其他true布尔值时会记录 \									    但需要使用mysqlbinlog -v查看，这些语句是被注释的，\
										 恢复时不会被执行。
	max_binlog_size=	 		#指定二进制日志文件最大值，超出指定值将自动滚动。但由于事务不会跨文件，\
								 所以并不一定总是精确。
	binlog_cache_size=32768		#基于事务类型的日志会先记录在缓冲区，当达到该缓冲大小时这些日志会写入磁盘
	max_binlog_cache_size=		#指定二进制日志缓存最大大小，硬限制。默认4G，够大了，建议不要改
	binlog_cache_use			#使用缓存写二进制日志的次数(这是一个实时变化的统计值)
	binlog_cache_disk_use		#使用临时文件写二进制日志的次数，当日志超过了binlog_cache_size的时候
								会使用临时文件写日志，如果该变量值不为0，则考虑增大binlog_cache_size的值
	binlog_stmt_cache_size=32768	 #一般等同于且决定binlog_cache_size大小，\
									  所以修改缓存大小时只需修改这个而不用修改binlog_cache_size
	binlog_stmt_cache_use			#使用缓存写二进制日志的次数
	binlog_stmt_cache_disk_use		#使用临时文件写二进制日志的次数，当日志超过了binlog_cache_size的时								   候会使用临时文件写日志，如果该变量值不为0，
									 则考虑增大binlog_cache_size的值
	sync_binlog = { 0 | n } 		#这个参数直接影响mysql的性能和完整性
		sync_binlog=0:不同步，日志何时刷到磁盘由FileSystem决定，这个性能最好。
		sync_binlog=n:每写n次二进制日志事件(不是事务)，MySQL将执行一次磁盘同步指令fdatasync()将缓存 \
					  日志刷新到磁盘日志文件中。Mysql中默认的设置是sync_binlog=0，即不同步， \
					  这时性能最好，但风险最大。一旦系统奔溃，缓存中的日志都会丢失。


	注：在innodb的主从复制结构中，如果启用了二进制日志(几乎都会启用)，要保证事务的一致性和持久性的时候，必须将sync_binlog的值设置为1，因为每次事务提交都会写入二进制日志，设置为1就保证了每次事务提交时二进制日志都会写入到磁盘中，从而立即被从服务器复制过去。

**5. 二进制日志定点还原数据库**

	只需指定二进制日志的起始位置（可指定终止位置）并将其保存到sql文件中，由mysql命令来载入恢复即可。当然直接通过管道送给mysql命令也可。
	
	选择时间点来恢复比较直观些，并且跨日志文件恢复时更方便。
	~]# mysqlbinlog --stop-datetime="2014-7-2 15:27:48" /tmp/mysql-bin.000008 | mysql -u user -p password
	
	恢复多个二进制日志文件时：
	~]# mysqlbinlog mysql-bin.[*] | mysql -uroot -p password
	
	或者将它们导入到一个文件中后恢复。
	~]# mysqlbinlog mysql-bin.000001 > /tmp/a.sql
	~]# mysqlbinlog mysql-bin.000002 >>/tmp/a.sql
	~]# mysql -u root -p password -e "source /tmp/a.sql"

## 9.5 事务日志

[事务日志](http://www.cnblogs.com/f-ck-need-u/p/9010872.html#auto_id_16)

## 9.6 中继日志

# 10. 备份与恢复
## 10.1 备份类型

	1.按照是否能够继续提供服务，将数据库备份类型划分为：
		热备份：在线备份，能读能写
		温备份：能读不能写
		冷备份：离线备份
		
	2.按照备份数据库对象分类：
		物理备份：直接复制数据文件
		逻辑备份：将数据导出至文件中，必要时将其还原(也包括备份成sql语句的方式)
		
	3.按照是否备份整个数据集分为：
		完全备份：备份从开始到某段时间的全部数据
		增量备份：备份自上次增量备份以来变化的数据
			-->
			    -->
			        -->
		差异备份：备份自完全备份以来变化的数据					
			-->
			------>
			-------->
	
	分类方式不同，不同分类的备份没有冲突的关系，它们可以任意组合。

## 10.2 备份内容和备份工具

	1.需要备份的内容：文件、二进制日志、事务日志、配置文件、操作系统上和MySQL相关的配置（如sudo，定时任务）。
	
	2.物理备份和逻辑备份的优缺点：
		物理备份：直接复制数据文件，速度较快。
		逻辑备份：将数据导出到文本文件中或其他格式的文件中。有MySQL服务进程参与，相比物理备份而言速度较慢；
		 		 可能丢失浮点数精度；但可以使用文本工具二次处理；可以跨版本和跨数据库系统进行移植。
	
	3.备份策略：要考虑安全，也要考虑还原时长
		完全备份+增量
		完全备份+差异
	
	4.备份工具：
	(a)mysqldump：逻辑备份工具。要求mysql服务在线。MyISAM(温备)，InnoDB（热备），逻辑备份
	(b)mysqlhotcopy：物理备份工具，温备份，实际上是冷备。加锁、flush table并进行cp或scp。即将废弃的工具
	(c)cp/tar：冷备
	(d)lvm快照：几乎热备。注意点是：先flush table、lock table、创建快照、释放锁、复制数据。\
			   因为要先flush table和lock table，这对于MyISAM来说很简单很容易实现。但对于InnoDB来说，\
			   因为事务的原因，锁表后可能还有缓存中的数据在写入文件中，所以应该监控缓存中的数据是真的已经完全			 写入数据文件中，之后才能进行复制数据。
	(e)xtrabackup：开源。MyISAM（温备），InnoDB（热备），速度较快。物理备份
				   完全备份、部分备份
				   完全备份、增量备份
				   完全备份、差异备份

## 10.3 mysqldump

官方手册：https://dev.mysql.com/doc/refman/5.7/en/mysqldump.html

	mysqldump默认会从配置文件中的mysqldump段读取选项，配置文件读取的顺序为：
	/etc/my.cnf --> /etc/mysql/my.cnf --> /usr/local/mysql/etc/my.cnf --> ~/.my.cnf
	
	语法选项：	
		mysqldump [OPTIONS] database [tables]
		mysqldump [OPTIONS] --databases [OPTIONS] DB1 [DB2 DB3...]
		mysqldump [OPTIONS] --all-databases [OPTIONS]
	
	连接选项：
		-u, --user=name        #指定用户名
		-S, --socket=name      #指定套接字路径
		-p, --password[=name]  #指定密码
		-P, --port=#           #指定端口
		-h, --host=name        #指定主机名
		-r, --result-file=name #将导出结果保存到指定的文件中，在Linux中等同于覆盖重定向。
							   在windows中因为回车符\r\n的原因，使用该选项比重定向更好
	
	筛选选项：
		--all-databases, -A：指定dump所有数据库。等价于使用--databases选定所有库
		--databases, -B：指定需要dump的库。该选项后的所有内容都被当成数据库名；
						 在输出文件中的每个数据库前会加上建库语句和use语句
		--ignore-table=db_name.tbl_name：导出时忽略指定数据库中的指定表，同样可用于忽略视图，
										 要忽略多个则多次写该选项
		-d, --no-data：不导出表数据，可以用在仅导出表结构的情况。
		--events, -E：导出事件调度器
		--routines, -R：导出存储过程和函数。但不会导出它们的属性值，若要导出它们的属性，
						可以导出mysql.proc表然后reload
		--triggers：导出触发器，默认已开启
		--tables：覆盖--databases选项，导出指定的表。但这样只能导出一个库中的表。
				  格式为--tables database_name tab_list
		--where='where_condition', -w 'where_condition'：指定筛选条件并导出表中符合筛选的数据，
														 如--where="user='jim'"
	
	DDL选项：
		--add-drop-database：在输出中的create database语句前加上drop database语句先删除数据库
		--add-drop-table：在输出的create table语句前加上drop table语句先删除表，默认是已开启的
		--add-drop-trigger：在输出中的create trigger语句前加上drop trigger语句先删除触发器
		-n, --no-create-db：指定了--databases或者--all-databases选项时默认会加上数据库创建语句，
						    该选项抑制建库语句的输出
		-t, --no-create-info：不在输出中包含建表语句
		--replace：使用replace代替insert语句
	
	字符集选项：
		--default-character-set=charset_name：在导出数据的过程中，指定导出的字符集。很重要，
											  客户端服务端字符集不同导出时可能乱码，默认使用utf8
		--set-charset：在导出结果中加上set names charset_name语句。默认启用。
	
	复制选项：
		--apply-slave-statements
		--delete-master-logs
		--dump-slave[=value]
		--include-master-host-port
		--master-data[=value]  
			该选项主要用来建立一个replication，当值为1时，导出文件中记录change master语句；
			当值为2时，change master语句被写成注释语句，默认值为空。
			该选项自动忽略--lock-tables，当没有使用--single-transaction时自动启用--lock-all-tables。
	
	格式化选项：
		--compact：简化输出导出的内容，几乎所有注释都不会输出
		--complete-insert, -c：insert语句中加上插入的列信息
		--create-options：在导出的建表语句中，加上所有的建表选项
		--tab=dir_name, -T dir_name：将每个表的结构定义和数据分别导出到指定目录下文件名同表名的.sql和
									 txt文件中，其中.txt文件中的字段分隔符是制表符。要求mysqldump必须
									 和MySQL Server在同一主机，且mysql用户对指定的目录有写权限，并且连								   接数据库的用户必须有file权限。且指定要dump的表，不能和--databases								  或--all-databases一起使用。它的实质是执行select into outfile。
		--fields-terminated-by=name：指定输出文件中的字段分隔符
		--fields-enclosed-by=name：指定输出文件中的字段值的包围符，如使用引号将字符串包围起来引用
		--fields-optionally-enclosed-by=name：指定输出文件中可选字段引用符
		--fields-escaped-by=name：指定输出文件中的转义符
		--lines-terminated-by=name：指定输出文件中的换行符   
		-Q, --quote-names：引用表名和列名时使用的标识符，默认使用反引号"`" 
	
	性能选项：
		--delayed-insert：对于非事务表，在insert时支持delayed功能，但在MySQL5.6.6开始该选项已经废弃
		--disable-keys, -K：在insert语句前后加上禁用和启用索引语句，大量数据插入时该选项很适合。默认开启
		--insert-ignore：使用insert ignore语句替代insert语句
		--quick, -q：快速导出数据，该选项对于导出大表非常好用。默认导出数据时会一次性检索表中所有数据并加入
					 到内存中，而该选项是每次检索一行并导出一行
	
	加锁和事务相关选项：
		--add-locks         
		#在insert语句前后加上lock tables和unlock tables语句，默认已开启。
		
		--flush-logs, -F 
		#在开始dump前先flush logs，如果同时使用了--all-databases则依次在每个数据库dump前flush，
		如果同时使用了--lock-all-tables,--master-data或者--single-transaction，则仅flush
		一次，等价于使用flush tables with read lock锁定所有表，这样可以让dump和flush在完全精
		确的同一时刻执行。
		
		--flush-privileges   
		#在dump完所有数据库后在数据文件的结尾加上flush privileges语句，在导出的数据涉及mysql库或
		者依赖于mysql库时都应该使用该选项
		
		--lock-all-tables, -x  
		#为所有表加上一个持续到dump结束的全局读锁。该选项在dump阶段仅加一次锁，一锁锁永久且锁所有。
		该选项自动禁用--lock-tables和--single-transaction选项
		
		--lock-tables, -l  
		#在dump每个数据库前依次对该数据库中所有表加read local锁(多次加锁，lock tables...read local)，
		这样就允许对myisam表进行并发插入。对于innodb存储引擎，使用--single-transaction比
		--lock-tables更好，因为它不完全锁定表。因为该选项是分别对数据库加锁的，所以只能保证每个数
		据库的一致性而不能保证所有数据库之间的一致性。该选项主要用于myisam表，如果既有myisam又有
		innodb，则只能使用--lock-tables，或者分开dump更好
		
		--single-transaction 
		#该选项在dump前将设置事务隔离级别为repeatable read并发送一个start transaction语句给
		服务端。该选项对于导出事务表如innodb表很有用，因为它在发出start transaction后能保证导
		出的数据库的一致性时而不阻塞任何的程序。该选项只能保证innodb表的一致性，无法保证myisam表
		的一致性。在使用该选项的时候，一定要保证没有任何其他连接在使用ALTER TABLE,CREATE TABLE,
		DROP TABLE,RENAME TABLE,TRUNCATE TABLE语句，因为一致性读无法隔离这些语句。
		--single-transaction选项和--lock-tables选项互斥，因为lock tables会隐式提交事务。
		要导出大的innodb表，该选项结合--quick选项更好
		
		--no-autocommit  
		#在insert语句前后加上SET autocommit = 0，并在需要提交的地方加上COMMIT语句
		
		--order-by-primary  
		#如果表中存在主键或者唯一索引，则排序后按序导出。对于myisam表迁移到innobd表时比较有用，但是
		这样会让事务变得很长很慢
	
	备份实例：
		MyISAM：温备，备份时要锁定表
			a.锁定所有库：		-x,--lock-all-tables：锁定所有库的所有表，读锁
			b.锁定正在备份的库：	  -l,--lock-tables：锁定指定库所有表
		InnoDB：支持温备和热备
			--single-transation：创建一个事务，基于此快照进行备份
			
		常用选项：
			-R,--routines：备份指定库的存储过程和存储函数
			--triggers：备份指定库的触发器
			-E,--events：
			--master-data[=NUM]
				NUM=1：记录为change master to语句，此语句不被注释
				--master-data=1
				CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000001',MASTER_LOG_POS=100;
				
				NUM=2：记录为change master to语句，此语句被注释
				--master-data=2
				--CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000001',MASTER_LOG_POS=100;
		
			-F,--flush-logs：锁定表完成后，即进行日志刷新操作，刷新到新文件
		
	    1.备份所有数据库 -A,--all-databases
			#备份所有库表，由于有myisam引擎表，需锁定库，可在备份文件头部看到二进制日志文件位置
			~]# mysqldump -uroot -p -hlocalhost -A -x -R --triggers -E --master-data=2 \
				--flush-logs > /tmp/alldb-$(date +%F).sql
			
			#恢复备份库,当数据全部丢失，通过 全量+二进制日志 恢复
			~]# mysqlbinlog node1-logbin.000005 > binlog-$(date +%F).sql  #拿到全备份后的二进制日志
			~]# mysql -uroot -p -hlocalhost < /tmp/alldb-2020-05-26.sql
			~]# mysql -uroot -p -hlocalhost < /tmp/binlog-2020-05-26.sql
	    
	    
		2.单个数据库备份与恢复-B,--databases
			#注意若是myisam引擎需要锁库温备，innodb加上--single-transation可以热备
			~]# mysqldump -uroot -p -hlocalhost -B test > /tmp/test_bak.sql
			~]# mysql -uroot -p -hlocalhost < /tmp/tset_bak.sql
			
			~]# mysqldump -uroot -p123456 -hlocalhost -B test | gzip > /tmp/tset_bak.sql.gz
			~]# mysqldump -uroot -p123456 -B test study | gzip > /tmp/mul_bak.sql.gz
			
			注:--compact 减少垃圾数据输出，适用于调试,恢复也是采用 全量+二进制日志
		
		
		3.单个数据库备份，不添加-B参数
			~]# mysqldump -uroot -p123456 test > /tmp/test_bak.sql
			~]# mysql -uroot -p123456 test < /tmp/test_bak.sql
			#过滤出备份内容如下，与添加-B区别为此备份不会有建库语句
			~]# egrep -v "#|\*|--|^$" /tmp/test_bak.sql   
				DROP TABLE IF EXISTS `student`;
				CREATE TABLE `student` (
				  `id` int(11) DEFAULT NULL,
				  `name` char(10) DEFAULT NULL
				) ENGINE=InnoDB DEFAULT CHARSET=utf8;
				LOCK TABLES `student` WRITE;
				INSERT INTO `student` VALUES (1,'zhang'),(2,'wang'),(3,'li'),(4,'liu');
				UNLOCK TABLES;
		
		4.分库备份
			~]# mysql -uroot -p123456 -e "show databases;" 2> /dev/null | grep -Evi "database|infor|perfor" | sed -r 's#^([a-z].*$)#mysqldump -uroot -p123456 -B \1 | gzip > /tmp/bak/\1_bak.sql.gz#' | bash
		
		5.分表备份
			test 库
			study student 表
			~]# mysqldump -uroot -p123456 test study student > /tmp/test_bak.sql
			
			备份表结构，没有数据
			test库，库后面可加一个或多个表
			~]# mysqldump -uroot -p123456 -d test > /tmp/test_bak.sql
			
			只备份数据
			test库，库后面可加一个或多个表
			~]# mysqldump -uroot -p123456 -t test > /tmp/test_bak.sql
		
		6.binlog备份与恢复
			数据备份但不能停止数据库时,-F 刷新binlog,--master-data=1不用刷新binlog，备份时会有记录。
			--single-transaction适合innoDB引擎
			~]# mysqldump -uroot -p123456 -B -F test > /tmp/test_bak.sql
			~]# mysqldump -uroot -p123456 -B --single-transaction --master-data=1 test > /tmp/test_bak.sql
			
			恢复
			#只是将test库中恢复的内容重定向到备份文件中，即可恢复数据库 
			~]# mysqlbinlog -d test mysql-bin.000020 > test_bak.sql 
			~]# mysql -uroot -p -hlocalhost < test_bak.sql
	        
	        #指定位置点恢复
			~]# mysqlbinlog mysql-bin.000020 --start-position=365 --stop-position=456 -r test_bak.sql 
			
			#指定时间点恢复
			~]# mysqlbinlog mysql-bin.000020 --satrt-datetime='2018-9-1 09:54:32' --stop-datetime='2018-9-1 09:54:33' -r test_bak.sql   		
			
		7.恢复总结
			1.利用source命令恢复数据库
				mysql> source /tmp/test_bak.sql
				
			2.利用mysql命令恢复数据库
				mysql -uroot -p123456 test < tset_bak.sql  #未加-B
				mysql -uroot -p123456 < tset_bak_B.sql  #加了-B选项
				
			3.批量恢复
				mysql_bak.sql
				study_bak.sql
				sys_bak.sql
				test_bak.sql
			
				~]# for dbname in `ls /tmp/bak | awk -F "_" '{print $1}'`; do mysql -uroot -p123456 < ${dbname}_bak.sql; done

## 10.4 xtrabackup

# 11. 主从复制
## 11.1 主从复制原理
[主从原理](https://www.cnblogs.com/f-ck-need-u/p/9155003.html#)

## 11.2 主从复制
**master：**

```c
1.开启master bin-log
    log-bin=mysql-log
	server-id=1  #这个必须不同
	skip_name_resolve=ON	#跳过名称解析
    
2.授权从库账号,用于从节点连接	
	mysql> grant replication slave on *.* to 'rep'@'192.168.%.%' identified by '960711';
	mysql> flush privileges;

3.若主库已有数据，需要先将主库数据备份到从库	
	mysql> flush table with read lock;  #只允许读数据，不允许写数据。
	注:锁表后数据库不能退出，备份可在新窗口进行
	
	mysql> show master status;    #查看bin-log文件和位置，用于从库同步起始位置
	~]# mysqldump -uroot -p --all-databases --master-data=2 > dump_all.db
	注:加上--master-data=2参数，可直接获取bin-log文件及位置，加-x参数，备份时自动锁表 
	
	mysql> unlock tables; #解锁
```

**slave：**

	1.开启中继日志
		relay_log=slave_log
		server-id=2		#与master不同
		skip_name_resolve=ON
	    
		注：relay_log.info用于记录SQL线程信息
	
	2.设置连接	
		mysql> CHANGE MASTER TO
			   MASTER_HOST='192.168.110.115',
			   MASTER_PORT=3306,
			   MASTER_USER='rep',
			   MASTER_PASSWORD='960711',
			   MASTER_LOG_FILE='mysql-bin.000003',
			   MASTER_LOG_POS=1452;
		#该信息会存放在master.info，用于记录IO线程信息中
			
	3.打开slave开关	
		mysql> start slave
			
	4.查看slave状态	
		mysql> show slave status\G;
			#若出现如下为成功:   
			   Slave_IO_Running: Yes
			   Slave_SQL_Running: Yes

**清除主从复制关系：**

```c
mysql> reset slave all;		#再删除所有二进制日志，中继日志及其索引文件
```

## 11.3 主主复制

**master-node1：**

```c
1.开启node1 二进制日志与中继日志
    log-bin=/var/log/mysql/node1-logbin
    relay-log=/var/log/mysql/node1-relay
	server-id=1  #这个必须不同
	skip_name_resolve=ON	#跳过名称解析
    
2.授权从库账号,用于从节点连接	
	mysql> grant replication slave on *.* to 'repnode1'@'192.168.%.%' identified by '960711';
	mysql> flush privileges;

2.设置连接,需要从服务器信息	
	mysql> CHANGE MASTER TO
		   MASTER_HOST='192.168.100.115',
		   MASTER_PORT=3306,
		   MASTER_USER='repnode2',
		   MASTER_PASSWORD='960711',
		   MASTER_LOG_FILE='node2.000001',
		   MASTER_LOG_POS=245;
	#该信息会存放在master.info，用于记录IO线程信息中
		
3.打开slave开关	
	mysql> start slave
		
4.查看slave状态	
	mysql> show slave status\G;
		#若出现如下为成功:   
		   Slave_IO_Running: Yes
		   Slave_SQL_Running: Yes
```

**master-node2：**

```c
1.开启node2 二进制日志与中继日志
    log-bin=/var/log/mysql/node2-logbin
    relay-log=/var/log/mysql/node2-relay
	server-id=2  #这个必须不同
	skip_name_resolve=ON	#跳过名称解析
    
2.授权从库账号,用于从节点连接	
	mysql> grant replication slave on *.* to 'repnode2'@'192.168.%.%' identified by '960711';
	mysql> flush privileges;

2.设置连接,需要主服务器信息	
	mysql> CHANGE MASTER TO
		   MASTER_HOST='192.168.100.114',
		   MASTER_PORT=3306,
		   MASTER_USER='repnode1',
		   MASTER_PASSWORD='960711',
		   MASTER_LOG_FILE='node1.000001',
		   MASTER_LOG_POS=245;
	#该信息会存放在master.info，用于记录IO线程信息中
		
3.打开slave开关	
	mysql> start slave
		
4.查看slave状态	
	mysql> show slave status\G;
		#若出现如下为成功:   
		   Slave_IO_Running: Yes
		   Slave_SQL_Running: Yes
```

**主主复制：**

```c
1.主从：两个节点都需要开启binlog和relaylog

2.增长id：若id为主键或唯一键
    定义一个节点使用奇数id：
		auto_increment_offset=1
        auto_increment_increment=2
    定义一个节点使用偶数id：
        auto_increment_offset=2
        auto_increment_increment=2

3.从服务器设定为"只读"
    在从服务器启动read_only，但仅对非super权限的用户有效
    
    阻止所有用户：
    	mysql> flush tables with read lock;

4.尽量确保复制时的事务安全
    在master节点启用参数
    	sync_binlog=ON		#事务实时刷新进二进制文件中，默认会先放在内存中
    
    如果用到的是innodb引擎：
    	innodb_flush_logs_at_trx_commit=ON
    	innodb_support_xa=ON
    
5.从服务器意外终止时尽量避免自动启动复制线程
    
6.从节点设置参数
    sync_master_info=ON		#从节点复制完成后立即同步到master.info中
    sync_relay_log_info=ON 

```

## 11.4 GTID复制

## 11.5 半同步复制
```c
半同步复制：主节点完成数据写入，且至少一个从节点也完成同步后，主节点返回写入成功，主从都需安装插件
```

**前提：已经做好主从复制**

**master：**

```c
mysql> show plugins;	#查看插件
mysql> install plugin rpl_semi_sync_master soname 'semisync_master.so';	#安装插件
    
mysql> show global variables like 'rpl_semi%';
+------------------------------------+-------+
| Variable_name                      | Value |
+------------------------------------+-------+
| rpl_semi_sync_master_enabled       | OFF   |
| rpl_semi_sync_master_timeout       | 10000 |
| rpl_semi_sync_master_trace_level   | 32    |
| rpl_semi_sync_master_wait_no_slave | ON    |
+------------------------------------+-------+
    
mysql> show global status like 'rpl_semi%';		#半同步复制的状态信息
+--------------------------------------------+-------+
| Variable_name                              | Value |
+--------------------------------------------+-------+
| Rpl_semi_sync_master_clients               | 0     |
| Rpl_semi_sync_master_net_avg_wait_time     | 0     |
| Rpl_semi_sync_master_net_wait_time         | 0     |
| Rpl_semi_sync_master_net_waits             | 0     |
| Rpl_semi_sync_master_no_times              | 0     |
| Rpl_semi_sync_master_no_tx                 | 0     |
| Rpl_semi_sync_master_status                | OFF   |
| Rpl_semi_sync_master_timefunc_failures     | 0     |
| Rpl_semi_sync_master_tx_avg_wait_time      | 0     |
| Rpl_semi_sync_master_tx_wait_time          | 0     |
| Rpl_semi_sync_master_tx_waits              | 0     |
| Rpl_semi_sync_master_wait_pos_backtraverse | 0     |
| Rpl_semi_sync_master_wait_sessions         | 0     |
| Rpl_semi_sync_master_yes_tx                | 0     |
+--------------------------------------------+-------+

mysql> set global rpl_semi_sync_master_enabled=on;	#启用半同步复制

```

**slave：需要半同步的从节点**

```c
mysql> install plugin rpl_semi_sync_slave soname 'semisync_slave.so';

mysql> show global variables like 'rpl%';
+---------------------------------+-------+
| Variable_name                   | Value |
+---------------------------------+-------+
| rpl_recovery_rank               | 0     |
| rpl_semi_sync_slave_enabled     | OFF   |
| rpl_semi_sync_slave_trace_level | 32    |
+---------------------------------+-------+

mysql> set global rpl_semi_sync_slave_enabled=on;    #启动半同步
    
注：若已经启动了从节点 IO线程，需重新启动一次 stop slave;
```

## 11.6 复制过滤

	复制过滤器：
	仅复制有限一个或几个数据库相关的数据，而非所有；由复制过滤器进行
	
	两种实现思路
	（1）主服务器
		主服务器仅向二进制日志中记录有关特定数据库相关的写操作
		问题：其他库的time-point recovery将无从实现；
		
			binlog_do_db=
			binlog_ignore_db=
			
	（2）从服务器
		从服务器的SQL THREAD仅重放关注的数据库或相关的事件，并将其应用于本地
		问题：网络IO和磁盘IO
		
			Replicate_Do_DB=					
			Replicate_Ignore_DB=
			
			Replicate_Do_Table=
			Replicate_Ignore_Table=
			
			Replicate_Wild_Do_Table=			#通配符指定表的白名单
			Replicate_Wild_Ignore_Table=

## 11.7 复制的监控与维护

**1.清理日志**

```c
mysql> purge {binary|master} logs {to 'log_name'|before datetime_expr};

mysql> purge binary logs to 'node1-logbin.000002'	#清楚000002之前的文件，不包含000002
```

**2.复制监控**

**master：**

```c
mysql> show master status;
+---------------------+----------+--------------+------------------+
| File                | Position | Binlog_Do_DB | Binlog_Ignore_DB |
+---------------------+----------+--------------+------------------+
| node1-logbin.000003 |      326 |              |                  |
+---------------------+----------+--------------+------------------+

mysql> show binlog events;
+---------------------+-----+-------------+-----------+-------------+----------------------+
| Log_name            | Pos | Event_type  | Server_id | End_log_pos | Info                                      |
+---------------------+-----+-------------+-----------+-------------+----------------------+
| node1.000001 |   4 | Format_desc |         1 |         245 | 5.5.65-MariaDB, Binlog ver: 4 |
| node1.000001 | 245 | Query       |         1 |         326 | create database rep                       |
| node1.000001 | 326 | Stop        |         1 |         345 |                                           |
+---------------------+-----+-------------+-----------+-------------+----------------------+

mysql> show binary logs;
+---------------------+-----------+
| Log_name            | File_size |
+---------------------+-----------+
| node1-logbin.000001 |       345 |
| node1-logbin.000002 |       264 |
| node1-logbin.000003 |       326 |
+---------------------+-----------+
```

**slave：**

```c
mysql> show slave status\G;
	   ...
       Seconds_Behind_Master=0			#判断从服务器是否落后于主服务器
	   ...

```

**3.如何确定主从数据一致**

```c
1.通过表的CHECKSUM检查
2.使用percona-toolkit工具中的 pt-table-checksum 检查
  https://www.percona.com/software/database-tools/percona-toolkit
```

**4.主从数据不一致修复**

```c
重新复制
```

# 12. 读写分离

```c

```



# 13. 高可用

	~]# cat /etc/my.cnf
		[mysqld]
		server-id                          = 1
		
		basedir                            = /usr/local/mysql
		datadir                            = /usr/local/mysql/var/db
		innodb_data_home_dir               = /usr/local/mysql/var/innodb
		innodb_log_group_home_dir          = /usr/local/mysql/var/innodb
		log-bin                            = /usr/local/mysql/var/replication/binary-log
		log-error                          = /usr/local/mysql/var/log/mysqld.log
		master_info_file                   = /usr/local/mysql/var/replication/master.info
		pid-file                           = /usr/local/mysql/var/run/mysqld.pid
		relay_log                          = /usr/local/mysql/var/replication/relay-log
		relay_log_info_file                = /usr/local/mysql/var/replication/relay-log.info
		relay_log_index                    = /usr/local/mysql/var/replication/relay-log.index
		slow_query_log_file                = /usr/local/mysql/var/log/slow_query.log
		socket                             = /usr/local/mysql/var/run/mysqld.sock
		tmpdir                             = /usr/local/mysql/var/tmp
		
		innodb_additional_mem_pool_size    = 16M
		innodb_autoextend_increment        = 256
		innodb_buffer_pool_instances       = 12
		innodb_buffer_pool_size            = 24G                                                                                                                                                                                                                                       
		innodb_concurrency_tickets         = 5000                                                                                                                                                                                                                                      
		innodb_data_file_path              = ibdata1:1G:autoextend                                                                                                                                                                                                                     
		innodb_file_format                 = Barracuda                                                                                                                                                                                                                                 
		innodb_file_per_table              = 1                                                                                                                                                                                                                                         
		innodb_flush_log_at_trx_commit     = 2                                                                                                                                                                                                                                         
		innodb_flush_method                = O_DIRECT                                                                                                                                                                                                                                  
		innodb_log_file_size               = 512M                                                                                                                                                                                                                                      
		innodb_log_files_in_group          = 4                                                                                                                                                                                                                                         
		innodb_old_blocks_time             = 1000
		innodb_open_files                  = 2048
		innodb_stats_on_metadata           = OFF 
		
		large-pages
		binlog-row-event-max-size          = 8192
		binlog-format                      = MIXED
		character_set_server               = utf8
		collation_server                   = utf8_bin
		expire_logs_days                   = 1
		join_buffer_size                   = 262144
		max_allowed_packet                 = 32M
		max_connect_errors                 = 10000
		max_connections                    = 2500
		max_heap_table_size                = 134217728
		port                               = 3306
		query_cache_type                   = 0
		query_cache_size                   = 0
		slow-query-log                     = ON
		table_open_cache                   = 2048
		thread_cache_size                  = 64
		tmp_table_size                     = 134217728
		user                               = mysql
		wait_timeout                       = 86400
		
		[client]
		port                               = 3306
		socket                             = /usr/local/mysql/var/run/mysqld.sock	