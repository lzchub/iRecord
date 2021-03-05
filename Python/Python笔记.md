## 书籍推荐： ##

	《Python Cookbook》
	《Learn Python The Hard Way》
	《Google's Python Class》
	《简明Python教程》

# 1.开发环境

Python安装：源码

```c
1.下载
    ~]# wget https:/www.python.org/ftp/python/3.7.3/Python-3.7.3.tar.xz
   
2.依赖安装
    ~]# yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel gcc gcc-c++ 
        
3.安装
    ~]# tar xf Python-3.7.3.tar.xz
    ~]# cd Python-3.7.3
    ~]# ./configure --prefix=/usr/local/python37 --enable-optimizations

4.配置环境变量
    ~]# cat /etc/profile.d/python37.sh 
        PY_HOME=/usr/local/python37
        PATH=$PATH:$PY_HOME/bin   
	~]# . /etc/profile.d/python37.sh 
    ~]# ln -sv /usr/local/python37/bin/python3 /usr/bin/python3
            
5.编辑vim格式
	~]# cd ~
	~]# vim .vimrc
		set nu
        set ts=4		#tab为4个空格长度
		syntax on		
		set expandtab	#将tab换为空格
		set autoindent
		set ruler
		set nohls
        inoremap _main if __name__ == '__main__':			#映射快捷键，输入模式
		map <F2> gg9999dd									#映射快捷键，命令模式	
```



## 1.1 Pyenv (Linux) 

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

**虚拟环境：** 

	~]$ mkdir ~/chuan/projects/cmdb
	~]$ cd ~/chuan/projects/cmdb
	~]$ pyenv virtualenv 3.5.3 chuan353
	~]$ pyenv versions
	~]$ pyenv local chuan353

**pip工具配置：**

	~]$ mkdir ~/.pip
	~]$ cat pip.conf 
		[global]
		index-url=https://pypi.tuna.tsinghua.edu.cn/simple/
	
		index-url=https://pypi.doubanio.com/simple/
	
	注：Windows就在对用用户主目录下，如chuan用户就在C盘用户chuan下面建立pip/pip.ini文件即可
	
	~]$ pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gevent		#临时使用一次

**使用脚本安装和升级pip：**

	~]# wget https://bootstrap.pypa.io/get-pip.py
	~]# python get-pip.py
	~]# pip -V　　#查看pip版本

**jupyter：**

	~]$ pip install ipython
	~]$ pip install jupyter
	~]$ mkdir /home/python/.jupyter	
	~]$ jupyter notebook password		#修改登录密码
	~]$ jupyter notebook --ip=0.0.0.0	
	
	可以直接访问：
		http://192.168.164.162:8888		#默认为8888端口
	
	~]$ pip freeze > reuqire.txt	#可导出当前环境的所有包
	~]$ pip install -r require.txt	#将文件中的所有包导入

## 1.2 pycharm

**Python for Windows：**

	https://www.python.org/ftp/python/3.6.1/python-3.6.1-amd64.exe

**pycharm：**

```c
https://www.jetbrains.com
```





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

# 4. 面向对象

## 4.1 特殊属性

| 属性        | 含义                                                         |
| ----------- | ------------------------------------------------------------ |
| \__name__   | 类，函数，方法等的名字                                       |
| \__module__ | 类定义所现在的模块名                                         |
| \__class__  | 对象或类所属的类                                             |
| \__bases__  | 类的基类的元素，顺序为他们在基类列表中出现的顺序             |
| \__doc__    | 类/函数的文档字符传，如果没有定义则为None                    |
| \__mro__    | 类的mro,class.mro()返回                                      |
| \__dict__   | 类或实例的属性，可写的字典                                   |
| \__dir__    | 返回了类或者对象所有成员列表，dir()函数调用的是_dir_()，如果提供了_dir_()，则返回属性列表，否则尽可能从__dict__属性中收集信息 |

## 4.2 魔术方法

| 描述                                           | 方法                                                         |
| ---------------------------------------------- | ------------------------------------------------------------ |
| 初始化和销毁                                   | \_\_init__  和   \_\_del__                                   |
| 哈希（在字典和set中使用）                      | \_\_hash__                                                   |
| 布尔类型，常用于判断语句                       | \_\_bool__                                                   |
| 可视化，用于输出对应的类型                     | \_\_str___ 和  \_\_repr\_\_                                  |
| 运算符重载                                     | \_\_eq\_\_  ,  \_\_ne\_\_  ,  \_\_gt\_\_  ,  _\_lt\_\_  等   |
| 容器和大小相关及操作相关属性                   | \_\_getitem\_\_  ,  _\_setitem\_\_ ,  \_\_iter\_\_   等      |
| 可调用对象（将实例化的对象当成一个函数去调用） | \_\_call\__                                                  |
| 上下文管理（with  open(x)  as f 等形式）       | \_\_enter\_\_  ,  \_\_exit\_\_                               |
| 反射                                           | \_\_getattr\_\_  ,   \_\_setattr\_\_  ,  \_\_delattr\_\_  ,  \_\_hasattr\_\_ |
| 描述器                                         | Object._get_(self,instance,owner)Object._set_(self,instance,value)Object._delete_(self,instance) |

实例参考：https://cloud.tencent.com/developer/article/1566261