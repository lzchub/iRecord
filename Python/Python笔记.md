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
	~]$ pyenv [global|shell|local]	#全局、shell、当前目录及其子目录

	~]$ pyenv install 3.5.3 -v 		#安装py 3.5.3版本，联机到官网下载

	~]$ cd ~/.pyenv/
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


## Python for Windows

	https://www.python.org/ftp/python/3.6.1/python-3.6.1-amd64.exe

# 2.Python基础学习
## 2.1 基础类型

	1. 字节（bytes），字节组成的有序的不可变字节序列
	2. 字节数组（bytearray），字节组成的有序的不可变字节序列，类似于列表与元组
	3. 数字（int,float）
	4. 字符串（string），不可变对象
	5. 列表（list），可变对象，[]
	6. 元组（tunple），不可变对象，与列表相比，相当于固定的列表，()
	7. 集合（set），可变的，无序的，不重复的，{}
	8. 字典（dict），可变的，无序的，key不重复

## 2.2 线性结构

	线性结构的查询时间复杂度是 O(n)，即随着数据规模的增大而耗时增加
	set、dict等结构，内部使用hash值作为key，时间复杂度可以做到 O(1)，查询时间和数据规模无关

	可hash
		数值型：int，float，complex
		布尔型：True，False
		字符串：string，bytes
		元组：tuple
		空值：None 
			
		以上都是不可变对象，为可哈希类型，hashable

## 2.3 装饰器	


# 3.基础数据结构实现
## 3.1 排序
### 3.1.1 冒泡排序

	list1 = [5,7,5,2,9,6,4,1]
	length = len(list1)
	
	for i in range(length):
	    for j in range(length-i-1):
	        if list1[j] > list1[j+1]:
	            temp=list1[j]
	            list1[j]=list1[j+1]
	            list1[j+1]=temp
	
	print(list1)
	