# 1.安装配置
官网：http://saltsatck.com
官方仓库：http://repo.saltstack.com

实验：关闭防火墙，selinux
```
~]# yum install https://repo.saltstack.com/yum/redhat/salt-repo-latest-2.el7.noarch.rpm 
~]# yum clean expire-cache
~]# yum install salt-master salt-minion

配置minion：只需安装salt-minion即可
~]# vim /etc/minion
	master:MASTER_IP
	id:				#默认为主机名，minion启动后，id不可轻易修改

配置master：
~]# systemctl start salt-master
~]# systemctl start salt-minion

~]# salt-key -L
~]# salt-key -A	-y	#master添加所有minion,salt使用ssl签证方式进行安全验证

```
# 2.saltstack基础使用

```
1. 获取所有远程命令模块
	~]# salt "m*" sys.list_modules 
2. 获取模块所有方法列表
	~]# salt master* sys.list_functions file
3. 获取模块信息
	`]# salt master* sys.doc file
4. 获取模块对应方法信息
	~]# salt master* sys.doc file.chown
	
节点分组：nodegroups
    ~]# vim /etc/salt/master		#修改完需要重启
        nodegroups:
        web: 'L@node1.chuan.com,node2.chuan.com'
    ~]# salt -N web test.ping  

```

# 3.salt命令参数解析

```
Usage: salt [options] '<target>' <function> [arguments]

options:
	-V, --versions-report：查看salt及其依赖版本信息
	-v, --verbose：开启命令的详细描述
	--summary：显示一条salt命令的摘要，如成功多少失败多少..
	--out：定义输出格式，可取（json，yaml，raw，quiet，nested）

target:
	1.全局匹配：
		*:代表任意字符串，也可以是空字符串
		?:代表一个字符，但不能为空
		[]:字符集合，[a-z]一个字符,[0-9]一个数字

	2.正则匹配：-E --pcre
		~]# salt -E ".*com$" test.ping

	3.列表匹配：-L --list 
		~]# salt -L "node1.chuan.com node2.chuan.com" cmd.run_all "echo hello"
	
	4.grains：-G
		~]# salt -G 'os:Ubuntu' test.version	#目标可以基于使用Grains系统的minion系统信息进行过滤
		
		自定义grains方法：
			1.修改/etc/salt/minion配置文件grains字段 
				grains:									
                  roles:
                    - webserver
                    - memcache
            2.直接将配置写入/etc/salt/grains文件         
                roles:
                  - webserver
                  - memcache
			3.利用grains模块定义
				~]# salt 'm*' grains.setval cpu_num 8	#会保存为grains文件
				~]# salt 'm*' grains.setvals cpu_info '["Intel","Xen",8]'	#以列表的形式定义
				~]# salt 'm*' grains.item cpu_info	#查询信息
				~]# salt 'm*' grains.delval cpu_info	#删除自定义grains，只是删除value，key还是存在，赋值为none
				~]# salt 'salt-min*' grains.append name 'node2'	#当前名称后追加值，可以多次追加
		
			定义好后刷新或者重启minion：
				~]# salt-minion saltutil.refresh_modules	#刷新minion配置
		
			4.查看grains
				~]# salt 'SCYD-10.1.33.81' grains.ls			#查看grains名称
				~]# salt 'SCYD-10.1.33.81' grains.items			#查看grains名称和值
				~]# salt 'SCYD-10.1.33.81' grains.get roles		#查看对应grains名称和值
				
				~]# salt-call grains.append roles idle
			
		静态数据，当minion启动时收集的Minion本地的相关信息。如操作系统版本，内核版本，CPU，内存，硬盘，设备型号，序列号等
		~]# salt "m*" grains.items	#查看所有grains信息
		~]# salt "m*" grains.item os	#查看某一项
		~]# salt -G "os:CentOS" test.ping	#对os为centos的机器进行操作，grains里面的信息都可以使用 --grain 
		~]# salt -G "os:C*" test.ping   #也可匹配
		
		top.sls使用：
			'os:CentOS':
			  - match: grain
			  - web.apache
			
	5.pillar：同grains，只是pillar可以定义为更加动态的形式，修改master pillar_opts参数启用，pillar_roots设置目录
		~]# salt -I 'key:value' test.ping
		
		设置pillar：使用sls文件定义，可以多层级定义
			如：
				a:
				  b:
 				    c: value

			~]# mkdir /srv/pillar -pv && cd /srv/pillar

			~]# cat master.sls 
				role: master
				
			~]# cat node.sls
				role: slave

			~]# cat top.sls 
                base:
                  'master.chuan.com':
                    - master
                  'node1.chuan.com':
                    - node
                  'node2.chuan.com':
                    - node
			
			~]# salt '*' saltutil.refresh_pillar
			~]# salt '*' pillar.items

	6.复合匹配：支持and，or，not，@符号规定每部分匹配的类型，前面的类型均可使用
		~]# salt -C 'node* and G@os:CentOS not E@.*' test.ping
		~]# salt -C 'm* or n* not E@.*1.*' test.ping  
		
	7.CIDR匹配
		~]# salt -S '192.168.100.0/24' test.ping

		
function：列出常用 module.function，所有模块文件在/lib/python2.7/site-packages/salt/modules/目录下
	1.远程命令执行模块：cmd
		cmd.run：执行命令
			 ~]# salt m* cmd.run 'echo hello' 
		cmd.rum_all：执行命令，输出详细信息
			~]# salt '*' cmd.run_all 'ps aux|wc -l'

	2.安装包管理模块：pkg
		pkg.install：安装软件
			~]# salt *1* pkg.install 'httpd'
		pkg.info_installed：查看安装信息
			~]# salt *1* pkg.info_installed 'httpd' 
		pkg.version:查看版本
			~]# salt *1* pkg.version 'httpd' 
		pkg.remove：移除
			~]# salt *1* pkg.remove 'httpd'

	3.管理服务模块：service
		service.status：状态信息	
			~]# salt node* service.status 'httpd'
		service.start
		service.stop
		service.enable
		service.disable

	4.文件管理模块：file
		file.stats：文件信息查询
			~]# salt '*' file.stats '/etc/fstab' 
		file.chown：修改文件权限
		file.managed：复制文件到minion
		file.directory：建立目录
		file.symlink：建立软连接
		file.recurse：下发整个目录

	5.用户管理模块：user
		user.add：添加用户
		user.delete：删除用户
		user.info：用户信息		

	6.定时计划模块：cron
		cron.present：制定定时任务

	7.内核配置模块：sysctl
		sysctl.present：调整内核参数

	8.pip模块：
		pip.installed：安装python模块

注意：具体参数可到官网查看
```
# 4.自定义模块

```
modules:
	~]# mkdir /srv/salt/_modules -pv
	~]# vim /srv/salt/_modules/hello.py
		def world():
		    """
		    This is my first function.
		    CLI Example::       
		        salt '*' hello.world
		    """
		
		    return 'Hello,world!'
                       
	~]# salt '*' saltutil.sync_modules	#将写好的模块文件推送到minion
	~]# salt '*' hello.world	#即可使用

grains_modules:
	~]# mkdir /srv/salt/_grains -pv
	~]# vim /srv/salt/my_grains.py
		import time
		def now():
		    grains = {}
		    grains['now'] = time.time()
		    return grains
	~]# salt '*' saltutil.sync_grains
	~]# salt '*' grains.item now
	~]# salt '*' grains.delval my_grains

```

# 5.状态配置文件书写及注意
**基础事项：**

```
注意：
	1.状态配置文件必须以 .sls为后缀
	2.默认base环境为/srv/salt，可修改master配置文件修改
	3.使用state.sls执行
	4.使用yaml格式书写
	5.状态模块与前面的远程命令模块略有不同

查看所有状态模块：
	~]# salt m* sys.list_state_modules
查看模块方法列表：
	~]# salt m* sys.list_state_functions MODULE

```
**状态文件书写规则**
```
~]# vim test.sls	#在/srv/salt目录下
<ID declaration>
  <state module>.<function>:
    - name: <name>
    - <function arg>
    - ...
    - <function arg>
    - <requisite declaration>
      - <requisite reference>

注意：
	1.每个id下，一个模块只能用一次
	2.若不写name，则id为name
	3.默认从上往下执行

~]# salt '*' state.sls test		#执行状态
~]# salt '*' state.sls dir.test		#dir为test的父目录，即为/srv/salt/dir/test/sls

后面会介绍使用top.sls执行
```

# 6.jinja2模板

```
变量使用 	{{}}
	{{var}}
表达式使用	{% %}
	{% set var='good' %}
```

参考文档：http://docs.jinkan.org/docs/jinja2/

# 7.实例解析

## 7.1 saltstack使用yum搭建LAMP
```
~]# tree .
|-- lamp
|   |-- files
|   |   |-- httpd.conf
|   |   |-- index.php
|   |   |-- mariadb.php
|   |   |-- my.cnf
|   |   `-- php.ini
|   `-- lamp.sls
|-- httpd
|   |-- conf
|   |   `-- httpd.conf
|   |-- httpd_conf.sls
|   |-- httpd_install.sls
|   |-- httpd_service.sls
|   `-- init.sls
|-- mariadb
|   |-- conf
|   |   `-- my.cnf
|   |-- init.sls
|   |-- mariadb_conf.sls
|   |-- mariadb_install.sls
|   `-- mariadb_service.sls
|-- php
|   |-- conf
|   |   `-- php.ini
|   |-- init.sls
|   |-- php_conf.sls
|   `-- php_install.sls
`-- top.sls

~]# salt '*' state.highstate	#执行top.sls

~]# cat httpd/init.sls 
    include:
      - .httpd_install
      - .httpd_conf
      - .httpd_service

~]# cat top.sls 
    base:
      "node1.chuan.com":
        - match: list
        - httpd
        - php
        - mariadb 
      "node2.chuan.com":
        - lamp.lamp 

~]# cat lamp.sls
    lamp-install:
      pkg.installed:
        - names:
          - httpd
          - php
          - mariadb-server
          - php-mysql

    httpd-conf:
      file.managed:
        - name: /etc/httpd/conf/httpd.conf
        - source: salt://lamp/files/httpd.conf
        - user: root
        - group: root
        - mode: 644
        - template: jinja
        - defaults:
          PORT: 880

    php-conf:
      file.managed:
        - name: /etc/php.ini
        - source: salt://lamp/files/php.ini
        - user: root
        - group: root
        - mode: 644

    mariadb-conf:
      file.managed:
        - name: /etc/my.cnf
        - source: salt://lamp/files/my.cnf
        - user: root
        - group: root
        - mode: 644

    httpd-service:
      service.running:
        - name: httpd
        - enable: True
        - reload: True
        - watch:
          - file: httpd-conf
          - file: php-conf
        - require:
          - pkg: lamp-install

    mariadb-service:
      service.running:
        - name: mariadb
        - enable: True
        - reload: True
        - watch:
          - file: mariadb-conf
        - require:
          - pkg: lamp-install

    test-page-php:
      file.managed:
      - name: /var/www/html/index.php
      - source: salt://lamp/files/index.php
      - user: root
      - group: root
      - mode: 644

    test-page-mariadb:
      file.managed:
      - name: /var/www/html/mariadb.php
      - source: salt://lamp/files/mariadb.php
      - user: root
      - group: root
      - mode: 644

```