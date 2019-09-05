## 书籍推荐： ##

	《Python Cookbook》
	《Learn Python The Hard Way》
	《Google's Python Class》
	《简明Python教程》

# 1.开发环境：Pyenv 

	~]# yum install -y git
	~]# yum install -y gcc make patch gdbm-devel openssl-devel sqlite-devel readline-devel zlib-devel bzip2-devel 
	~]# useradd python
	~]# passwd python
	~]# su - python

	~]$ curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
	~]$ vi  ~/.bashrc
		...
		export PATH="/home/python/.pyenv/bin:$PATH"
		eval "$(pyenv init -)"
		eval "$(pyenv virtualenv-init -)"

	~]$ . ~/.bashrc

	~]$ pyenv install --list 		#列出所有可用版本
	~]$ pyenv version				#当前使用的版本
	~]$ pyenv versions				#当前已有的所有版本	
	~]$ pyenv [global|shell|local]	#全局、shell、会话

	~]$ pyenv install 3.5.3 -v 		#安装py 3.5.3版本，联机到官网下载

	~]$ cd .pyenv/
	~]$ mkdir cache			#将三种格式的安装包放在该目录下，tar.gz | tar.xz | tgz	会随机选择一种进行安装

## 虚拟环境： 

	~]$ mkdir ~/chuan/projects/cmdb
	~]$ cd ~/chuan/projects/cmdb
	~]$ pyenv virtualenv 3.5.3 chuan353
	~]$ pyenv versions
	~]$ pyenv local chuan353

## pip工具配置：

	~]$ mkdir ~/.pip
	~]$ cat pip.conf 
		[global]
		index-url=https://pypi.tuna.tsinghua.edu.cn/simple/

	~]$ pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gevent		#临时使用一次

## 使用脚本安装和升级pip：

	~]# wget https://bootstrap.pypa.io/get-pip.py
	~]# python get-pip.py
	~]# pip -V　　#查看pip版本

## jupyter：

	~]$ pip install ipython
	~]$ pip install jupyter
	~]$ mkdir /home/python/.jupyter	
	~]$ jupyter notebook password		#修改登录密码
	~]$ jupyter notebook --ip=0.0.0.0	

	可以直接访问：
		http://192.168.164.162:8888		#默认为8888端口

	~]$ pip freeze > reuqire.txt	#可导出当前环境的所有包
	~]$ pip install -r require.txt	#将文件中的所有包导入