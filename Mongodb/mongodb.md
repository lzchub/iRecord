# 1. MongoDB安装

## 1.1 yum安装

```c
~]# cat /etc/yum.repos.d/mongodb-org.repo
    [mongodb-org] 
    name = MongoDB Repository
    baseurl = https://mirrors.aliyun.com/mongodb/yum/redhat/$releasever/mongodb-org/3.6/x86_64/
    gpgcheck = 1 
    enabled = 1 
    gpgkey = https:// www.mongodb.org/static/pgp/server-3.6.asc

~]# yum install -y mongodb-org-server mongodb-org-shell mongodb-org-tools
~]# cat /etc/mongod.conf | grep -vE "#|^$"
    systemLog:
      destination: file
      logAppend: true
      path: /var/log/mongodb/mongod.log
    storage:
      dbPath: /data/mongodb
      journal:
        enabled: true
    processManagement:
      timeZoneInfo: /usr/share/zoneinfo
    net:
      port: 27017
    
~]# mkdir -pv /data/mongodb
~]# chown mongod:mongod /data -R
    
~]# systemctl start mongod
```

# 2. CRUD操作

```c
~]# mongo --host 127.0.0.1		#默认登录在test库
    
帮助
> help
> help.mycoll.help()
```

## 2.1 Create

```c
> use stu		#延迟创建数据库，当有数据生成就自动生成库
> db.student.insert({name:"zhangsan",age:55,sex:"M"})		#插入一条数据
    
> show dbs		#插入数据后，库已经生成
  admin   0.000GB
  config  0.000GB
  local   0.000GB
  stu     0.000GB    
    
> show collections 	#可以理解为表
  student
```

## 2.2 Read

```c
> db.student.find()		#查询当前collection所有数据
> db.student.find().pretty()	#结果以json格式显示

find比较操作：
    > db.student.find({age:{$gt: 50}})		#大于
    > db.student.find({age:{$gte: 55}})		#大于等于
    > db.student.find({age:{$lt: 55}})		#小于
    > db.student.find({age:{$lte: 55}})		#小于等于
    > db.student.find({age:{$eq: 55}})		#等于
    > db.student.find({age:{$ne: 55}})		#不等于

find逻辑运算：
    > db.student.find({$or:[{name:"lisi"},{age:{$lt:25}}]})		#or
    > db.student.find({$and:[{sex:"M"},{age:{$lt:25}}]})		#and
	
find type查找：https://www.runoob.com/mongodb/mongodb-operators-type.html
    > db.student.find({age:{$type:1}})		#与下条等同
    > db.student.find({age:{$Type:"double"}})
```

## 2.3 Update

```c
> db.student.update({name:"zhangsan"},{$set:{age:36}})		#修改zhangsan的age字段
> db.student.update({name:"zhangsan"},{$unset:{age:36,sex:"M"}})    #删除zhangsan的age、sex字段
> db.student.update({age:55},{$set:{sex:"G"}},{multi:true})		#当有多个匹配项时，默认只会修改匹配到的第一个，加此参数全部修改   
    
> db.student.save({"_id":ObjectId("5f3df4c027519270934ecb5d"),name:"test",age:66})    	#替换某一个id的数据
```

## 2.4 Delete

```c
> db.student.remove({age:{$gte:55}})		#移除age大于等于55的数据，默认是匹配到的都删除
> db.student.remove({age:{$gte:55}},{justOne:true})		#只删除匹配到的第一个
```

## 2.5 其他操作

```c
use stu		#进入stu库
db.stats()	#查看stu库信息
db.student.stats()	#查看stu库student collection信息
db.student.drop()	#删除stu库student collection
db.dropDatabase()    #删除stu库 
```

# 3. 索引

```
1.单列索引
2.组合索引
3.多键索引：文档中有子文档的时候
4.空间索引
5.全文索引
6.hash索引
```

```c
创建单列索引：
    > use stu
    > for(i=0;i<10000;i++) db.student.insert({name:"student_"+i,age:(i%99),sex:(i%2)})
    > db.student.ensureIndex({name:1})		# 1表示以升序创建索引，-1降序
    > db.student.getIndexes()				#得到coll下所有索引
    > db.student.dropIndex("name_1")		#删除索引
    > db.student.dropIndexes()				#删除当前coll下所有索引  
        
创建唯一索引：
    > db.student.ensureIndex({name:1},{unique:ture})			#创建唯一索引
```

# 4. 用户管理

| **Read**                 | 允许用户读取指定数据库                                       |
| ------------------------ | :----------------------------------------------------------- |
| **readWrite**            | 允许用户读写指定数据库                                       |
| **dbAdmin**              | 允许用户在指定数据库中执行管理函数，如索引创建、删除，查看统计或访问system.profile |
| **userAdmin**            | 允许用户向system.users集合写入，可以找指定数据库里创建、删除和管理用户 |
| **clusterAdmin**         | 只在admin数据库中可用，赋予用户所有分片和复制集相关函数的管理权限。 |
| **readAnyDatabase**      | 只在admin数据库中可用，赋予用户所有数据库的读权限            |
| **readWriteAnyDatabase** | 只在admin数据库中可用，赋予用户所有数据库的读写权限          |
| **userAdminAnyDatabase** | 只在admin数据库中可用，赋予用户所有数据库的userAdmin权限     |
| **dbAdminAnyDatabase**   | 只在admin数据库中可用，赋予用户所有数据库的dbAdmin权限。     |
| **root**                 | 只在admin数据库中可用，超级账号，超级权限                    |

```c
用户创建语法:
{
  user: "<name>", 
  pwd: "<cleartext password>", 
  customData: { <any information> }, 
  roles: [ 
    { role: "<role>", db: "<database>" } | "<role>", 
	... 
  ] 
}

语法说明：
    user字段：用户的名字;
    pwd字段：用户的密码;
    cusomData字段：为任意内容，例如可以为用户全名介绍;
    roles字段：指定用户的角色，可以用一个空数组给新用户设定空角色；
    roles 字段：可以指定内置角色和用户定义的角色。
```

## 4.1 创建用户

### 1.创建管理员用户

```c
#进入管理数据库
> use admin

#创建管理用户，root权限
> db.createUser(
  {
    user: "root",
    pwd: "root",
    roles: [ { role: "root", db: "admin" } ]
  }
  )    

注意：
    1.创建管理员角色用户的时候，必须到admin下创建。
    2.删除的时候也要到相应的库下操作。

#查看创建完用户后的collections；
> show tables; 
  system.users  # 用户存放位置
  system.version
      
#查看创建的管理员用户
> show users
  {
      "_id" : "admin.root",
      "user" : "root",
      "db" : "admin",
      "roles" : [
          {
              "role" : "root",
              "db" : "admin"
          }
      ]
  }

# 验证用户是否能用
> db.auth("root","root")
  1  # 返回 1 即为成功
```

### 2.创建对某库的只读用户

```c
# 在test库创建只读用户test
> use test
> db.createUser(
  {
    user: "test",
    pwd: "test",
    roles: [ { role: "read", db: "test" } ]
  }
  )

# 测试用户是否创建成功
> db.auth("test","test")
> show  users

# 登录test用户，并测试是否只读
~]# mongo --host 127.0.0.1 --port 27017 -utest -ptest stu    
> show collections
> db.createCollection('b')	#会无法创建
```

### 3.**创建某库的读写用户**

```
# 创建test1用户，权限为读写
> db.createUser(
  {
    user: "test1",
    pwd: "test1",
    roles: [ { role: "readWrite", db: "test" } ]
  }
  )

# 查看并测试用户
> show users;
> db.auth("test1","test1")
```

### 4.**创建对多库不同权限的用户**

```
# 创建对app为读写权限，对test库为只读权限的用户
> use app
> db.createUser(
  {
    user: "app",
    pwd: "app",
    roles: [ { role: "readWrite", db: "app" },
             { role: "read", db: "test" }
    ]
  }
  )

# 查看并测试用户
> show users
> db.auth("app","app")
```

### 5.**删除用户**

```
# 删除app用户：先登录到admin数据库
~]# mongo -uroot –proot 127.0.0.1/admin

# 进入app库删除app用户
~]# use app
~]# db.dropUser("app")

```

### 6.命令行中进行登陆

**方法一：登录时验证**

```
~]$ mongo -uroot -proot admin 
    MongoDB shell version: 3.2.8
    connecting to: admin

```

**方法二：在数据库中进行登陆验证**

```
~]$ mongo 
    MongoDB shell version: 3.2.8
    connecting to: test
    > use admin
    switched to db admin
    > db.auth("root","root")
    1
    > show tables;
    system.users
    system.version
```

### 7.查看当前mongo客户端链接数

```c
> db.serverStatus().connections
```

## 4.2 集群启用用户认证

```c
1.修改配置文件/etc/mongod.conf
  security:
    authorization: enabled
    keyFile: /data/mongodb/mongokey.file	#集群模式需要额外添加此行配置，用于集群内认证

2.创建认证文件
	~]# openssl rand -base64 756 > /data/mongodb/mongokey.file	#所有mongo节点上都需要放置此文件
	~]# chmod 400 /data/mongodb/mongokey.file		#必须要给予此权限，否则会报错
    ~]# rm -f /data/mongodb/mongo.lock		#若是集群中途添加认证功能，需删除此文件，否则报错
 
3.重启服务
    ~]# systemctl restart mongod    
        
说明：可以先开启认证重启后再添加用户。但是只能在admin库添加一次，所以如果忘记了，或者权限分配不恰当就无法再更改，所以建议先添加用户再开启认证重启，并且集群不建议在每个单节点添加用户，并且建议单节点关闭初始添加账号的权限，详情见enableLocalhostAuthBypass)
        
```



# 5. MongoDB复制

```c
分类：
    1.主从	master/slave
    2.复制集	replica set
```

## 5.1 复制集(replica set)

```c
主节点将数据修改操作保存在oplog中，集群节点至少为3个，且应该为奇数个节点，从节点每2s会向主节点发送心跳信息，通过选举出主节点
    
复制集节点分类：
    0优先级的节点：冷备节点，不会被选举成主节点，但能参加选举
    被隐藏的从节点：首先是一个0优先级的节点，除此外对客户端不可见
	延迟复制的节点：首先是一个0优先级的节点，且复制时间落后于主节点一个固定市场
    arbiter：无任何权限，用于节点仲裁
    
oplog：
    大小固定的文件，存储在local数据库中
    	初始同步
    	回滚后追赶
    	切分块迁移
    
    local库：存放了副本集的所有元数据和oplog;用于存储oplog的是一个名为oplog.rs的collection，oplog大小依赖于OS与文件系统，				当然可以手动指定
    
Mongo的数据同步类型：
    初始同步：
        节点没有任何数据时
        节点丢失副本复制历史
        
       	初始同步的步骤：
        	1.克隆所有数据库
        	2.应用数据集的所有改变
        	3.为所有collection构建索引
        
    复制：      
```

**复制集配置：**

```c

~]# cat /etc/mongod.conf		#3个节点使用相同配置,IP按需修改
    ...
    replication:
       replSetName: "reptestdb" # 设置复制集名称
    ...
           
#主节点配置复制集           
> config = {_id:'rs0',members:[
    {_id:0,host: '192.168.240.21:27017'},
    {_id:1,host: '192.168.240.21:28018'},
    {_id:2,host: '192.168.240.21:29019'}
]}
> rs.initiate(config)           
{
        "ok" : 1,
        "operationTime" : Timestamp(1562308842, 1),
        "$clusterTime" : {
                "clusterTime" : Timestamp(1562308842, 1),
                "signature" : {
                        "hash" : BinData(0,"AAAAAAAAAAAAAAAAAAAAAAAAAAA="),
                        "keyId" : NumberLong(0)
                }
        }
}           

#从节点确认ok
> rs.slaveOk()
    
#主节点给某个从节点设定优先级
> cfg=rs.conf()
> cfg.members[1].priority=2
> rs.reconfig(cfg)		#重新载入配置
    
#主节点添加仲裁节点
> rs.addArb()		#直接添加为仲裁节点，节点不会同步数据

> cfg=rs.conf()		#将从节点转换为仲裁节点
> cfg.members[1].arbiterOnly=true
> rs.reconfig(cfg)

```

**复制集常用管理操作**

**查看复制集状态：**

```
rs.isMaster()
rs.status()
```

**查看复制集配置：**

```
rs.config()
```

**添加普通节点：**

```
rs.add("ip:port")
```

**删除一个节点：**

```
rs.remove("ip:port")
```

**新增仲裁节点：**

```
rs.addArb("ip:port")
```

**调整副本集优先级（优先级为0的节点，无法成为主节点）：**

```
cfg = rs.conf()
cfg.members[0].priority = 0.5
cfg.members[1].priority = 2
cfg.members[2].priority = 2
rs.reconfig(cfg)
```

**配置非投票节点（votes和priority必须为0）：**

```
cfg = rs.conf();
cfg.members[3].votes = 0; 
cfg.members[3].priority = 0;
rs.reconfig(cfg);
```

**更改Oplog大小：**

```
use local
db.oplog.rs.stats().maxSize
db.adminCommand({replSetResizeOplog: 1, size: 16000})
```

**重新触发选主：**

```
rs.stepDown()
```

**一段时间内不能成为主：**

```
rs.freeze(120)
```

**启用链式复制：**

```
cfg = rs.config()
cfg.settings.chainingAllowed = true
rs.reconfig(cfg)
```

**副本重新选举的影响条件：**

```c

1.心跳信息
2.优先级
3.optime：与主节点同步的时间差
4.网络连接

```

# 6. MongoDB分片

```c
分片架构中的角色：
    mongos：Router
    config server：元数据服务器
    shard：数据节点，也称mongo实例

分片类型：
    1.基于范围分片
    	对于顺序的索引
    2.基于列表切片
    	离散指定分片，对于不是顺序的索引
    3.基于hash切片
    
    目标：写离散，读集中
```

参考文档：https://www.cnblogs.com/clsn/archive/2004/01/13/8214345.html#auto-id-22

# 7. MongoDB的备份与恢复

## 7.1 mongoexport/mongoimport

### 1.mongoexport导出

Mongodb中的mongoexport工具可以把一个**collection**导出成JSON格式或CSV格式的文件。可以通过参数指定导出的数据项，也可以根据指定的条件导出数据。

**mongoexport参数：**

| **参数**                     | **参数说明**                           |
| ---------------------------- | -------------------------------------- |
| **-h**                       | 指明数据库宿主机的IP                   |
| **-u**                       | 指明数据库的用户名                     |
| **-p**                       | 指明数据库的密码                       |
| **-d**                       | 指明数据库的名字                       |
| **-c**                       | 指明collection的名字                   |
| **-f**                       | 指明要导出那些列                       |
| **-o**                       | 指明到要导出的文件名                   |
| **-q**                       | 指明导出数据的过滤条件                 |
| **--type**                   | 指定文件类型                           |
| **--authenticationDatabase** | 验证数据的名称，即备份用户所在的数据库 |

**导出collection，默认为json格式**：

```c
~]# mongoexport --host 192.168.100.56 --port 27017 -uroot -proot --authenticationDatabase admin -d stu -c student -o ./stu.json		#必须要指定某个库某个collection
    
~]# cat stu.json 
    {"_id":{"$oid":"5f472c4409e15f31303ae939"},"name":"zhangsan","age":55.0,"sex":"M"}
    {"_id":{"$oid":"5f653456ed046b4d2fd989b7"},"name":"lisi","age":22.0,"sex":"M"}
    
~]# mongoexport --host 192.168.100.56 --port 27017 -utest -ptest --authenticationDatabase stu -d stu -c student -o ./stu2.json
```

---

**导出collection，为csv格式**：

```c
~]# mongoexport -h 10.0.0.152:27017 -uroot -proot --authenticationDatabase admin  -d stu -c student --type=csv -f name,age -o student.csv		#导出为csv格式必须要指定列名
    
~]# cat student.csv 
    name,age
    zhangsan,55
    lisi,22
```

---

### 2.mongoimport导入

Mongodb中的mongoimport工具可以把一个特定格式文件中的内容导入到指定的collection中。该工具可以导入JSON格式数据，也可以导入CSV格式数据。

**mongoimport参数：**

| **参数**                     | **参数说明**                          |
| ---------------------------- | ------------------------------------- |
| **-h**                       | 指明数据库宿主机的IP                  |
| **-u**                       | 指明数据库的用户名                    |
| **-p**                       | 指明数据库的密码                      |
| **-d**                       | 指明数据库的名字                      |
| **-c**                       | 指明collection的名字                  |
| **-f**                       | 指明要导出那些列                      |
| **-o**                       | 指明到要导出的文件名                  |
| **-q**                       | 指明导出数据的过滤条件                |
| **--drop**                   | 插入之前先删除原有的                  |
| **--headerline**             | 指明第一行是列名，不需要导入。        |
| **-j**                       | 同时运行的插入操作数（默认为1），并行 |
| **--authenticationDatabase** | 验证数据的名称                        |

**json格式导入：**

```c

~]# mongoimport --host 192.168.100.57 --port 27017 -uroot -proot --authenticationDatabase admin -d stu -c student --drop stu2.json 
```

**csv格式导入：**

```c
~]# mongoimport -h 10.0.0.152:27017 -uroot -proot --authenticationDatabase admin -d stu -c student --type=csv --headerline --file student.csv
```

## 7.2 mongodump/mongorestore

### 1.mongodump导出

**mongodump参数：**

| **参数**                     | **参数说明**                                  |
| ---------------------------- | --------------------------------------------- |
| **-h**                       | 指明数据库宿主机的IP                          |
| **-u**                       | 指明数据库的用户名                            |
| **-p**                       | 指明数据库的密码                              |
| **-d**                       | 指明数据库的名字                              |
| **-c**                       | 指明collection的名字                          |
| **-o**                       | 指明到要导出的文件名                          |
| **-q**                       | 指明导出数据的过滤条件                        |
| **--authenticationDatabase** | 验证数据的名称                                |
| **--gzip**                   | 备份时压缩                                    |
| **--oplog**                  | use oplog for taking a point-in-time snapshot |

**全库备份：**

```
# 备份为目录，目录下为库(目录)，库下为collection
~]# mongodump -h 10.0.0.152:27017 -uroot -proot --authenticationDatabase admin  -o /root/backup/all
```

**备份stu库：**

```
# 备份为目录，以库名命名，下为collection
~]# mongodump -h 10.0.0.152:27017 -uroot -proot --authenticationDatabase admin  -d stu -o /root/backup/db
```

**备份stu库下的student集合：**

```
# collection备份出来也是目录
~]# mongodump -h 10.0.0.152:27017 -uroot -proot --authenticationDatabase admin  -d stu -c student -o /root/backup/coll
```

```
~]# tree .
.
├── all
│   ├── admin
│   │   ├── system.users.bson
│   │   ├── system.users.metadata.json
│   │   ├── system.version.bson
│   │   └── system.version.metadata.json
│   └── stu
│       ├── student.bson
│       └── student.metadata.json
├── coll
│   └── stu
│       ├── student.bson
│       └── student.metadata.json
└── db
    └── stu
        ├── student.bson
        ├── student.metadata.json
        ├── teachername.bson
        └── teachername.metadata.json
```

**压缩备份库：**

```
~]# mongodump -h 10.0.0.152:27017 -uroot -proot --authenticationDatabase admin  -d test -o /home/mongod/backup/ --gzip
```

**压缩备份单表：**

```
mongodump -h 10.0.0.152:27017 -uroot -proot --authenticationDatabase admin  -d test -c vast -o /home/mongod/backup/ --gzip
```

### 2.mongorestore导入

**mongorestore参数：**

| **参数**                     | **参数说明**                                  |
| ---------------------------- | --------------------------------------------- |
| **-h**                       | 指明数据库宿主机的IP                          |
| **-u**                       | 指明数据库的用户名                            |
| **-p**                       | 指明数据库的密码                              |
| **-d**                       | 指明数据库的名字                              |
| **-c**                       | 指明collection的名字                          |
| **-o**                       | 指明到要导出的文件名                          |
| **-q**                       | 指明导出数据的过滤条件                        |
| **--authenticationDatabase** | 验证数据的名称                                |
| **--gzip**                   | 备份时压缩                                    |
| **--oplog**                  | use oplog for taking a point-in-time snapshot |
| **--drop**                   | 恢复的时候把之前的集合drop掉                  |

**全库备份中恢复单库（基于之前的全库备份）：**

```
~]# mongorestore -h 10.0.0.152:27017 -uroot -proot --authenticationDatabase admin --drop  /root/backup/all/
```

**恢复stu库：**

```
~]# mongorestore -h 10.0.0.152:27017 -uroot -proot --authenticationDatabase admin -d stu --drop /root/backup/db/
```

**恢复stu库下的student集合：**

```
~]# mongorestore -h 10.0.0.152:27017 -uroot -proot --authenticationDatabase admin -d stu -c student /root/backup/coll/stu/student.bson		#恢复集合必须指定文件，若不使用--drop参数，比配置文件多余的数据不会被清除
```

**--drop参数实践恢复：**

```
# 恢复单库
~]# mongorestore -h 10.0.0.152:27017 -uroot -proot --authenticationDatabase admin -d stu --drop /root/backup/db/
# 恢复单表
~]# mongorestore -h 10.0.0.152:27017 -uroot -proot --authenticationDatabase admin -d stu -c student --drop /root/backup/coll/stu/student.bson
```

## 7.3 mongoexport/mongoimport与mongodump/mongorestore的对比

* mongoexport/mongoimport导入/导出的是JSON格式，而mongodump/mongorestore导入/导出的是BSON格式。

* JSON可读性强但体积较大，BSON则是二进制文件，体积小但对人类几乎没有可读性。

* 在一些mongodb版本之间，BSON格式可能会随版本不同而有所不同，所以不同版本之间用mongodump/mongorestore可能不会成功，具体要看版本之间的兼容性。当无法使用BSON进行跨版本的数据迁移的时候，使用JSON格式即mongoexport/mongoimport是一个可选项。跨版本的mongodump/mongorestore并不推荐，实在要做请先检查文档看两个版本是否兼容（大部分时候是的）。

* JSON虽然具有较好的跨版本通用性，但其只保留了数据部分，不保留索引，账户等其他基础信息。使用时应该注意。

* mongoexport/mongoimport只适用导入导出collection，而mongodump/mongorestore适用于全库、单库、集合的备份与恢复。

## 7.4 参考文档

https://www.cnblogs.com/clsn/p/8244206.html

# 8. MongoDB监控

https://www.cnblogs.com/clsn/p/8244206.html

# 9. MongoDB集群性能优化

https://www.cnblogs.com/clsn/p/8244206.html