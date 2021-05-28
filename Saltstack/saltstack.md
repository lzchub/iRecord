# 1. 安装配置
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

~]# salt-key -L		#查看当前证书签证情况
~]# salt-key -A	-y	#master添加所有minion,salt使用ssl签证方式进行安全验证

```
# 2. saltstack基础使用

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

# 3. salt命令参数解析

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
                    
                重启salt-minion 服务
                    
            2.直接将配置写入/etc/salt/grains文件         
                roles:
                  - webserver
                  - memcache
                  
                重启salt-minion 服务
                  
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
				~]# salt 'SCYD-10.1.33.81' grains.items			#查看grains所有名称和值
				~]# salt 'SCYD-10.1.33.81' grains.item roles	#查看对应grains名称和值	
				~]# salt 'SCYD-10.1.33.81' grains.get roles		#查看对应grains值
				
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

```
# 4. 常用模块

```c
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
            
    9.cp模块

注意：具体参数可到官网查看
```



# 5. 自定义模块

```
扩展modules:
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

扩展grains_modules:
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

扩展state
```

# 6. state模块及状态配置文件书写
**state模块：**

```c
 1.查看minion支持的所有states列表
	~]# salt SCYD-192.168.183.129 sys.list_state_modules
     
 2.查看指定state的所有function
     ~]# salt SCYD-192.168.183.129 sys.list_state_functions file 
     
 3.查看指定state的用法
     ~]# salt SCYD-192.168.183.129 sys.state_doc file
     
 4.查看指定state指定function用法
     ~]# salt SCYD-192.168.183.129 sys.state_doc file.managed
     
```

**基础事项：**

```
注意：
	1.状态配置文件必须以 .sls为后缀
	2.默认base环境为/srv/salt，可修改master配置文件修改
	3.使用state.sls执行
	4.使用yaml格式书写
	5.状态模块与前面的远程命令模块略有不同
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
~]# salt '*' state.sls dir.test		#dir为test的父目录，即为/srv/salt/dir/test.sls

指定对象，执行对应模块文件

后面会介绍使用top.sls执行
```

## 6.1 state.sls与state.highstate的区别

```c
1. state.highstate会读取所有环境（包括base环境）的top.sls文件，并且执行top.sls文件内容里面定义的sls文件，不在top.sls文件里面记录的sls则不会被执行；
2. state.sls默认读取base环境，但是它并不会读取top.sls文件。你可以指定state.sls执行哪个sls文件，只要这个sls文件在base环境下存在；
3. state.sls也可以指定读取哪个环境：state.sls salt_env='prod' xxx.sls，这个xxx.sls可以不在top.sls中记录。
4. state.sls执行的xxx.sls会被下发到minion端，而state.highstate则不会

其实这些都不是重点，我认为重点在于state.sls执行指定模块的前提是，该模块存在init.sls文件。
```



# 7. jinja2模板

```
变量使用 	{{}}
	{{var}}
表达式使用	{% %}
	{% set var='good' %}
```

参考文档：http://docs.jinkan.org/docs/jinja2/

# 8. 实例解析

## 8.1 saltstack使用yum搭建LAMP
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

~]# salt '*' state.highstate test=True	#测试执行top.sls
~]# salt '*' state.highstate


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

# 9. restful API操作saltstack

如果需要通过第三方来调用SaltStack时，使用SaltStack自带的Python API并不能很好的满足需求。可以通过使用SaltStack基于RESTful风格的HTTP API。该API模块并不是内置的，需要单独安装。

**1.安装 salt-api**

一般情况下，salt-api会使用HTTPS，首次配置成功后，使用用户名和密码登陆，获得Token，Token创建后，默认有效期是12小时，在有效期之内，使用该Token可以代替使用用户名和密码来访问API（该有效时间可在salt-master配置文件中修改）。

```c
# 使用https模式，需要安装如下依赖
~]# yum -y install gcc make python-devel libffi-devel
~]# pip install pyOpenSSL==0.15.1 
    
# 生成https证书
~]# cd /etc/pki/tls/private
~]# openssl genrsa 2048 > localhost.key
~]# cd /etc/pki/tls/certs
~]# make testcert

# 额外安装服务
~]# yum install -y salt-api
```

**2.配置用户分配权限**

```c
~]# cat /etc/salt/master

...
rest_cherrypy:
  port: 8000
  ssl_crt: /etc/pki/tls/certs/localhost.crt
  ssl_key: /etc/pki/tls/private/localhost.key
external_auth:
  pam:
    saltapi:
      - .*
      - '@wheel'
      - '@runner'
      - '@jobs'
          
# 创建账号          
~]# useradd -s /sbin/nologin saltapi
~]# echo chuan | passwd --stdin saltapi     
          
注：
    external_auth:
      pam:  #认证模式，pam指的是用Linux本身的用户认证模式
        sa:  #Linux系统中真实存在的用户名
          - '*':  #设置用户的权限，允许该用户操作哪些主机，*代表全部
            - test.*  #允许操作的模块及方法
            - cmd.*
```

**3.测试获取token**

一般情况下，salt-api会使用HTTPS，首次配置成功后，使用用户名和密码登陆，获得Token，Token创建后，默认有效期是12小时，在有效期之内，使用该Token可以代替使用用户名和密码来访问API（该有效时间可在salt-master配置文件中修改）。

```c
~]# curl -sSk https://localhost:8000/login -H 'Accept: application/x-yaml' -d username=saltapi -d password=chuan -d eauth=pam                
return:
- eauth: pam
  expire: 1621965658.824181
  perms:
  - .*
  - '@wheel'
  - '@runner'
  - '@jobs'
  start: 1621922458.824179
  token: eb7b048ac374a9ce5df75b8053ad577d762f2d4e
  user: saltapi
```

**4.通过token进行验证**

```c
~]# curl -sSk https://localhost:8000 -H 'Accept: application/x-yaml' -H 'X-Auth-Token: eb7b048ac374a9ce5df75b8053ad577d762f2d4e' -d client=local -d tgt='*' -d fun=test.ping
return:
- SCYD-192.168.183.129: true
  SCYD-192.168.183.130: true
  SCYD-192.168.183.131: true
```

**5.使用python操作salt restful api**

**python 2.x 版本**

```c
#!/usr/bin/python
#encoding:utf-8

import urllib2,urllib
import time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
try:
    import json
except ImportError:
    import simplejson as json
 
class SaltAPI(object):
    __token_id = ''
    def __init__(self,url,username,password):
        self.__url = url.rstrip('/')
        self.__user = username
        self.__password = password
 
    def token_id(self):
        ''' user login and get token id '''
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        content = self.postRequest(obj,prefix='/login')
        try:
                self.__token_id = content['return'][0]['token']
        except KeyError:
                raise KeyError
 
    def postRequest(self,obj,prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token'   : self.__token_id}
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content
 
    def list_all_key(self):
        '''
        获取包括认证、未认证salt主机
        '''
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        return minions,minions_pre
 
    def delete_key(self,node_name):
        '''
        拒绝salt主机，删除主机
        '''
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': node_name}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret
 
    def accept_key(self,node_name):
        '''
        接受salt主机
        '''
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': node_name}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret
 
    def remote_noarg_execution(self,tgt,fun):
        ''' 
        执行命令没有参数
        tgt：目标主机
        fun: 执行模块，例如“test.ping”
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0].values()
        return ret
 
    def remote_execution(self,tgt,fun,arg):
        ''' 执行命令有参数 '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0][tgt]
        return ret
 
    def target_remote_execution(self,tgt,fun,arg):
        ''' 异步执行远程命令，执行模块 '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'nodegroup'}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid
 
    def deploy(self,tgt,arg):
        ''' 状态管理 '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        return content
 
    def async_deploy(self,tgt,arg):
        ''' 异步状态管理 '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid
 
 
def main():
    sapi = SaltAPI(url='https://192.168.183.132:8000',username='saltapi',password='chuan')
    sapi.token_id()
    #print sapi.list_all_key()
    #sapi.delete_key('test-01')
    #sapi.accept_key('test-01')
    #sapi.deploy('test-01','nginx')
    print sapi.remote_noarg_execution('SCYD-192.168.183.130','test.ping')
 
if __name__ == '__main__':
    main()
```

**python 3.X版本**

```c
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author : wangyongcun
 
import requests
import copy
 
SALT_API = {
    "url": "https://192.168.11.12:8000",
    "user": "saltapi",
    "password": "password",
}
 
 
class SaltApi(object):
 
    def __init__(self):
        self.__user = SALT_API["user"]
        self.__passwd = SALT_API["password"]
        self.url = SALT_API["url"]
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.__base_data = dict(
            username=self.__user,
            password=self.__passwd,
            eauth='pam'
        )
        self.__token = self.get_token()
 
    def get_token(self):
        """  login salt-api and get token_id """
        params = copy.deepcopy(self.__base_data)
        requests.packages.urllib3.disable_warnings()  # close ssl warning, py3 really can do it!
        ret = requests.post(url=self.url + '/login', verify=False, headers=self.headers, json=params)
        ret_json = ret.json()
        token = ret_json["return"][0]["token"]
        return token
 
    def __post(self, **kwargs):
        """  custom post interface, headers contains X-Auth-Token """
        headers_token = {'X-Auth-Token': self.__token}
        headers_token.update(self.headers)
        requests.packages.urllib3.disable_warnings()
        ret = requests.post(url=self.url, verify=False, headers=headers_token, **kwargs)
        ret_code, ret_data = ret.status_code, ret.json()
        return (ret_code, ret_data)
 
    def list_all_keys(self):
        """  show all keys, minions have been certified, minion_pre not certification """
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        r = self.__post(json=params)
        minions = r[1]['return'][0]['data']['return']['minions']
        minions_pre = r[1]['return'][0]['data']['return']['minions_pre']
        return minions, minions_pre
 
    def delete_key(self, tgt):
        """ delete a key """
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': tgt}
        r = self.__post(json=params)
        return r[1]['return'][0]['data']['success']
 
    def accept_key(self, tgt):
        """  accept a key """
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': tgt}
        r = self.__post(json=params)
        return r[1]['return'][0]['data']['success']
 
    def lookup_jid_ret(self, jid):
        """  depend on jobid to find result """
        params = {'client': 'runner', 'fun': 'jobs.lookup_jid', 'jid': jid}
        r = self.__post(json=params)
        return r[1]['return'][0]
 
    def salt_running_jobs(self):
        """ show all running jobs """
        params = {'client': 'runner', 'fun': 'jobs.active'}
        r = self.__post(json=params)
        return r[1]['return'][0]
 
    def run(self, params):
        """ remote common interface, you need custom data dict
            for example:
                params = {
                    'client': 'local',
                    'fun': 'grains.item',
                    'tgt': '*',
                    'arg': ('os', 'id', 'host' ),
                    'kwargs': {},
                    'expr_form': 'glob',
                    'timeout': 60
                }
         """
        r = self.__post(json=params)
        return r[1]['return'][0]
 
    def remote_execution(self, tgt, fun, arg, ex='glob'):
        """ remote execution, command will wait result
            arg must be a tuple, eg: arg = (a, b)
            expr_form : tgt m
        """
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': ex}
        r = self.__post(json=params)
        return r[1]['return'][0]
 
    def async_remote_execution(self, tgt, fun, arg, ex='glob'):
        """ async remote exection, it will return a jobid
            tgt model is list, but not python list, just like 'node1, node2, node3' as a string.
         """
        params = {'client': 'local_async', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': ex}
        r = self.__post(json=params)
        return r[1]['return'][0]['jid']
 
    def salt_state(self, tgt, arg, ex='list'):
        """  salt state.sls """
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': ex}
        r = self.__post(json=params)
        return r[1]['return'][0]
 
    def salt_alive(self, tgt, ex='glob'):
        """ salt test.ping """
        params = {'client': 'local', 'tgt': tgt, 'fun': 'test.ping', 'expr_form': ex}
        r = self.__post(json=params)
        return r[1]['return'][0]
 
 
if __name__ == '__main__':
    data = {
        'client': 'local',
        'fun': 'grains.item',
        'tgt': '*',
        'arg': ('os', 'id', 'host' ),
        'kwargs': {},
        'expr_form': 'glob',
        'timeout': 60
    }
    obj = SaltApi()
    # ret = obj.list_all_keys()
    # ret = obj.accept_key('windows-test')
    # ret = obj.delete_key('windows-test')
    # ret = obj.lookup_jid_ret('20180612111505161780')
    # ret = obj.salt_running_jobs()
    # ret = obj.remote_execution('*', 'grains.item', ('os', 'id'))
    # ret = obj.async_remote_execution('*', 'grains.item', ('os', 'id'))
    # ret = obj.salt_alive('*', 'glob')
    ret = obj.run(data)
    print(ret)
```

