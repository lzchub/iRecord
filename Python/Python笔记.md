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
    ~]# make && make install 

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

**测试代码：**

### 1. **\_\_name\_\_**   

获取类和函数的名字

```c
class A:
    pass

class B:
    pass

print(A.__name__,B.__name__,sep='\n')

--------------------------------------------------
A
B
```

### 2. **\_\_module\_\_** 	

类定义所在的模块名

```c
class  A:
    pass
class B:
    pass
print  (A.__module__,B.__module__)

--------------------------------------------------
__main__
__main__
```

### 3. **\_\_class\_\_**   

对象或类所属的类 

```
class  A:
    pass
class B(A):
    pass
a=A()
b=B()
print (A.__class__,B.__class__,sep='\n')  #类所属的类是class
print (a.__class__,b.__class__,sep='\n')  # 对象所属的类是实实在在的类

--------------------------------------------------
<class 'type'>
<class 'type'>
<class '__main__.A'>
<class '__main__.B'>
```

### 4. **\_\_bases\_\_**  

 类的基类的元组，顺序是他们在基类列表中出现的顺序 

```c
class  A:
    pass
class B(A):
    pass
class C(B):
    pass
class E:
    pass
class D(E,C):
    pass
print (A.__bases__,B.__bases__,C.__bases__,D.__bases__,sep='\n')
        
--------------------------------------------------
(<class 'object'>,)
(<class '__main__.A'>,)
(<class '__main__.B'>,)
(<class '__main__.E'>, <class '__main__.C'>)
```

### 5. **\_\_doc\_\_**   

文档字符串，针对类和函数有效，若不存在，则返回为None

```c
class  A:
    '''this  is  class'''
    pass
def B():
    '''this is function'''
    pass
class C:
    pass
print (A.__doc__,B.__doc__,C.__doc__,sep='\n')
        
--------------------------------------------------
this  is  class
this is  function
None
```

### 6. **\_\_mro\_\_**   

类的mro。返回多继承中的查找顺序

```c
class  A:
    pass
class B(A):
    pass
class C(B):
    pass
class E:
    pass
class D(E,C):
    pass
print (A.__mro__,B.__mro__,C.__mro__,D.__mro__,sep='\n')
        
--------------------------------------------------
(<class '__main__.A'>, <class 'object'>)
(<class '__main__.B'>, <class '__main__.A'>, <class 'object'>)
(<class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>)
(<class '__main__.D'>, <class '__main__.E'>, <class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>)
```

### 7. **\_\_dict\_\_** 

类或者实例的属性，可写的字典

```c
class  A:
    a=10
    def  __init__(self,x):
        self.x=5
a=A(3)

print (A.__dict__)
print (a.__dict__)
            
--------------------------------------------------
{'__module__': '__main__', 'a': 10, '__init__': <function A.__init__ at 0x0000017ADCB02B70>, '__dict__': <attribute '__dict__' of 'A' objects>, '__weakref__': <attribute '__weakref__' of 'A' objects>, '__doc__': None}
{'x': 5}
```

### 8. **\_\_dir\_\_**  

dir 返回了类或者对象所有成员名称列表，dir()函数调用的是\_\_dir\_\_()，如果提供了\_\_dir\_\_() ,则返回属性的列表，否则会尽量从\_\_dict\_\_属性中收集

dir() 对于不同类型的对象具有不同的行为：

1、如果对象是模块对象，则列表包含模块的属性名

```c
import  re
def  foo(x):
    y=1
print (dir())  # 输出当前模块信息,此处会打印当前导入的模块和导入的函数
print (dir(re))
print ('+'*20)
print (dir(foo))
```

```c
['__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'foo', 're']
['A', 'ASCII', 'DEBUG', 'DOTALL', 'I', 'IGNORECASE', 'L', 'LOCALE', 'M', 'MULTILINE', 'RegexFlag', 'S', 'Scanner', 'T', 'TEMPLATE', 'U', 'UNICODE', 'VERBOSE', 'X', '_MAXCACHE', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', '__version__', '_alphanum_bytes', '_alphanum_str', '_cache', '_compile', '_compile_repl', '_expand', '_locale', '_pattern_type', '_pickle', '_subx', 'compile', 'copyreg', 'enum', 'error', 'escape', 'findall', 'finditer', 'fullmatch', 'functools', 'match', 'purge', 'search', 'split', 'sre_compile', 'sre_parse', 'sub', 'subn', 'template']
++++++++++++++++++++
['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
```

2、如果对象是类型或者类对象，列表包含类的属性名，以及其他基类的属性名

```c
class A:
    a='1234'
    def __init__(self):
        pass
class  B(A): # 此处调用父类，其dir中会包含父类的属性
    pass
print (dir())  # 输出当前模块信息,此处会打印当前导入的模块和导入的函数
print ('*'*40)
print (dir(A),dir(B),sep='\n')  # 此中DIR属性父类和子类是完全相同的，但dict中却是不同的
print (A.__dict__,B.__dict__,sep='\n')
```

```c
['A', 'B', '__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']
****************************************
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'a']
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'a']
{'__module__': '__main__', 'a': '1234', '__init__': <function A.__init__ at 0x0000022206254C80>, '__dict__': <attribute '__dict__' of 'A' objects>, '__weakref__': <attribute '__weakref__' of 'A' objects>, '__doc__': None}
{'__module__': '__main__', '__doc__': None}
```

 3、如果是对象，列表包含对象的属性名，它的类的属性名和基类的属性名 

```c
class A:
    a='1234'
    def __init__(self):
        self.x=10
class  B(A): # 此处调用父类，其dir中会包含父类的属性
    pass
a=A()
print (dir())  # 输出当前模块信息,此处会打印当前导入的模块和导入的函数
print ('*'*40)
print (dir(A),dir(B),dir(a),sep='\n') #此处若是打印实例的属性，则会吧类的属性也打印上来
```

```c
['A', 'B', '__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'a']
****************************************
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'a']
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'a']
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'a', 'x']
```

 4、此处对属性名进行了重写操作

```c
class A:
    a='1234'
    def __init__(self):
        self.x=10
class  B(A): # 此处调用父类，其dir中会包含父类的属性
    def __dir__(self): # 此处是针对实例设置的，和类本身并无关系
        return ['this is class A '] # 此处是dir返回是列表，若使用字符串，则会处理成列表进行返回
a=A()
b=B()
print (dir())  # 输出当前模块信息,此处会打印当前导入的模块和导入的函数，以及实例后的对象
print ('*'*40)
print (dir(A),dir(B),dir(a),dir(b),sep='\n') #此处若是打印实例的属性，则会吧类的属性也打印上来
```

```c
['A', 'B', '__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'a', 'b']
****************************************
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'a']
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'a']
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'a', 'x']
['this is class A ']
```

### 9. \_\_slots\_\_

**问题引出：**

>  都是字典惹的祸 字典为了提升查询效率，必须用空间换时间  一般来说一个对象，属性多一点，都存储在字典中便于查询，问题不大，但是数百万个对象，那么字典就占得有点大了，这个时候，python便提供了\_\_slots\_\_  

**测试代码：**

```c
class A:
    x=123
    __slots__ = ('p1',)  # 此处只放置了一个槽位，则只能使用p1变量，不能使用其他
    def __init__(self):
        self.p1=1
        self.p2=2
    def show(self):
        print ('this is  test1,{}'.format(self.p1))
print (A().__dict__)
```

```c
Traceback (most recent call last):
  File "D:/python-scripts/scripts/test.py", line 625, in <module>
    print (A().__dict__)
  File "D:/python-scripts/scripts/test.py", line 622, in __init__
    self.p2=2
AttributeError: 'A' object has no attribute 'p2'
```

```c
class A:
    x=123
    __slots__ = ('p1','p2')  # 此处只放置了一个槽位，则只能使用p1变量，不能使用其他
    def __init__(self):
        self.p1=1
        self.p2=2
    def show(self):
        print ('this is  test1,{}'.format(self.p1))
print ('slots',A().__slots__)  #实例的此属性可以被打印出来，但实例的字典属性却不存在
print (A.__dict__)  # 类的字典属性不受影响
print ('dict',A().__dict__)
```

```c
slots ('p1', 'p2')
{'__module__': '__main__', 'x': 123, '__slots__': ('p1', 'p2'), '__init__': <function A.__init__ at 0x000001CBDBAD2B70>, 'show': <function A.show at 0x000001CBDBAE4C80>, 'p1': <member 'p1' of 'A' objects>, 'p2': <member 'p2' of 'A' objects>, '__doc__': None}
Traceback (most recent call last):
  File "D:/python-scripts/scripts/test.py", line 637, in <module>
    print ('dict',A().__dict__)
AttributeError: 'A' object has no attribute '__dct__'
```

```c
class A:
    x=123
    __slots__ = 'p1','p2'  # 此处只放置了一个槽位，则只能使用p1变量，不能使用其他
    def __init__(self):
        self.p1=1
        self.p2=2
    def show(self):
        print ('this is  test1,{}'.format(self.p1))
print ('slots',A().__slots__)  #实例的此属性可以被打印出来，但实例的字典属性却不存在
print (A.__dict__)  # 类的字典属性不受影响
A.p4=300  #类添加属性，只会影响类的__dict__，实例中不会显示，而__slots__ 不会对类造成影响
try:
    setattr(A(),'p5',30)
except  AttributeError  as  a:
    print (A(),'不能添加属性')
finally:
    print (A().__slots__) #查看

try:
    A().P3=300
except  AttributeError  as  a:
    print (A(),'不能添加属性')
finally:
    print (A().__slots__) #查看
```

```c
slots ('p1', 'p2')
{'__module__': '__main__', 'x': 123, '__slots__': ('p1', 'p2'), '__init__': <function A.__init__ at 0x000001C7BDEB2B70>, 'show': <function A.show at 0x000001C7BDEC4C80>, 'p1': <member 'p1' of 'A' objects>, 'p2': <member 'p2' of 'A' objects>, '__doc__': None}
<__main__.A object at 0x000001C7BDEC6780> 不能添加属性
('p1', 'p2')
<__main__.A object at 0x000001C7BDEC67B8> 不能添加属性
('p1', 'p2')
```

**继承：**

```c
class A:
    x=123
    __slots__ = 'p1','p2'  # 此处只放置了一个槽位，则只能使用p1变量，不能使用其他
    def __init__(self):
        self.p1=1
        self.p2=2
    def show(self):
        print ('this is  test1,{}'.format(self.p1))
class B(A):
    def __init__(self):
        super().__init__()
        self.b1=200
b=B()
b.b2=300
print (b.__dict__)  # 继承则失效 
```

```c
{'b1': 200, 'b2': 300}
```



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

### 1. \_\_init\_\_ 、\_\_del\_\_

```c
class X:
    def __init__(self,name):
        self.name=name
        self.x=10
        print ("init  instance")
    def __del__(self):
        print ('delete {}'.format(self.name))
a=X('a')
del  a  # 因为python自身的垃圾回收机制，而del删除实例的操作不确定何时执行，因此需要使用del进行清除处理
```

```c
init  instance
delete a
```

### 2. \_\_hash__

hash 中最基础的hash就是取模运算。 list 不能hash的原因  list 源码： 其中hash=None,在调用None的时候自然是不能hash的

**判断是否可以hash：**

```c
from collections import Hashable
class X:
    def __init__(self,x):
        self.x=x
    def __hash__(self):
        return 1
print (isinstance(X(1),Hashable))
print (isinstance([],Hashable))
```

```c
True
False
```

**定义不可hash类型：**

```
from collections import Hashable

class A:
    def __init__(self,x):
        self.x = x

    #def __hash__(self):
    #   return None
        
    __hash__ = None

print(hash(A(10)))
```

```c
Traceback (most recent call last):
  File "D:/python-scripts/scripts/test.py", line 679, in <module>
    print(hash(A(10)))
TypeError: unhashable type: 'A'
```

**实例：**

```c
class X:
    def __init__(self):
        self.x=10
    def __hash__(self):  # 此处是定义的是实例的hash，和类没关系
        return  None  # 此处设置hash的返回为None,模拟列表
        # 另一种方式定义不可哈希类型  __hash__=None
class Y:  #此类未设置相关的hash属性
    def __init__(self):
        pass
class Z: # 此类定义了hash的返回值为1 ，则实例化后调用hash返回为1
    def __hash__(self):
        return  1
print (hash(Y())) # 此处返回整数
print (hash(Z())) # 此处返回为固定数
print (hash(X()))  #进行判断是否能够进行hash操作，未进行hash，直接抛出异常
```

```c
Traceback (most recent call last):
  File "D:/python-scripts/scripts/test.py", line 696, in <module>
    print (hash(X()))  #进行判断是否能够进行hash操作，未进行hash，直接抛出异常
TypeError: __hash__ method should return an integer
-9223371912820427818
1
```

### 3. \_\_bool__

\_\_bool\_\_ 内建函数bool(), 或者对象放在逻辑表达式的位置，调用这个函数返回布尔值，没有定义\_\_bool\_\_，就找\_\_len\_\_ 返回长度，非0为真，如果\_\_len\_\_也没有定义，则所有的实例都返回是真。

```c
class Point:  # 此类未定义len和bool，因此其返回值为恒真
    def  __init__(self):
        self.x=3
        self.y=4
    # def __bool__(self):
    #     return False

print (bool(Point()))

class Point2:
    def  __init__(self):
        self.x=3
        self.y=4
    def __bool__(self):
        return False

print (bool(Point2()))

class Point3:
    def  __init__(self):
        self.x=3
        self.y=4
    # def __bool__(self):
    #     return False

    def __len__(self):
        return 0
print (bool(Point3()))


class Point4:
    def  __init__(self):
        self.x=3
        self.y=4
    # def __bool__(self):
    #     return False

    def __len__(self):
        return 1
print (bool(Point4()))

class Point5:		# 当 bool 与 len 都定义时，以
    def  __init__(self):
        self.x=3
        self.y=4
    def __bool__(self):
        return False

    def __len__(self):
        return 1
print (bool(Point5()))
```

```c
True
False
False
True
False
```

### 4. \_\_str___ 、\_\_repr\_\_

\_\_repr\_\_ : 内建函数repr()对一个对象获取字符串表达式，如果一个类定义了\_\_repr\_\_但没有定义\_\_str\_\_，那么在请求该类的实例的"非正式"的字符串也将调用\_\_repr\_\_()

\_\_str___ : str() 函数，内建函数format，print()函数调用，需要返回对象的字符串表达式

当str和repr同时存在时，如果输出结果直接作用于对象上，则调用str方法，否则将调用repr方法

1. `__repr__`正式，`__str__` 非正式。 
2. `__str__`主要由 `str()`,`format()`和`print()`三个方法调用。
3.  若定义了`__repr__`没有定义`__str__`，那么本该由`__str__`展示的字符串会由`__repr__`代替。
4. `__repr__`主要用于调试和开发，而`__str__`用于为最终用户创建输出。 
5. `__repr__`看起来更像一个有效的 Python 表达式，可用于重新创建具有相同值的对象（给定适当的环境）。

```c
class Point:
    def  __init__(self):
        self.x=3
        self.y=4
    def  __repr__(self):
        return str([self.x,self.y])  #此处的返回必须使用字符串进行包裹，否则会报错
print (Point())
print("-"*50)

class Point2:
    def  __init__(self):
        self.x=3
        self.y=4
    def  __repr__(self):
        return str([self.x,self.y])  #此处的返回必须使用字符串进行包裹，否则会报错
    def  __str__(self):  # 若存在此属性，则上述的表达式将不会被调用
        return  'abcdefg'
print (Point2())
print("-"*50)

class Point3:
    def  __init__(self):
        self.x=3
        self.y=4
    def  __repr__(self):
        return str([self.x,self.y])  #此处的返回必须使用字符串进行包裹，否则会报错
    def  __str__(self):  # 若存在此属性，则上述的表达式将不会被调用
        return  'abcdefg'
print (Point3())
p1=Point3()
p2=Point3()
lst=[p1,p2]
for x in  lst:
    print (x)
print (lst)

print (*lst)  #进行解包处理，此时是针对于对象上的，此时应该调用的是str
```

```c
[3, 4]
--------------------------------------------------
abcdefg
--------------------------------------------------
abcdefg
abcdefg
abcdefg
[[3, 4], [3, 4]]
abcdefg abcdefg
```

### 5. 运算符重载

operator 模块提供以下的特殊方法，可以将类的实例使用下面操作符来进行操作 

| 运算符                 | 特殊方法                                                     | 含义                                   |
| ---------------------- | ------------------------------------------------------------ | -------------------------------------- |
| <,<=,==,>,>=,!=        | \_\_lt\_\_ , \_\_le\_\_ , \_\_eq\_\_ , \_\_gt\_\_ , \_\_ge\_\_ , \_\_ne\_\_ | 比较运算符                             |
| +,-,*,/,%,//,**,divmod | \_\_add\_\_ , \_\_sub\_\_ , \_\_mul\_\_ , \_\_truediv\_\_ , \_\_mod\_\_ , \_\_floordiv\_\_ , \_\_pow\_\_ , \_\_divmod\_\_ | 算数运算符，移位，位运算也有对应的方法 |
| +=,-=,*=,/=,%=,//=,**= | \_\_iadd\_\_ , \_\_isub\_\_ , \_\_imul\_\_ , \_\_itruediv\_\_ , \_\_imod\_\_ , \_\_ifloordiv\_\_ , \_\_ipow\_\_ |                                        |

```c
class A():
    def __init__(self,x):
        self.x = x

    # <
    def __lt__(self, other):
        print("__lt__")
        return self.x < other.x

    # <=
    def __le__(self, other):
        print("__le__")
        return self.x <= other.x

    # >
    def __gt__(self, other):
        print("__gt__")
        return self.x > other.x

    # >=
    def __ge__(self, other):
        print("__ge__")
        return self.x >= other.x

    # !=
    def __ne__(self, other):
        print("__ne__")
        return self.x != other.x

    # ==
    def __eq__(self, other):
        print("__eq__")
        return self.x == other.x

    # +=
    def __iadd__(self, other):
        print("__iadd__")
        self.x += other.x
        return self

    # -=
    def  __isub__(self, other):
        print ('__isub__')
        self.x -= other.x
        return  self

    def __add__(self, other):
        print("__add__")
        return self.x + other.x

    # 反向加法
    def __radd__(self, other):
        print("__radd__")
        return self.x + other.x

class B():
    def __init__(self,x):
        self.x = x

a1 = A(5)
a2 = A(10)
a3 = A(2)

print(a1 > a2)
print(a1 > a3)
print(a2 > a3)
print(a1 == a3)
print("-"*50)

a1+=a2
print(a1.x,a2.x)
print("-"*50)

print(a1+a2)
print("-"*50)

print(a2+a1)
print("-"*50)

b1 = B(10)
print(a1+b1)
print("-"*50)

print(b1+a1)
```

```c
__gt__
False
__gt__
True
__gt__
True
__eq__
False
--------------------------------------------------
__iadd__
15 10
--------------------------------------------------
__add__
25
--------------------------------------------------
__add__
25
--------------------------------------------------
__add__
25
--------------------------------------------------
__radd__
25
```

**结论：**

```c
b+a 等价于 b.add(a),但是B类没有实现add方法，就去找a的__radd__方法 

1+a 等价于1.add(a)，而int 类型实现了__add__放方法，不过这个方法对于这种加法的返回值是NotImplemented，解释器发现了这个值，就会对第二个操作对象执行__radd__进行调用。
```

### 6. 容器相关方法

| 内建方法         | 含义                                                         |
| ---------------- | ------------------------------------------------------------ |
| \_\_len\_\_      | 内建函数len()，返回对象的长度(>=0的整数)，其实即使吧对象当作容器类型来看，就如同list或dict，bool()函数调用的时候，如果没有_bool_()方法，则会看_len_()方法是否存在，存在返回非0为真，第三方库中可能存在size，其和len的含义相同 |
| \_\_iter\_\_     | 迭代器时，调用，返回一个新的迭代器对象                       |
| \_\_contains\_\_ | in成员运算符，没有实现，就调用\_\_iter\_\_方法遍历           |
| \_\_getitem\_\_  | 实现self[key]访问，序列对象，key接受整数为索引，或者切片，对于set和dict，key为hashable，key不存在时引KeyError异常 |
| \_\_setitem\_\_  | 和\_\_getitem\_\_的访问相似，是设置值的方法                  |
| \_\_missing\_\_  | 字典使用\_\_getitem\_\_()调用时，key不存在执行该方法         |

```c
class Item:
    def __init__(self,*args):
        self.lst = list(args)

    # 返回列表长度
    def __len__(self):
        return len(self.lst)

    # 返回一个迭代器
    def __iter__(self):
        return iter(self.lst)

    # 重新add方法
    def __add__(self, other):
        self.lst.append(other)
        return self

    # 返回索引对象值
    def __getitem__(self, index):
        if index >= len(self.lst):
            return "index error..."
        else:
            return self.lst[index]

    # 动态设置索引对象值
    def __setitem__(self, index, value):
        if index >= len(self.lst):
            return "index error..."
        else:
            self.lst[index] = value
            return self

    # 可视化
    def __repr__(self):
        return str(self.lst)

item = Item(5,10,15,20)
# 调用 __len__方法
print(len(item))
print("-"*50)

# 未实现__contains__,将会调用__iter__方法
for i in item:
    print(i)
print("-"*50)

# 调用了 __add__ 方法 和 __repr__ 方法
print(item + 55)
print("-"*50)

# 调用了 __getitem__ 方法
print(item[5])
print(item[2])
print("-"*50)

# 调用了 __setitem__ 、__getitem__ 方法
item[2] = 222
print(item[2])
```

```c
4
--------------------------------------------------
5
10
15
20
--------------------------------------------------
[5, 10, 15, 20, 55]
--------------------------------------------------
index error...
15
--------------------------------------------------
222
```

### 7. \_\_call\_\_

在python中一切皆对象，函数也不例外  

可调用对象 方法 \_\_call\_\_类中出现该方法，实例就可以像函数一样调用， 可调用对象： 定义一个类，并实例化得到其实例，将实例像函数一样调用。调用是实例的，不是类的

```c
在函数中
def foo():
	pass

# 这两种调用方法效果相同，函数对象默认实现了__call__        
foo()
foo.__call__()
        
# 可以通过dir来查看        
print(dir(foo))
        
# 通过类实现斐波拉契序列
class  A:
    def __init__(self):
        pass
    
    def  __call__(self,num):
        a,b=0,1
        for  i in  range(num):
            print (b)
            a,b=b,a+b
A()(10)
```

```c
1
1
2
3
5
8
13
21
34
55
```

### 8. 上下文管理

文件IO操作可以对文件对象进行上下文管理，使用with...as语法 

| 方法          | 意义                                                         |
| ------------- | ------------------------------------------------------------ |
| \_\_enter\_\_ | 进入于此对象相关的上下文，如果存在该方法，with语法会把该方法的返回值作为绑定到as字句中指定的变量上 |
| \_\_exit\_\_  | 退出与此对象的上下文                                         |

exit 中变量的含义： 

​		1、exc_type：异常类型，如果没有异常，则返回是None 

​		2、exc_tb：异常追踪信息，如果没有异常，则是None 

​		3、exc_va：异常对应的值，如果没异常，则是None   此处的return 用于压制异常，若此处是False,则会抛出异常，等效True 或 False 缺少了enter 进不去，缺少了exitc出不来

**基础语法：**

```c
class A:
    def __init__(self):
        print("__init__")

    def __enter__(self):
        print("__enter__")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__")

with A() as f:
    pass
```

```c
__init__
__enter__
__exit__
```

```c
class A:
    def __init__(self):
        print("__init__")

    def __enter__(self):
        print("__enter__")
        return 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__")

a = A()
# 此处的f是__enter__的返回值，是a的参数，若此处__enter__无return，则默认返回为None，无意义
with a as f:
	# 即使是抛出异常，仍然会执行exit操作
	# raise Exception('error')	
    print(a==f)
    print(a is f)
    print(a)
    print(f)
```

```c
__init__
__enter__
False
False
<__main__.A object at 0x000002040C573BA8>
1
__exit__
```

```c
class A:
    def  __init__(self):
        print ('init instance')

    def  __enter__(self):
        print ('__enter__')
        return self

    def  __exit__(self, exc_type, exc_val, exc_tb):
        print ('__exit__')
        print (exc_tb) #追踪信息
        print (exc_type)  # 类型
        print (exc_val)  # 值
        return  1  # 此处设置为1 是压制异常，不让其出现

p=A()
with  p  as  f:  # 此处的f是__enter__的返回值，若此处__enter__无return，则默认返回为None，无意义
    #raise   Exception('Error1234454')
    print (p==f) # 此处用于比较p和f的关系
    print (p is f)
    print (p)
    print (f)
```

```c
init instance
__enter__
True
True
<__main__.A object at 0x000002F6D4E93BE0>
<__main__.A object at 0x000002F6D4E93BE0>
__exit__
None
None
None
```

### 9. 反射

反射：python中，能够通过一个对象，找出其type,class,attribute或method的能力，称为反射或自醒。

```javascript
object 可以是类或实例 
语法格式:
	getattr(object,name[,default]) : 通过name 返回object的属性值，当属性不存在时，将使用default返回，如果没有default，则抛出attributeError，name 必须位字符串 

	setattr(object,name,value) object 的属性存在，则覆盖，若不存在，则新增。

	hasattr(object,name)  判断对象是否有这个名字属性，name必须时字符串
```

```c
class A:
    x = 10
    def __init__(self):
        self.x = 5

setattr(A,'y',20)
print(getattr(A,'x'))
print(getattr(A,'y'))
print(A.__dict__)
print("-"*50)
a = A()
print(getattr(a,'x'))
print(getattr(a,'y'))
setattr(a,'z',55)
print(getattr(a,'z'))
print(a.__dict__)
```

```c
10
20
{'__module__': '__main__', 'x': 10, '__init__': <function A.__init__ at 0x000001AF5A192B70>, '__dict__': <attribute '__dict__' of 'A' objects>, '__weakref__': <attribute '__weakref__' of 'A' objects>, '__doc__': None, 'y': 20}
--------------------------------------------------
5
20
55
{'x': 5, 'z': 55}
```

```c
class A:
    x = 10
    def __init__(self,y):
        self.x = 5
        self.y = y

a=A(20)
# 类添加一个函数属性
setattr(A,'printf',lambda self: 1)

# 实例添加一个属性
setattr(a,'myclass',lambda : 10)

print(getattr(a,'printf')())
print(getattr(a,'myclass')())

if not hasattr(A,'sub'):
    setattr(A,'sub',lambda self,other: self.y - other.y)

if not hasattr(A,'add'):
    setattr(A,'add',lambda self,other: self.y + other.y)

print(A.__dict__)
print(a.__dict__)

b1 = A(20)
b2 = A(30)

print(b1.sub(b2))
print(b1.add(b2))
```

```c
1
10
{'__module__': '__main__', 'x': 10, '__init__': <function A.__init__ at 0x0000028FDD972B70>, '__dict__': <attribute '__dict__' of 'A' objects>, '__weakref__': <attribute '__weakref__' of 'A' objects>, '__doc__': None, 'printf': <function <lambda> at 0x0000028FDD7A2EA0>, 'sub': <function <lambda> at 0x0000028FDD984E18>, 'add': <function <lambda> at 0x0000028FDD984D08>}
{'x': 5, 'y': 20, 'myclass': <function <lambda> at 0x0000028FDD984C80>}
<__main__.A object at 0x0000028FDD986898>
50
```

**运行时注册：**

```c
class Dispatcher:
    def __init__(self):
        pass

    def cmd1(self):
        print("cmd1.........")

    def reg(self,cmd,fn):
        if isinstance(cmd,str):
            setattr(self.__class__,cmd.strip(),fn)
        else:
            print("type error...")

    def run(self):
        while True:
            cmd = input("please input str:")
            if cmd.strip() == 'q' or cmd.strip() == 'quit':
                return
            getattr(self,cmd.strip(),self.defaultrun())()

    def defaultrun(self):
        print("defaultrun...")

dsp = Dispatcher()
dsp.reg("cmd2",lambda self: print("cmd2"))
dsp.reg("cmd3",lambda self: print("cmd3"))
dsp.run()
```

```c
please input str:cmd1
cmd1.........
please input str:cmd2
cmd2
please input str:cmd3
cmd3
please input str:q
```

**反射相关魔术方法：**

| 魔术方法               | 意义                                                         |
| ---------------------- | ------------------------------------------------------------ |
| \_\_getattr\_\_()      | 当通过搜索实例，实例的类以及祖先类查不到的属性，就会调用此方法 |
| \_\_setattr\_\_()      | 通过访问实例属性，进行增加，修改都要调用它                   |
| \_\_delattr\_\_()      | 当通过实例删除属性的时候调用此方法                           |
| \_\_getattribute()\_\_ | 实例所有的属性调用都是此方法开始                             |

```c
class A():
    m=6
    def __init__(self,x):
        print ('init')
        self.x=x  #此处定义了属性，所以下面的__setattr__被执行了一次，初始化先执行，之后__setattr__这个属性再执行一次

    def __getattr__(self, item):#针对上述无法查找到的属性，则执行此属性，可配置其值为None来弥补此属性值
        print ('__getattr__',item)
        self.__dict__[item]=None

    def __setattr__(self, key, value): #设置一个属性时，一定要执行，至于是否生效，则另当别论
        print ('__setattr__',key,value)

    def __delattr__(self, item): #此处在删除一个实例的属性进行的操作，只要实例能找到，都能够删除
        print ('__delattr__',item)

A.n=50 # 此处是正常的添加类属性，不会产生其他的报错
print(A.__dict__)
print("-"*50)

a=A(20)
print (a.__dict__)
print("-"*50)

print(a.b)  # 针对不存在的属性进行调用
print("-"*50)

print(a.m)  # 针对存在的属性进行调用
print("-"*50)

print(a.x)  # 针对实例属性
print("-"*50)

a.x=30  # 设置实例的属性变化
print("-"*50)

a.c=200     # 添加一个不存在的属性
print("-"*50)

del  a.m    # 删除一个实例的属性
print("-"*50)

print (a.__dict__)
```

```c
{'__module__': '__main__', 'm': 6, '__init__': <function A.__init__ at 0x0000022B42D32B70>, '__getattr__': <function A.__getattr__ at 0x0000022B42D44C80>, '__setattr__': <function A.__setattr__ at 0x0000022B42D44E18>, '__delattr__': <function A.__delattr__ at 0x0000022B42D44D08>, '__dict__': <attribute '__dict__' of 'A' objects>, '__weakref__': <attribute '__weakref__' of 'A' objects>, '__doc__': None, 'n': 50}
--------------------------------------------------
init
__setattr__ x 20
{}
--------------------------------------------------
__getattr__ b
None
--------------------------------------------------
6
--------------------------------------------------
__getattr__ x
None
--------------------------------------------------
__setattr__ x 30
--------------------------------------------------
__setattr__ c 200
--------------------------------------------------
__delattr__ m
--------------------------------------------------
{'b': None, 'x': None}
```

```c
class A():
    m=6
    def __init__(self,x):
        print ('init')
        self.x=x  # 此处定义了属性，所以下面的__setattr__被执行了一次，初始化先执行，之后__setattr__这个属性再执行一次

    def __getattr__(self, item):# 针对上述无法查找到的属性，则执行此属性，可配置其值为None来弥补此属性值
        print ('__getattr__',item)
        self.__dict__[item]=None

    def __setattr__(self, key, value): # 设置一个属性时，一定要执行，至于是否生效，则另当别论
        print ('__setattr__',key,value)

    def __delattr__(self, item): # 此处在删除一个实例的属性进行的操作，只要实例能找到，都能够删除
        print ('__delattr__',item)

    def __getattribute__(self, item):  # 此处是在字典属性之前进行拦截执行
        print ('__getattribute__',item)
a=A(20)
print("-"*50)
print(a.x)
print("-"*50)
print(a.m)
```

```c
init
__setattr__ x 20
--------------------------------------------------
__getattribute__ x
None
--------------------------------------------------
__getattribute__ m
None
```

**结论：**

```c
实例的所有属性的访问，第一个都会调用__getattribute__方法，其阻止了属性查找，该方法应该返回(计算后)值或者抛出一个attributeError 异常，他的return 值将作为属性查找的结果，如果抛出attributeError 异常，则会直接调用__getattr__方法，因为表示属性没有找到，如下
```

```c
class A():
    m=6
    def __init__(self,x):
        print ('init')
        self.x=x  #此处定义了属性，所以下面的__setattr__被执行了一次，初始化先执行，之后__setattr__这个属性再执行一次

    def __getattr__(self, item):#针对上述无法查找到的属性，则执行此属性，可配置其值为None来弥补此属性值
        print ('__getattr__',item)
        # self.__dict__[item]=None

    def __setattr__(self, key, value): #设置一个属性时，一定要执行，至于是否生效，则另当别论
        print ('__setattr__',key,value)

    def __delattr__(self, item): #此处在删除一个实例的属性进行的操作，只要实例能找到，都能够删除
        print ('__delattr__',item)

    def __getattribute__(self, item):  #此处是在字典属性之前进行拦截执行
        print ('__getattribute__',item)
        raise  AttributeError(item)  # 此处若属性不存在，抛出异常，则直接进入getattr中机型处理
        #return object.__getattribute__(self, item)  # 此处表示若不存在，则直接去object中进行查找，并得到其访问的值
a=A(20)

print(a.x)
```

```c
init
__setattr__ x 20
__getattribute__ x
__getattr__ x
None
```

**注意：\_\_getattribute\_\_ 方法中为了避免在该方法中无限递归，实现了应该永久调用基类的同名方法以访问需要的任何属性，除非你明确知道\_\_getattribute\_\_方法用来做什么，否则不要使用它。**

**总结：**

**属性查找顺序** **实例调用----> \_\_getattribute\_\_()----> instance.dict---->instance.class----> 继承的祖先类(知道object)的\_\_dict\_\_调用\_\_getattr\_\_()**

### 10. 描述器

在python中，一个类实现了一下三种方式中的任何一种，就是描述器

```c
object.__get__(self,instance,owner)
object.__set__(self,instance,value)
object.__delete__(self,instance)
```

**如果仅实现了\_\_get\_\_，就是非数据描述器 non-data descriptor**   

**同时实现了\_\_get\_\_和\_\_set\_\_或者\_\_get\_\_和\_\_delete\_\_ 或者三个都实现，则称为数据描述符  data  descriptor**  

**如果一个类的类属性设置为描述器，那么那被称为owner属主。**

**实例：非数据描述器**

```c
class A:
    def  __init__(self):
        print ('A,init')
        self.a1='a1'

class B:
    x=A()  # 调用上述的类形成实例
    def __init__(self):
        print ('B,init')
        self.x=100  # 此处B类实例的属性为x=100

print  (B.x.a1)  # 此处通过调用B类而调用B类的类属性x，进而调用A类的实例的a1方法.必须是先初始化，然后再进行相关的调用

b=B()  # 此处调用从类开始，会执行A和B的init方法
print  (b.x)   #此处调用的是实例B的x属性，其值是100，此处对x.a1没有属性，因为其被self.x=100覆盖了
```

```c
A,init
a1
B,init
100
```

**默认查找顺序： 类加载时，类变量需要先生成，而类B的x属性是类A的实例，因此需要先执行类A的初始化，进而执行B的初始化操作。**

```c
class A:
    def  __init__(self):
        print ('A,init')
        self.a1='a1'
            
    def __get__(self, instance, owner): #加入此方法,行为被拦截，执行了init后执行了此方法，返回为None,因此后面调用的None
        return (self,instance,owner)

class B:
    x=A()  # 调用上述的类形成实例
    def __init__(self):
        print ('B,init')
        self.x=100  # 此处B类实例的属性为x=100

print(B.x)  # 此处x对应的a1的属性被拦截，上述返回为x实例，instance为B类实例的返回，owner为B类，及就是属性所属的类，self为A类的实例
b=B()  # 对类B进行实例化
print(b.x)  # 对类b的属性进行调用
```

```c
A,init
(<__main__.A object at 0x00000205A6383BE0>, None, <class '__main__.B'>)
B,init
100
```

```c
class A:
    def  __init__(self):
        print ('A,init')
        self.a1='a1'
    def __get__(self, instance, owner): #加入此方法，行为被拦截，执行了init后执行了此方法，返回为None,因此后面调用的None
        return (self,instance,owner)

class B:
    x=A()  # 调用上述的类形成实例
    def __init__(self):
        print ('B,init')
        self.x=A()  # 此处B类实例的属性为调用A类的属性

b=B()  # 对类B进行实例化
print("-"*50)
print (b.x.a1)  # 对类b的属性进行调用,此处调用的是A类的属性，此处没有触动__get__魔术方法，进而说明__get__和实例无关
```

```c
A,init
B,init
A,init
--------------------------------------------------
a1
```

**结论： \_\_get\_\_()魔术方法只对调用的类有拦截作用，对类B下的实例无任何作用，此\_\_get\_\_是在调用子类的类属性时会执行此方法。**

```c
class A:
    def  __init__(self):
        print ('A,init')
        self.a1='a1'

    def __get__(self, instance, owner): #加入此方法,行为被拦截,执行了init后执行了此方法，返回为None,因此后面调用的None
        return   self # 此处返回self,则表示A的实例，A的实例当然可以调用a1方法

class B:
    x=A()  # 调用上述的类形成实例
    def __init__(self):
        print ('B,init')
        self.x=A()  # 此处B类实例的属性为调用A类的属性

print(B.x.a1)# 此处因为返回的是self,及A的实例，因此此处可以调用A实例的a1方法，自然是成功的
B.x.a1=30 #通过描述器来修改属主的状态
print("-"*50)
print(B.x.a1)  # 打印状态
```

```c
A,init
a1
--------------------------------------------------
30
```

**实例：数据描述器**

```c
class A:
    def  __init__(self):
        print ('A,init')
        self.a1='a1'

    def __get__(self, instance, owner): #加入此方法，行为被拦截，执行了init后执行了此方法，返回为None,因此后面调用的None
        print ('__get__',self,instance,owner)
        return   self # 此处返回self,则表示A的实例，A的实例当然可以调用a1方法

    # def __set__(self, instance, value): #实例化B类时需要调用此方法，
    #     print ('__set__',self,instance,value)

class B:
    x=A()  # 调用上述的类形成实例
    def __init__(self):
        print ('B,init')
        self.x=100  # 此处B类实例的属性为调用A类的属性
b=B()
print("-"*50)
print(b.__dict__)  # 打印实例b对应的属性字典
print('+'*30)
print(b.x.a1)  #此处默认的a1方法是不存在于b实例中，使用set方法将跳过b中定义的self.x方法
```

```c
A,init
B,init
--------------------------------------------------
{'x': 100}
++++++++++++++++++++++++++++++
Traceback (most recent call last):
  File "D:/python-scripts/scripts/test.py", line 1272, in <module>
    print(b.x.a1)  #此处默认的a1方法是不存在于b实例中，使用set方法将跳过b中定义的self.x方法
AttributeError: 'int' object has no attribute 'a1'
```

```c
class A:
    def  __init__(self):
        print ('A,init')
        self.a1='a1'

    def __get__(self, instance, owner): #加入此方法，行为被拦截，执行了init后执行了此方法，返回为None,因此后面调用的None
        print ('__get__',self,instance,owner)
        return   self # 此处返回self,则表示A的实例，A的实例当然可以调用a1方法

    def __set__(self, instance, value): #实例化B类时需要调用此方法，
        print ('__set__',self,instance,value)

class B:
    x=A()  # 调用上述的类形成实例
    def __init__(self):
        print ('B,init')
        self.x=100  # 此处B类实例的属性为调用A类的属性
b=B()
print("-"*50)
print(b.__dict__)  # 打印实例b对应的属性字典
print('+'*30)
print(b.x.a1)  #此处默认的a1方法是不存在于b实例中，使用set方法将跳过b中定义的self.x方法
```

```c
A,init
B,init
__set__ <__main__.A object at 0x000001375E736748> <__main__.B object at 0x000001375E7367B8> 100
--------------------------------------------------
{}
++++++++++++++++++++++++++++++
__get__ <__main__.A object at 0x000001375E736748> <__main__.B object at 0x000001375E7367B8> <class '__main__.B'>
a1
```

```c
class A:
    def  __init__(self):
        print ('A,init')
        self.a1='a1'

    def __get__(self, instance, owner): #加入此方法，行为被拦截，执行了init后执行了此方法，返回为None,因此后面调用的None
        print ('__get__',self,instance,owner)
        return self # 此处返回self,则表示A的实例，A的实例当然可以调用a1方法

    def  __set__(self, instance, value): #实例化B类时需要调用此方法，
        print ('__set__',self,instance,value)
        self.a1=value  # 若此处定义a1的返回值为value,及类B对应的实例属性x的值，则此处在访问时，其结果便是100

class B:
    x=A()  # 调用上述的类形成实例
    def __init__(self):
        print ('B,init')
        self.x=100  # 此处B类实例的属性为调用A类的属性
b=B()
print (b.__dict__)  # 打印实例b对应的属性字典
print ('+'*30)
print (b.x.a1)  # 此处最终访问__get__的原因是此处调用的是类的属性，而不是实例的属性，因此__get__会生效
```

```c
A,init
B,init
__set__ <__main__.A object at 0x000001D8FA426710> <__main__.B object at 0x000001D8FA426780> 100
{}
++++++++++++++++++++++++++++++
__get__ <__main__.A object at 0x000001D8FA426710> <__main__.B object at 0x000001D8FA426780> <class '__main__.B'>
100
```

**结论：**

**当一个类的类属性是一个数据描述器时（及除了\_\_get\_\_方法外还有至少一种方法），对他的实例属性描述器的操作相当与对应的类的属性进行操作，及实例的字典优先级会降低，而类的字典的优先级会升高，实际的结果是当其成为数据属性描述器时，其对应的实例的字典中定义的实例属性将会消失**



**属性查找顺序：** 

**实例的dict优先于非数据描述器(只有\_\_get\_\_方法)，数据描述器优先于实例的\_\_dict\_\_  ,及数据描述器---> 实例的\_\_dict_\_\_---> 非数据描述器---> 类的\_\_dict\_\_**

# 5.常用模块

## 5.1 os 模块

**1. os.name**

该属性宽泛地指明了当前 Python 运行所在的环境，实际上是导入的操作系统相关模块的名称.目前有效名称为以下三个：posix，nt，java。其中posix是 Portable Operating System Interface of UNIX（可移植操作系统接口）的缩写。Linux 和 Mac OS 均会返回该值；nt全称应为“Microsoft Windows NT”，大体可以等同于 Windows 操作系统，因此 Windows 环境下会返回该值；java则是 Java 虚拟机环境下的返回值。

```c
>> print(os.name)
posix
```

**2. os.environ**

属性可以返回环境相关的信息，主要是各类环境变量。

```c
>> print(os.environ["PATH"])
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/data/tools/jdk/bin:/root/bin
```

**3. os.walk()**

这个函数需要传入一个路径作为`top`参数，函数的作用是在以`top`为根节点的目录树中游走，对树中的每个目录生成一个由`(dirpath, dirnames, filenames)`三项组成的三元组。其中，`dirpath`是一个指示这个目录路径的字符串，`dirnames`是一个`dirpath`下子目录名（除去`“.”`和`“..”`）组成的列表，`filenames`则是由`dirpath`下所有非目录的文件名组成的列表。要注意的是，这些名称并不包含所在路径本身，要获取`dirpath`下某个文件或路径从`top`目录开始的完整路径，需要使用`os.path.join(dirpath, name)`。

注意最终返回的结果是一个迭代器，我们可以使用`for`语句逐个取得迭代器的每一项：

```c
for dir in os.walk("/root/"):
    print(dir)
```

**4. os.listdir()**

“listdir”即“list directories”，列出（当前）目录下的全部路径（及文件）。该函数存在一个参数，用以指定要列出子目录的路径，默认为`“.”`，即“当前路径”。函数返回值是一个列表，其中各元素均为字符串，分别是各路径名和文件名。通常在需要遍历某个文件夹中文件的场景下极为实用。

```c
//获取对应目录下的所有普通文件
def getfile(dir):
    dir = os.listdir(dir)
    filelist = []
    for file in dir:
        if(os.path.isfile(file)):
            filelist.append(file)
    return filelist
                
print(getfile("/root"))		
```

**5. os.mkdir()**

mkdir”，即“make directory”，用处是“新建一个路径”。需要传入一个类路径参数用以指定新建路径的位置和名称，如果指定路径已存在，则会抛出`FileExistsError`异常。该函数只能在已有的路径下新建一级路径，否则（即新建多级路径）会抛出`FileNotFoundError`异常。相应地，在需要新建多级路径的场景下，可以使用`os.makedirs()`来完成任务。函数`os.makedirs()`执行的是递归创建，若有必要，会分别新建指定路径经过的中间路径，直到最后创建出末端的“叶子路径”。

```c
os.mdkir("/root/test")
os.makedirs("/root/test/world/hello")
```

**6. os.remove()**

用于删除文件，如果指定路径是目录而非文件的话，就会抛出`IsADirectoryError`异常。删除目录应该使用`os.rmdir()`函数。同样的，对应于`os.makedirs()`，删除路径操作`os.rmdir()`也有一个递归删除的函数`os.removedirs()`，该函数会尝试从最下级目录开始，逐级删除指定的路径，几乎就是一个`os.makedirs()`的逆过程；一旦遇到非空目录即停止。

```c
os.remove("/root/test/hello/world")		#不能删除目录
os.rmdir("/root/test/hello/world")		#删除指定目录
os.remove("/root/test/hello/t/test.file")		#删除指定文件
os.removedirs("/root/test/hello/t")	 #从t目录开始往前删除，遇到目录不为空即停止，如删除t目录，删除hello目录，删除test目录...
```

**7. os.rename()**

修改目录名，一般调用格式为`os.rename(src, dst)`

```c
 os.rename('/root/hello','/root/world')
```

**8. os.getcwd()**

"getcwd"实际上是“get the current working directory”的简写，顾名思义，也就是说这个函数的作用是 "获取当前工作路径"。

```c
os.getcwd()
```

**9. os.chdir()**

“chdir”其实是“change the directory”的简写，因此`os.chdir()`的用处实际上是切换当前工作路径为指定路径。

```c
os.chdir("/home/justdopython/just/do")   # 也可将参数指定为".."，即可切换到父目录
```

**10. os.path.join()**

将多个传入路径组合为一个路径。实际上是将传入的几个字符串用系统的分隔符连接起来，组合成一个新的字符串，所以一般的用法是将第一个参数作为父目录，之后每一个参数即使下一级目录，从而组合成一个新的符合逻辑的路径。但如果传入路径中存在一个“绝对路径”格式的字符串，且这个字符串不是函数的第一个参数，那么其他在这个参数之前的所有参数都会被丢弃，余下的参数再进行组合。更准确地说，只有最后一个“绝对路径”及其之后的参数才会体现在返回结果中。

```c
>>> os.path.join("/just", "do", "python", "dot", "com")
'/just/do/python/dot/com'
>>> 
>>> os.path.join("/just", "do", "/python", "dot", "com")
'/python/dot/com'
>>> 
>>> os.path.join("just", "do", "python", "dot", "/", "com")
'/com'
```

**11. os.path.abspath()**

  将传入路径规范化，返回一个相应的绝对路径格式的字符串。

```c
os.path.abspath('/python//dot///com')
'/python/dot/com'
```

**12. os.path.basename()**

该函数返回传入路径的“基名”，即传入路径的最下级目录。

```c
os.path.basename('/python/dot/com')
'com'
```

**13. os.path.dirname()**

返回的是最后一个分隔符前的整个字符串。

```c
os.path.dirname('/python/dot/com')
'/python/dot'
```

**14. os.path.split()**

函数`os.path.split()`的功能就是将传入路径以最后一个分隔符为界，分成两个字符串，并打包成元组的形式返回；前两个函数`os.path.dirname()`和`os.path.basename()`的返回值分别是函数`os.path.split()`返回值的第一个、第二个元素。

```c
os.path.split('/python/dot/com') 
('/python/dot', 'com')
```

**15. os.path.exists()**

判断路径所指向的位置是否存在。若存在则返回`True`，不存在则返回`False`

```c
>>> os.path.exists('/root')
True
>>> os.path.exists('/hello')
False
```

**16. os.path.isabs()**

该函数判断传入路径是否是绝对路径，若是则返回`True`，否则返回`False`

```c
>>> os.path.isabs('/root/hello')
True
>>> os.path.isabs('hello')      
False
```

**17. os.path.isfile() 和 os.path.isdir()**

这两个函数分别判断传入路径是否是文件或路径，注意，此处会核验路径的有效性，如果是无效路径将会持续返回`False`。

```c
>>> os.path.isfile('/root')
False
>>> os.path.isfile('/root/test.py')
True
>>> os.path.isdir('/root/test.py') 
False
>>> os.path.isdir('/root')        
True
```

**18. os.system**

system函数可以将字符串转化成命令在服务器上运行；其原理是每一条system函数执行时，其会创建一个子进程在系统上执行命令行，子进程的执行结果无法影响主进程；

```c
>>> os.system('cd /root/hello && mkdir /root/hello/test.file' )
```

## 5.2 sys 模块

**1. sys.argv**

“argv”即“argument value”的简写，是一个列表对象，其中存储的是在命令行调用 Python 脚本时提供的“命令行参数”。

```c
print("the first arguments is ",sys.argv)
print("the first arguments is ",sys.argv[0])
print("the first arguments is ",sys.argv[1])
print("the first arguments is ",sys.argv[2])
```

**2. sys.platform**

查看`sys`模块中的`sys.platform`属性可以得到关于运行平台更详细的信息,比较一下`os.name`的结果，不难发现，`sys.platform`的信息更加准确。

```c
sys.platform
```

**3. sys.byteorder**

“byteorder”即“字节序”，指的是在计算机内部存储数据时，数据的低位字节存储在存储空间中的高位还是低位。“小端存储”时，数据的低位也存储在存储空间的低位地址中，此时`sys.byteorder`的值为`“little”`。如果不注意，在按地址顺序打印内容的时候，可能会把小端存储的内容打错。当前**大部分机器**都是使用的小端存储。而另外还存在一种存储顺序是“大端存储”，即数据的高位字节存储在存储空间的低位地址上，此时`sys.byteorder`的值为`“big”`。

```c
print(sys.byteorder)
little
```

**4. sys.executable**

该属性是一个字符串，在正常情况下，其值是当前运行的 Python 解释器对应的可执行程序所在的绝对路径。

```c
print(sys.executable)
/usr/bin/python
```

**5. sys.modules**

该属性是一个字典，包含的是各种已加载的模块的模块名到模块具体位置的映射。

**6. sys.builtin_module_names**

该属性是一个字符串元组，其中的元素均为当前所使用的的 Python 解释器内置的模块名称。注意区别`sys.modules`和`sys.builtin_module_names`——前者的关键字（keys）列出的是导入的模块名，而后者则是解释器内置的模块名。

```c
('__builtin__', '__main__', '_ast', '_codecs', '_sre', '_symtable', '_warnings', '_weakref', 'errno', 'exceptions', 'gc', 'imp', 'marshal', 'posix', 'pwd', 'signal', 'sys', 'thread', 'zipimport')
```

**7. sys.path**

该属性是一个由字符串组成的列表，其中各个元素表示的是 Python 搜索模块的路径；在程序启动期间被初始化。其中第一个元素（也就是`path[0]`）的值是最初调用 Python 解释器的脚本所在的绝对路径；如果是在交互式环境下查看`sys.path`的值，就会得到一个空字符串。

```c
>>> print(sys.path)
['/root/script', '/usr/lib64/python27.zip', '/usr/lib64/python2.7', '/usr/lib64/python2.7/plat-linux2', '/usr/lib64/python2.7/lib-tk', '/usr/lib64/python2.7/lib-old', '/usr/lib64/python2.7/lib-dynload', '/usr/lib64/python2.7/site-packages', '/usr/lib/python2.7/site-packages']

>>> print(sys.path[0])
/root/script
```

**8. sys.stdin、sys.stdout、sys.err**

标准输入、标准输出、标准错误

```c
sys.stdin:
//sys.stdin.readline( )会将标准输入全部获取，包括末尾的'\n'，因此用len计算长度时是把换行符'\n'算进去了的，但是input( )获取输入时返回的结果是不包含末尾的换行符'\n'的。
	s1 = input()		//2.7版本为 raw_input()
	s2 = sys.stdin.readline()
	print(len(s1))
	print(len(s2))


sys.stdout:
//以下两行代码的作用类似
    sys.stdout.write('hello' + '\n')
    print('hello')
        
sys.err:
```

**9. sys.getrecursionlimit() 和 sys.setrecursionlimit()**

`sys.getrecursionlimit()`和`sys.setrecursionlimit()`是成对的。前者可以获取 Python 的最大递归数目，后者则可以设置最大递归数目。因为初学阶段很少用到，因此只做了解。

**10. sys.getrefcount()**

其返回值是 Python 中某个对象被引用的次数

**11. sys.getsizeof()**

这个函数的作用与 C 语言中的`sizeof`运算符类似，返回的是作用对象所占用的字节数。

```c
sys.getsizeof(1)
```

**12. sys.int_info 和 sys.float_info**

```c

```

## 5.3 commands 模块

**在3.x版本总，getstatus()方法被移除，getoutput()和getstatusoutput()被放到了subprocess模块中。**

**1.getoutput(cmd)**

执行cmd命令，并返回输出的内容，返回结果为str。

```c
>>> out = commands.getoutput("ls -l")
>>> print(out)
-r-xr-x--- 1 serv service 377 115 16:06 free.py
```

**2.getstatus(file)**

返回执行ls -ld file命令的结果。该函数已被python丢弃，不建议使用。

```c
>>> commands.getstatus("test.py")  
'-rw-r--r-- 1 root root 160 May 10 02:56 test.py'
```

**3.getstatusoutput(cmd)** 

执行cmd命令，并返回执行的状态和输出的内容，返回结果为int和str。返回正确int值为0

```c
>>> status,out=commands.getstatusoutput("ls -l /root")
>>> print(status)
0
>>> print(out)
-r-xr-x--- 1 serv service 377 115 16:06 free.py
```

## 5.4 datetime 模块

datetime模块重新封装了time模块，提供更多的接口，提供的类有： 

​	**date : 表示日期的类** 

​	**time : 表示时间的类** 

​	**datetime : 表示日期和时间的类** 

​	**timedelta : 表示时间间隔，即两个时间点的间隔** 

​	**tzinfo : 与时区有关的信息** 

( 这些类的对象都是不可变的 ) 

( 类有类方法，类方法里有方法，方法继承了类方法）

### 1. date类

**datetime.date（year，month，day）**

常用的类方法与属性：

| 属性或类方法                                      | 概述                                                 |
| ------------------------------------------------- | ---------------------------------------------------- |
| datetime.date.max                                 | 对象所能表示的最大日期（9999-12-31）                 |
| datetime.date.min                                 | 对象所能表示的最小日期（0001-01-01）                 |
| datetime.date.today()                             | 返回一个表示当前本地时间的date对象                   |
| datetime.date.resolution                          | date对象表示日期的最小单位（天）                     |
| datetime.date.fromtimestamp(timestamp)            | 根据给定的时间戳，返回一个date对象                   |
| datetime.date.year                                | 年对象                                               |
| datetime.date.month                               | 月对象                                               |
| datetime.date.day                                 | 日对象                                               |
| datetime.date.today().replace(year[,month[,day]]) | 生成并返回一个新的日期对象，原日期对象不变           |
| datetime.date.today().timetuple()                 | 返回日期对应的时间元组（time.struct_time）对象       |
| datetime.date.today().toordinal()                 | 返回日期是自0001-01-01开始的第多少天                 |
| datetime.date.today().weekday()                   | 返回日期是星期几，[0,6],0表示星期一，1表示星期二     |
| datetime.date.today().isoweekday()                | 返回日期是星期几，[1,7],1表示星期一，2表示星期二     |
| datetime.date.today().isocalendar()               | 返回格式为（year，weekday，isoweekday）的元组        |
| datetime.date.today().isoformat()                 | 返回‘YYYY-MM-DD’格式的日期字符串                     |
| datetime.date.today().strftime()                  | 自定义格式化字符串（和time模块的strftime()方法相同） |

实例：

```c
import datetime
import time

print("datetime.date.max:",datetime.date.max)
print("datetime.date.min:",datetime.date.min)
print("datetime.date.today():",datetime.date.today())
print("datetime.date.resolution:",datetime.date.resolution)
print("datetime.date.fromtimestamp(time.time()+3600000):",datetime.date.fromtimestamp(time.time()+3600000))	# 添加单位为秒
print("datetime.date.year:",datetime.date.year) #年对象
print("datetime.date.month:",datetime.date.month) #月对象
print("datetime.date.day:",datetime.date.day)  #日对象
print("datetime.date.today().year:",datetime.date.today().year) # 本地时时间的年
print("datetime.date.today().month:",datetime.date.today().month) # 本地时时间的月
print("datetime.date.today().day:",datetime.date.today().day) # 本地时间的日
print("datetime.date.today().replace(year=2019):",datetime.date.today().replace(year=2019))
print("datetime.date.today().timetuple():",datetime.date.today().timetuple())
print("datetime.date.today().toordinal():",datetime.date.today().toordinal())
print("datetime.date.today().weekday():",datetime.date.today().weekday())
print("datetime.date.today().isoweekday():",datetime.date.today().isoweekday())
print("datetime.date.today().isocalendar():",datetime.date.today().isocalendar())
print("datetime.date.today().isoformat():",datetime.date.today().isoformat())
print("datetime.date.today().strftime('%Y-%m-%d-%a-%I'):",datetime.date.today().strftime('%Y-%m-%d-%a-%I'))
    
    
datetime.date.max: 9999-12-31
datetime.date.min: 0001-01-01
datetime.date.today(): 2021-05-13
datetime.date.resolution: 1 day, 0:00:00
datetime.date.fromtimestamp(time.time()+3600000): 2021-06-24
datetime.date.year: <attribute 'year' of 'datetime.date' objects>
datetime.date.month: <attribute 'month' of 'datetime.date' objects>
datetime.date.day: <attribute 'day' of 'datetime.date' objects>
datetime.date.today().year: 2021
datetime.date.today().month: 5
datetime.date.today().day: 13
datetime.date.today().replace(year=2019): 2019-05-13
datetime.date.today().timetuple(): time.struct_time(tm_year=2021, tm_mon=5, tm_mday=13, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=133, tm_isdst=-1)
datetime.date.today().toordinal(): 737923
datetime.date.today().weekday(): 3
datetime.date.today().isoweekday(): 4
datetime.date.today().isocalendar(): (2021, 19, 4)
datetime.date.today().isoformat(): 2021-05-13
datetime.date.today().strftime('%Y-%m-%d-%a-%I'): 2021-05-13-Thu-12
```

### 2. time类

其中，time类和time模块各自独立 

**datetime.time(hour[,minute[,decond[,microsecond[,tzinfo]]]])**

常用的类方法与属性：

| 属性或类方法              | 概述                                                         |
| ------------------------- | ------------------------------------------------------------ |
| datetime.time.max         | 表示的最大时间                                               |
| datetime.time.min         | 表示的最小时间                                               |
| datetime.time.resolution  | 时间的最小单位，这里是1微秒                                  |
| datetime.time.hour        | 时对象                                                       |
| datetime.time.minute      | 分对象                                                       |
| datetime.time.second      | 秒对象                                                       |
| datetime.time.microsecond | 分秒对象                                                     |
| datetime.time.tzinfo      | 时区信息                                                     |
| datetime.time.replace()   | 用参数指定替代（时，分，秒，微秒，时区）对象，生成并返回新的对象 |
| datetime.time.isoformat() | 返回'HH:MM:SS'格式字符串                                     |
| datetime.time.strftime()  | 返回自定义格式化字符串                                       |

实例：

```c
import datetime
import time

print("datetime.time.max:",datetime.time.max)
print("datetime.time.min:",datetime.time.min)
print("datetime.time.resolution:",datetime.time.resolution)
print("datetime.time.hour:",datetime.time.hour)
print("datetime.time.minute:",datetime.time.minute)
print("datetime.time.second:",datetime.time.second)
print("datetime.time.microsecond:",datetime.time.microsecond)
print("datetime.time.tzinfo:",datetime.time.tzinfo)
```

### 3. datetime类

相当于date和time结合起来 

**datetime.datetime(year,month,day[,hour[,minute[,second[,microsecond[,tzinfo]]]]])**

常用的类方法与属性：

| 属性或类方法                           | 概述                                                         |
| -------------------------------------- | ------------------------------------------------------------ |
| datetime.max                           | 最大日期                                                     |
| datetime.min                           | 最小日期                                                     |
| datetime.resolution                    | datetime对象所表示日期的最小单位，1微秒                      |
| datetime.today()                       | 返回当前本地时间                                             |
| datetime.now([tz])                     | 返回当前本地时间，如果指定tz，则返回tz时区当地时间           |
| datetime.utcnow()                      | 返回当前UTC时间                                              |
| datetime.fromtimestamp(timestamp[,tz]) | 根据给定的时间戳返回datetime对象，如果指定tz,则返回tz时区datetime对象 |
| datetime.utcfromtimestamp(timestamp)   | 根据时间戳创建一个datetime对象                               |
| datetime.combine(date,time)            | 把指定的date和time对象整合为datetime对象                     |
| datetime.strftime(date_string,format)  | 将格式化字符串转换为datetime对象                             |
| dt.year                                | 年对象                                                       |
| dt.month                               | 月对象                                                       |
| dt.day                                 | 日对象                                                       |
| dt.hour                                | 时对象                                                       |
| dt.minute                              | 分对象                                                       |
| dt.second                              | 秒对象                                                       |
| dt.microsecond                         | 微妙对象                                                     |
| dt.tzinfo                              | 时区对象                                                     |
| dt.date()                              | 获取dt的date对象                                             |
| dt.time()                              | 获取dt的time对象，tzinfo 为none                              |
| dt.timetz()                            | 获取dt的time对象，tzinfo 为与datetime的tzinfo相同            |
| dt.replace()                           | 指定参数替代（年，月，日，时，分，秒，微妙，时区），生成并返回新对象 |
| dt.timetuple()                         | 返回日期时间对应的时间元组（time.struct_time）（不包括tzinfo） |
| dt.utctimetuple()                      | 返回UTC时间对应的时间元组（不包括tzinfo）                    |
| dt.timestamp()                         | 返回dt对象对应的时间戳                                       |
| dt.toordinal()                         | 返回日期是是自 0001-01-01 开始的第多少天（与date类相同）     |
| dt.weekday()                           | 返回日期是星期几，[1, 7], 1表示星期一（与date类相同）        |
| dt.isocalendar()                       | 返回格式如（year，month，day）的时间元组（与date类相同）     |
| dt.isoformat()                         | 返回格式如'YYYY-MM-DD HH:MM:SS'的字符串                      |
| dt.ctime()                             | 等价与time模块的time.ctime（time.mktime(d.timetuple())）     |
| dt.strftime()                          | 返回指定格式的时间字符串                                     |

实例：

```c
print("datetime.datetime.max:",datetime.datetime.max)
print("datetime.datetime.min:",datetime.datetime.min)
print("datetime.datetime.resolution:",datetime.datetime.resolution)
print("datetime.datetime.today():",datetime.datetime.today())
print("datetime.datetime.now():",datetime.datetime.now())
print("datetime.datetime.utcnow():",datetime.datetime.utcnow())
print("datetime.datetime.fromtimestamp(time.time()):",datetime.datetime.fromtimestamp(time.time()))
print("datetime.datetime.utcfromtimestamp(time.time()):",datetime.datetime.utcfromtimestamp(time.time()))
print("datetime.datetime.combine(datetime.date(2019, 3, 5), datetime.time(3, 2, 45)):",datetime.datetime.combine(datetime.date(2019, 3, 5), datetime.time(3, 2, 45)))
print("datetime.datetime.strftime(datetime.date(2019,9,2),'%Y-%m-%d %X'):",datetime.datetime.strftime(datetime.date(2019,9,2),'%Y-%m-%d %X'))
print("datetime.datetime.year:",datetime.datetime.year)
print("datetime.datetime.today().tzinfo:",datetime.datetime.today().tzinfo)
print("datetime.datetime.today().date():",datetime.datetime.today().date())
print("datetime.datetime.today().time():",datetime.datetime.today().time())
print("datetime.datetime.today().timetz():",datetime.datetime.today().timetz())
print("datetime.datetime.today().timetuple():",datetime.datetime.today().timetuple())
print("datetime.datetime.today().timestamp():",datetime.datetime.today().timestamp())
print("datetime.datetime.today().ctime():",datetime.datetime.today().ctime())
    
datetime.datetime.max: 9999-12-31 23:59:59.999999
datetime.datetime.min: 0001-01-01 00:00:00
datetime.datetime.resolution: 0:00:00.000001
datetime.datetime.today(): 2021-05-13 15:11:04.426012
datetime.datetime.now(): 2021-05-13 15:11:04.426011
datetime.datetime.utcnow(): 2021-05-13 07:11:04.426011
datetime.datetime.fromtimestamp(time.time()): 2021-05-13 15:11:04.426012
datetime.datetime.utcfromtimestamp(time.time()): 2021-05-13 07:11:04.426012
datetime.datetime.combine(datetime.date(2019, 3, 5), datetime.time(3, 2, 45)): 2019-03-05 03:02:45
datetime.datetime.strftime(datetime.date(2019,9,2),'%Y-%m-%d %X'): 2019-09-02 00:00:00
datetime.datetime.year: <attribute 'year' of 'datetime.date' objects>
datetime.datetime.today().tzinfo: None
datetime.datetime.today().date(): 2021-05-13
datetime.datetime.today().time(): 15:11:04.426012
datetime.datetime.today().timetz(): 15:11:04.426012
datetime.datetime.today().timetuple(): time.struct_time(tm_year=2021, tm_mon=5, tm_mday=13, tm_hour=15, tm_min=11, tm_sec=4, tm_wday=3, tm_yday=133, tm_isdst=-1)
datetime.datetime.today().timestamp(): 1620889864.426012
datetime.datetime.today().ctime(): Thu May 13 15:11:04 2021
```



### 4. timedelta类

时间加减（代表了两个datetime之间的时间差） 

**datetime.timedalta(days=0,seconds=0,microseconds=0,milliseconds=0,minutes=0 ,hours=0,weeks=0)** 

在日期上做天，小时，分钟，秒，毫秒，微秒,周 的时间计算 

    1毫秒转换为1000微秒 
     
    1分钟转换为60秒 
     
    1小时转换为3600秒 
     
    1周转换为7天 

其中，timedelta内部只存储 days,seconds,microseconds

常用的类方法与属性：

| 属性或类方法       | 概述                              |
| ------------------ | --------------------------------- |
| td.days            | 天（范围[-999999999，999999999]） |
| td.seconds         | 秒（范围[0,86399]）               |
| td.microseconds    | 微秒（范围[0,999999]）            |
| td.total_seconds() | 以秒为单位返回该时间差            |

实例：

```c
m = datetime.datetime.now()

print(m)

l = m + datetime.timedelta(3)

print(l)

n = m + datetime.timedelta(hours=4)

print(n)

span = l-m

print(span)

print(span.total_seconds())
```

### 5. tzinfo 类

其中，tzinfo是一个抽象类，所以不能直接被实例化 

时间转换需要用datetime和pytz来转换时区

## 5.5 time 模块

在Python中，通常有这几种方式来表示时间：

​			1）时间戳 

​			2）格式化的时间字符串 

​			3）元组（struct_time）共九个元素。由于Python的time模块实现主要调用C库，所以各个平台可能有所不同。

**UTC（Coordinated Universal Time，世界协调时）：**即格林威治天文时间，世界标准时间。在中国为UTC+8。DST（Daylight Saving Time）即夏令时。

**时间戳（timestamp）：**通常来说，时间戳表示的是从**1970年1月1日00:00:00**开始按秒计算的偏移量。我们运行“type(time.time())”，返回的是float类型。返回时间戳方式的函数主要有time()，clock()等。

**元组（struct_time）：**struct_time元组共有9个元素，返回struct_time的函数主要有gmtime()，localtime()，strptime()。

| 索引（Index） | 属性（Attribute）         | 值（Values）       |
| ------------- | ------------------------- | ------------------ |
| 0             | tm_year（年）             | 比如2011           |
| 1             | tm_mon（月）              | 1 - 12             |
| 2             | tm_mday（日）             | 1 - 31             |
| 3             | tm_hour（时）             | 0 - 23             |
| 4             | tm_min（分）              | 0 - 59             |
| 5             | tm_sec（秒）              | 0 - 59             |
| 6             | tm_wday（weekday）        | 0 - 6（0表示周日） |
| 7             | tm_yday（一年中的第几天） | 1 - 366            |
| 8             | tm_isdst（是否是夏令时）  | 默认为-1           |

**1. time.localtime([secs])**

将一个时间戳转换为当前时区的struct_time。secs参数未提供，则以当前时间为准。

```
import time
print(time.localtime())
print(time.localtime(time.time()+36000))

time.struct_time(tm_year=2021, tm_mon=5, tm_mday=19, tm_hour=9, tm_min=11, tm_sec=38, tm_wday=2, tm_yday=139, tm_isdst=0)
time.struct_time(tm_year=2021, tm_mon=5, tm_mday=19, tm_hour=19, tm_min=15, tm_sec=43, tm_wday=2, tm_yday=139, tm_isdst=0)
```

**2. time.gmtime([secs])**

和localtime()方法类似，gmtime()方法是将一个时间戳转换为UTC时区（0时区）的struct_time。

```c
print(time.gmtime())

time.struct_time(tm_year=2021, tm_mon=5, tm_mday=19, tm_hour=1, tm_min=13, tm_sec=52, tm_wday=2, tm_yday=139, tm_isdst=0)
```

**3. time.time()**

返回当前时间的时间戳

```c
print(time.time())
print(time.time()+3600)    
    
1621387048.8600447
1621390648.8600447
```

**4. time.mktime(t)**

将一个struct_time转化为时间戳。

```c
print(time.mktime(time.localtime()))
    
1621387237.0
```

**5. time.sleep([secs])**

线程推迟指定的时间运行。单位为秒。

```c
time.sleep(0.5)
```

**6. time.clock()**

这个需要注意，在不同的系统上**含义不同**。在UNIX系统上，它返回的是“进程时间”，它是用秒表示的浮点数（时间戳）。而在WINDOWS中，第一次调用，返回的是进程运行的实际时间。而第二次之后的调用是自第一次调用以后到现在的运行时间。（实际上是以WIN32上QueryPerformanceCounter()为基础，它比毫秒表示更为精确）

```c
import time

if __name__ == '__main__':
    time.sleep(1)
    print("clock1:%s" % time.clock())
    time.sleep(1)
    print("clock2:%s" % time.clock())
    time.sleep(1)
    print("clock3:%s" % time.clock())
        
linux:
	clock1:0.0
    clock2:0.0
    clock3:0.0
        
windows:
	clock1:6e-07
    clock2:1.0001054
    clock3:2.0003185
        
    第一个clock()输出的是程序运行时间
	第二、三个clock()输出的都是与第一个clock的时间间隔
```

**7. time.asctime(t)**

把一个表示时间的元组或者struct_time表示为这种形式：**'Sun Jun 20 23:21:05 1993'**。如果没有参数，将会将time.localtime()作为参数传入。

```c
print(time.asctime())
    
Wed May 19 09:29:50 2021
```

**8. time.ctime([secs])**

把一个时间戳（按秒计算的浮点数）转化为time.asctime()的形式。如果参数未给或者为None的时候，将会默认time.time()为参数。它的作用相当于time.asctime(time.localtime(secs))。

```c
print(time.ctime())
    
Wed May 19 09:32:10 2021
```

**9. time.strftime(format[, t])**

把一个代表时间的元组或者struct_time（如由time.localtime()和time.gmtime()返回）转化为格式化的时间字符串。如果t未指定，将传入time.localtime()。如果元组中任何一个元素越界，ValueError的错误将会被抛出。

| 格式 | 含义                                                         |
| ---- | ------------------------------------------------------------ |
| %a   | 本地（locale）简化星期名称                                   |
| %A   | 本地完整星期名称                                             |
| %b   | 本地简化月份名称                                             |
| %B   | 本地完整月份名称                                             |
| %c   | 本地相应的日期和时间表示                                     |
| %d   | 一个月中的第几天（01 - 31）                                  |
| %H   | 一天中的第几个小时（24小时制，00 - 23）                      |
| %I   | 第几个小时（12小时制，01 - 12）                              |
| %j   | 一年中的第几天（001 - 366）                                  |
| %m   | 月份（01 - 12）                                              |
| %M   | 分钟数（00 - 59）                                            |
| %p   | 本地am或者pm的相应符                                         |
| %S   | 秒（01 - 61）                                                |
| %U   | 一年中的星期数。（00 - 53星期天是一个星期的开始。）第一个星期天之前的所有天数都放在第0周。 |
| %w   | 一个星期中的第几天（0 - 6，0是星期天）                       |
| %W   | 和%U基本相同，不同的是%W以星期一为一个星期的开始。           |
| %x   | 本地相应日期                                                 |
| %X   | 本地相应时间，同 %H:%M:%S                                    |
| %y   | 去掉世纪的年份（00 - 99）                                    |
| %Y   | 完整的年份                                                   |
| %Z   | 时区的名字（如果不存在为空字符）                             |
| %%   | ‘%’字符                                                      |

 **备注**：

1.  "%p" 只有与 "%I" 配合使用才有效果。
2.  文档中强调确实是0 - 61，而不是59，闰年秒占两秒。
3.  当使用strptime()函数时，只有当在这年中的周数和天数被确定的时候%U和%W才会被计算。

```c
ISOTIMEFORMAT = '%Y-%m-%d %X'
print(time.strftime(ISOTIMEFORMAT, time.localtime()))
    
2021-05-19 09:41:43
```

**10. time.strptime(string[, format])**

把一个格式化时间字符串转化为struct_time。实际上它和strftime()是逆操作。

```c
print(time.strptime('2021-05-19 09:41:43','%Y-%m-%d %X'))
    
time.struct_time(tm_year=2021, tm_mon=5, tm_mday=19, tm_hour=9, tm_min=41, tm_sec=43, tm_wday=2, tm_yday=139, tm_isdst=-1)
```

## 5.6 re 模块

在Python中需要通过正则表达式对字符串进⾏匹配的时候，可以使⽤⼀个python自带的模块，名字为re。

r：在带有 `'r'` 前缀的字符串字面值中，反斜杠不必做任何特殊处理。 因此 `r"\n"` 表示包含 `'\'` 和 `'n'` 两个字符的字符串，而 `"\n"` 则表示只包含一个换行符的字符串。

re.match只匹配字符串的开始，如果字符串开始不符合正则表达式，则匹配失败

**1. re.match**

**re.match(pattern, string, flags=0)**

| 参数    | 解释                                                         |
| ------- | ------------------------------------------------------------ |
| pattern | 匹配的正则表达式                                             |
| string  | 要匹配的字符串                                               |
| flags   | 标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等。                                                                                                   I 忽略大小写                                                                                                                                                                                                L 表示特殊字符集 \w, \W, \b, \B, \s, \S 依赖于当前环境                                                                                                                          M 多行模式                                                                                                                                                                                                   S 即为 . 并且包括换行符在内的任意字符（. 不包括换行符）                                                                                                                      U 表示特殊字符集 \w, \W, \b, \B, \d, \D, \s, \S 依赖于 Unicode 字符属性数据库                                                                                  X 为了增加可读性，忽略空格和 # 后面的注释 |

**匹配单个字符：**

| 字符 | 功能                             | 位置                  |
| ---- | -------------------------------- | --------------------- |
| .    | 匹配任意1个字符（除了\n）        |                       |
| [ ]  | 匹配[ ]中列举的字符              |                       |
| \d   | 匹配数字，即0-9                  | 可以写在字符集[...]中 |
| \D   | 匹配⾮数字，即不是数字           | 可以写在字符集[...]中 |
| \s   | 匹配空⽩，即空格，tab键          | 可以写在字符集[...]中 |
| \S   | 匹配⾮空⽩字符                   | 可以写在字符集[...]中 |
| \w   | 匹配单词字符，即a-z、A-Z、0-9、_ | 可以写在字符集[...]中 |
| \W   | 匹配⾮单词字符                   | 可以写在字符集[...]中 |

**实例：**

```c
ret = re.match(".","sdvMasd")
print(ret.group())
ret = re.match("t.o","toooosssdq")
print(ret.group())
ret = re.match("t.o","twoacxzxc")
print(ret.group())
# 如果hello的⾸字符⼩写，那么正则表达式需要⼩写的h
ret = re.match("h","hello Python")
print(ret.group())
# 如果hello的⾸字符⼤写，那么正则表达式需要⼤写的H
ret = re.match("H","Hello Python")
print(ret.group())
# ⼤⼩写h都可以的情况
ret = re.match("[hH]","hello Python")
print(ret.group())
ret = re.match("[hH]","Hello Python")
print(ret.group())
ret = re.match("[hH]ello Python","Hello Python")
print(ret.group())
# 匹配0到9的多种写法
ret = re.match("[0123456789]Hello Python","7Hello Python")
print(ret.group())
ret = re.match("[0-9]Hello Python","7Hello Python")
print(ret.group())
# 匹配0到3和5-9
ret = re.match("[0-35-9]Hello Python","7Hello Python")
print(ret.group())
ret = re.match("嫦娥\d号","嫦娥1号发射成功")
print(ret.group())
ret = re.match("嫦娥\d号","嫦娥2号发射成功")
print(ret.group())
```

**匹配多个字符：**

| 字符  | 功能                                                         | 位置                | 表达式实例 | 完整匹配的字符串 |
| ----- | ------------------------------------------------------------ | ------------------- | ---------- | ---------------- |
| *     | 匹配前⼀个字符出现0次或者⽆限次，即可有可⽆                  | 用在字符或(...)之后 |            |                  |
| +     | 匹配前⼀个字符出现1次或者⽆限次，即⾄少有1次                 |                     |            |                  |
| ?     | 匹配前⼀个字符出现1次或者0次，即要么有1次，要么没有          |                     |            |                  |
| {m}   | 匹配前⼀个字符出现m次                                        |                     |            |                  |
| {m,n} | 匹配前⼀个字符出现从m到n次，若省略m，则匹配0到n次，若省略n，则匹配m到无限次 |                     |            |                  |

**实例：**

```c
#：匹配出，⼀个字符串第⼀个字⺟为⼤写字符，后⾯都是⼩写字⺟并且这些⼩写字⺟可有可⽆
ret = re.match("[A-Z][a-z]*","M")
print(ret.group())
ret = re.match("[A-Z][a-z]*","MnnM")
print(ret.group())
ret = re.match("[A-Z][a-z]*","Aabcdef")
print(ret.group())
#匹配出，变量名是否有效
names = ["name1", "_name", "2_name", "__name__"]
for name in names:
    ret = re.match("[a-zA-Z_]+[\w]*",name)
    if ret:
        print("变量名 %s 符合要求" % ret.group())
    else:
        print("变量名 %s ⾮法" % name)
#匹配出，0到99之间的数字
ret = re.match("[1-9]?[0-9]","7")
print(ret.group())
ret = re.match("[1-9]?\d","33")
print(ret.group())
# 这个结果并不是想要的，利⽤$才能解决
ret = re.match("[1-9]?\d","09")
print(ret.group())
ret = re.match("[a-zA-Z0-9_]{6}","12a3g45678")
print(ret.group())
#匹配出，8到20位的密码，可以是⼤⼩写英⽂字⺟、数字、下划线
ret = re.match("[a-zA-Z0-9_]{8,20}","1ad12f23s34455ff66")
print(ret.group())
```

**匹配开头结尾：**

| 字符 | 功能           |
| ---- | -------------- |
| ^    | 匹配字符串开头 |
| $    | 匹配字符串结尾 |

**实例：**

```
import re
email_list = ["xiaoWang@163.com", "xiaoWang@163.comheihei", ".com.xiaowang@qq.com"]
for email in email_list:
    ret = re.match("[\w]{4,20}@163\.com$", email)
    if ret:
        print("%s 是符合规定的邮件地址,匹配后的结果是:%s" % (email, ret.group()))
    else:
        print("%s 不符合要求" % email)
```

**匹配分组：**

| 字符       | 功能                                                         |
| ---------- | ------------------------------------------------------------ |
| \|         | 匹配左右任意⼀个表达式                                       |
| (ab)       | 将括号中字符作为⼀个分组                                     |
| \num       | 引⽤分组num匹配到的字符串                                    |
| (?P<name>) | 分组起别名，匹配到的子串组在外部是通过定义的 *name* 来获取的 |
| (?P=name)  | 引⽤别名为name分组匹配到的字符串                             |

**2. re.compile 函数**

compile 函数用于编译正则表达式，生成一个正则表达式（ Pattern ）对象，供 match() 和 search() 这两个函数使用。

```c
prog = re.compile(pattern)
result = prog.match(string)
    
等价于
    
result = re.match(pattern, string)
    
    
>>> pattern = re.compile(r'\d+')   
m = pattern.match('one12twothree34four', 3, 10) # 从'1'的位置开始匹配，正好匹配
>>> print m                                         # 返回一个 Match 对象
<_sre.SRE_Match object at 0x10a42aac0>
>>> m.group(0)   # 可省略 0
'12'
>>> m.start(0)   # 可省略 0
3
>>> m.end(0)     # 可省略 0
5
>>> m.span(0)    # 可省略 0
(3, 5)
```

在上面，当匹配成功时返回一个 Match 对象，其中：

    group([group1, …]) 方法用于获得一个或多个分组匹配的字符串，当要获得整个匹配的子串时，可直接使用 group() 或 group(0)；
    start([group]) 方法用于获取分组匹配的子串在整个字符串中的起始位置（子串第一个字符的索引），参数默认值为 0；
    end([group]) 方法用于获取分组匹配的子串在整个字符串中的结束位置（子串最后一个字符的索引+1），参数默认值为 0；
    span([group]) 方法返回 (start(group), end(group))
**3. re.search**

re.search 扫描整个字符串并返回第一个成功的匹配，如果没有匹配，就返回一个 None。

re.match与re.search的区别：re.match只匹配字符串的开始，如果字符串开始不符合正则表达式，则匹配失败，函数返回None；而re.search匹配整个字符串，直到找到一个匹配

```c
ret = re.search(r"\d+", "阅读次数为9999")
print(ret.group())
```

**4. re.findall**

在字符串中找到正则表达式所匹配的所有子串，并返回一个列表，如果没有找到匹配的，则返回空列表。注意**：** match 和 search 是匹配一次 findall 匹配所有。

```c
ret = re.findall(r"\d+", "python = 9999, c = 7890, c++ = 12345")
print(ret)
    
['9999', '7890', '12345']
```

**5. re.finditer**

和 findall 类似，在字符串中找到正则表达式所匹配的所有子串，并把它们作为一个迭代器返回。

```c
it = re.finditer(r"\d+", "12a32bc43jf3")
for match in it:
    print(match.group())
```

**6. re.sub**

sub是substitute的所写，表示替换，将匹配到的数据进⾏替换。

语法：

**re.sub(pattern, repl, string, count=0, flags=0)**

| 参数    | 描述                                                         |
| ------- | ------------------------------------------------------------ |
| pattern | 必选，表示正则中的模式字符串                                 |
| repl    | 必选，就是replacement，要替换的字符串，也可为一个函数        |
| string  | 必选，被替换的那个string字符串                               |
| count   | 可选参数，*count* 是要替换的最大次数，必须是非负整数。如果省略这个参数或设为 0，所有的匹配都会被替换 |
| flag    | 可选参数，标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等。 |

**实例：**

```c
举例：将匹配到的阅读次数加1 

def add(temp):
        #int（）参数必须是字符串，类似字节的对象或数字，而不是“re.Match”
        strNum = temp.group()
        num = int(strNum) + 1
        return str(num)
    ret = re.sub(r"\d+", add, "python = 997")
    print(ret)
    ret = re.sub(r"\d+", add, "python = 99")
    print(ret)
```

**7. re.split**

根据匹配进⾏切割字符串，并返回⼀个列表。

**re.split(pattern, string, maxsplit=0, flags=0)**

| 参数     | 描述                                                |
| -------- | --------------------------------------------------- |
| pattern  | 匹配的正则表达式                                    |
| string   | 要匹配的字符串                                      |
| maxsplit | 分隔次数，maxsplit=1 分隔一次，默认为 0，不限制次数 |

```c
ret = re.split(r":| ","info:xiaoZhang 33 shandong")
print(ret)
    
['info', 'xiaoZhang', '33', 'shandong']
```

## 5.7 json模块

Python是原生态支持json，这点可以从字典和列表结构看出来。

我们可以利用json模块处理json数据。

**1.json.dumps() 与 json.loads()**

dumps：把字典转成json字符串

loads：把json字符串转成字典

```c
import json

tdict={"name":"liu","age":15,"sex":"M"}
// 将字典转换为json字符串
json_txt = json.dumps(tdict)
print(json_txt)
print(type(json_txt))
# print(json_txt["name"])
    
<class 'str'>
{"name": "liu", "age": 15, "sex": "M"}

tjson = """
{
    "name":"liu",
    "age":"15",
    "sex":"M"
}
"""
// 将 json字符串转换为字典
json_dict = json.loads(tjson)
print(type(json_dict))
print(json_dict)
print(json_dict["name"])
    
<class 'dict'>    
{'name': 'liu', 'age': '15', 'sex': 'M'}
liu
```

最后，再说一个知识点。**如何把json转成有序的字典**。

众所周知，字典是无序的。所以json的loads方法转换得来的字典本来就是无序的。

但出于某种需求，需要确保顺序正常，按照原本json字符串的顺序。

这个需要在解析的时候，把无序字典换成有序字典。如下代码：

```c
from collections import OrderedDict
import json
 
json_text = '{ "b": 3, "a": 2, "c": 1}'
 
json_dict = json.loads(json_text)
print(u"转成普通字典")
for key, value in json_dict.items():
    print("key:%s, value:%s" % (key, value))
    
json_dict = json.loads(json_text, object_pairs_hook=OrderedDict)
print(u"\n转成有序字典")
for key, value in json_dict.items():
    print("key:%s, value:%s" % (key, value))
        
转成普通字典
key:b, value:3
key:a, value:2
key:c, value:1

转成有序字典
key:b, value:3
key:a, value:2
key:c, value:1    
```

**2.json.dump() 与 json.load()**

dump把字典转成json字符串并写入到文件

load从json文件读取json字符串到字典

```c
import json
import codecs

test_dict = {'a':1, 'b':2}
 
#把字典转成json字符串并写入到文件 1.json 中
with codecs.open('1.json', 'w', 'utf-8') as f:
    json.dump(test_dict, f)
        
#从json文件读取json字符串到字典
with codecs.open('1.json', 'r', 'utf-8') as f:
    json_dict = json.load(f)
```

## 5.8 ipaddress 模块

**1.ip_address**

ipaddress.ip_address() 工厂函数用于创建ip_address对象。它会根据传入的值自动确定是创建IPv4还是IPv6地址

```c
import ipaddress
# 点分十进制
IP = ipaddress.ip_address('192.168.100.100')
print(IP)
192.168.100.100 
    
print(IP.version)      # 打印IP版本号
print(str(IP))         # 转换为字符串
print(int(IP))         # 转换为十进制
print(hex(int(IP)))    # 转换为十六进制
print(bin(int(IP)))    # 转换为二进制
print(oct(int(IP)))    # 转换为八进制
print(IP.packed)       # 转换为字节    
    
4
192.168.100.100
3232261220
0xc0a86464
0b11000000101010000110010001100100
0o30052062144
b'\xc0\xa8dd'
    

# 二进制，前面需加上0b
IP = ipaddress.ip_address(0b11000000101010000110010001100100)
print(IP)
192.168.100.100

# 十六进制，前面需加上0x
IP = ipaddress.ip_address(0xC0A86464)
print(IP)
192.168.100.100
   
# 生成IPv6地址
IP6 = ipaddress.ip_address('2001:DB8::1')
print(IP6)
2001:DB8::1
    
IP6 = ipaddress.ip_address(42540766411282592856903984951653826561)
print(IP6)
2001:DB8::1
```

**2.ip_network()**

创建网络——使用格式为：ipaddress.ip_network('网络地址/掩码位数')

```c
# 创建网络对象，通过list转换为列表
a=list(ipaddress.ip_network('192.168.1.0/24'))
print(a[15:25])
    
# 设置strict=False实现附加位强制为0    
ipaddress.ip_network('192.168.1.1/24',strict=False)
# 查看网络内有多少可用地址
print(NT.num_addresses)

192.168.1.0/24
256
    
# 打印出所有IP    
for IP in NT.hosts():
    print(IP)

# 打印出掩码        
print(NT.netmask)
      
# 排除部分地址        
NT2=ipaddress.ip_network('192.168.1.0/26')
list(NT.address_exclude(NT2))
 
[IPv4Network('192.168.1.128/25'), IPv4Network('192.168.1.64/26')]

# 拆分网络段
list(NT.subnets(new_prefix=25))
        
```

**3.ip_interface()**

## 5.9 importlib 模块

**1.import_module()** 

在需要的时候动态导入模块

```c
import importlib

importlib.import_module('cmdb.type.IP')
importlib.import_module('cmdb.type')
```

# 6.Django框架

## 6.1 安装

 **下载安装：**

```c
pip3 install django==2.2.29
```

**手动创建项目:**

```c
django-admin startproject mydjango   # 项目名
```



![](./picture/1.jpg)

```c
外层的mysite/目录与Django无关，只是你项目的容器，可以任意重命名。
manage.py：一个命令行工具，用于与Django进行不同方式的交互脚本，非常重要！
内层的mysite/目录是真正的项目文件包裹目录，它的名字是你引用内部文件的包名，例如：mysite.urls。
mysite/__init__.py:一个定义包的空文件。
mysite/settings.py:项目的主配置文件，非常重要！
mysite/urls.py:路由文件，所有的任务都是从这里开始分配，相当于Django驱动站点的内容表格，非常重要！
mysite/wsgi.py:一个基于WSGI的web服务器进入点，提供底层的网络通信功能，通常不用关心。
```

**settings.py：**

```c
ALLOWED_HOSTS = []			# 允许机器访问，白名单

LANGUAGE_CODE = 'zh-hans'	# 默认界面语言，可选语言
TIME_ZONE = 'Asia/Shanghai'		# 时区
USE_TZ = False		#USE_TZ默认为True，因为Mysql存储的时间不能灵活设置时区，不像datetime对象有一项参数专门指定时区，所以为了统一全球的时间，必须使用国际标准时间UTC，否则就会乱套。所以时间在存入数据库前，必须转换成UTC时间。比如北京时间8点，存入mysql变成0点（UTC）。
```

**运行项目:**

```c
python manage.py runserver 127.0.0.1 8000
```

**添加应用:**

```c
# 在Django项目(my_project)的根目录下执行
python3 manage.py startapp my_app
```



## 6.2 视图 views

### 1. request对象

**1.常用的属性和方法**

```c
request.path	#请求路径
request.GET		#获取url中的查询参数
request.POST	#获取请求提交的数据
request.GET.get('name')	# 根据键值获取数据
request.POST.get()	
request.method	# 请求方法
request.data
request.META	#请求头信息
request.body	#获取http请求消息格式的请求数据部分的内容
```

### 2. response对象

**1.常用的属性和方法**

**2.添加响应头键值对**

```c
ret = render(request, "home.html", context={"Title": 'mydjango', "name": "liuzichuan"})
ret['a'] = 'b'
```

**3.添加响应状态码**

```c
# ret = render(request, "home.html", context={"Title": 'mydjango', "name": "liuzichuan"},status=202)
ret.status_code = 202
```

### 3. CBV和FBV

CBV：class based view ，就是基于类来写视图

FBV：class based view，就是基于函数来写视图

**1.给FBV添加装饰器**

```c
"""
    添加装饰器
"""
def outer(f,*args,**kwargs):

    def func(request,*args,**kwargs):
        print("装饰前")
        ret = f(request, *args,**kwargs)
        print("装饰后")
        return ret
    return func
            
# FBV添加装饰器
@outer
def book(request,year,month):
    print("FBV添加装饰器")
    return HttpResponse("book is {} year, {} month".format(year,month))
```

**2.给CBV添加装饰器**

```c
# CBV添加装饰器
# 2.给指定的方法添加装饰器
@method_decorator(outer,name='get')
class book(View):

    # 1.只是给单独的方法加装饰器
    @method_decorator(outer)
    def get(self,request,year,month):
        print("CBV添加装饰器，get方法")
        return render(request, 'book.html')
        #return HttpResponse("book is {} year, {} month".format(year,month))

    def post(self,request,year,month):
        print("CBV post方法")
        #return render(request, 'book.html')
        return HttpResponse("post ok...")
            
	#3.重写View父类中的dispatch方法，会给类中所有方法添加装饰器
    @method_decorator(outer)
    def dispatch(self,request,*args,**kwargs):
		print("装饰前")
        ret = super().dispatch(request, *args,**kwargs)
        print("装饰后")
        return ret
```

### 4.url反向解析

由于将来项目中的不同功能对应的url有可能会发生变化，所以我们在每个url上加上别名，将来通过反向url解析来使用这个对应的路径，所以只要别名不变，应用的url随便变化都能获取

**views使用url反向解析的方式：**

```c
url中配置name属性(别名)：
url('^add_book/', views.add_book,name='add_book')
    
views中使用：
from django.urls from reverse		
# 未使用正则    
redirect(reverse('add_book'))
# 使用无名分组
redirect(reverse('add_book',args=()))
# 使用有名分组
redirect(reverse('add_book',kwargs={})
```



## 6.3 模板 template

模板渲染：模板指的就是html文件，渲染指的就是字符串替换，将模板中的特殊符号替换成相关数据

模板渲染是在浏览器渲染之前，模板渲染完成后，才交给浏览器渲染，展示

**1.python模板语法:**

```c
{{ 变量 }}
{% 语句块 %}

info = {
    'name':'lzc',
    'age':25,
    'hobby':['洗脚','烫头','大保健'],
    'sex':{'xx':'oo','hello':'world'},
    'a':A()
}
ret = render(request,"home.html",info)
    
在html中调用时
    <p>
        {{ age }}
    </p>
    # 调用字段可以直接.key调用
    <p>
        {{ sex.hello }}
    </p>
    # 调用列表可直接通过列表下标调用
    <p>
    	{{ hobby.0 }}
    </p>
    <--!>调用属性或者方法，调用方法不需要加括号，不能传参<-->
    <p>
        {{ a.aaa }}
        {{ a.say }}
    </p>    
```

**2.过滤器：**

过滤器就是在对应参数没有数据时，设置一些默认值

**语法：{{ value|filter_name:参数 }}**

1.过滤器支持链式操作，即一个过滤器的输出可以作为另一个过滤器的输入{{ sss|过滤器1|过滤器2 }}

2.过滤器可以接受参数，如{{ sss|truncatewords:30 }}，这将显示sss的前30个词

3.过滤器包含空格的话，必须用"" '' 引起来

4.'|'两边没有空格

示例：都是系统自带的过滤器

```c
{{ name|default:"zhangsan" }}
{{ sss|truncatewords:30 }}
{{ name|length }}		#长度
{{ msg|slice:'0:2' }}	#切片
{{ now|date:"Y-m-d H:i:s" }}	#时间格式化
```

**3.标签**

​	**for标签：**

```c
<ul>
	{% for i in hobby %}
		<li>{{ i }}</li>
	{% endfor %}
</ul>

<ul>
    # 反序
	{% for i in hobby reversed %}
		<li>{{ i }}</li>
	{% endfor %}
</ul>
    
# 字典与python一样,d.values就是循环值，d.items就是key和值
# 循环还可以使用{{ forloop }} 来显示循环计数，必须循环内使用，具体查看官网    

```

​	**for..empty标签：**

当未查询到数据时，使用empty返回定义信息

```c
<ul>
	{% for i in hobby %}
		<li>{{ i }}</li>
    {% empty %}
		<h2>抱歉，没有查询到相关数据</h2>
	{% endfor %}
</ul>
```

​	**if标签：**

```c
{% if status > 1 %}
	<a href="">京东</li>
{% elif status == 1 %}
	<a href="">百度</li>
{% else %}
	<a href="">taobao</li>
{% endif %}

# 与python判断方式一致
```

​	**with标签：**

```c
# 取个别名，只能在with里面使用
{% with aaaaaa as a %}
	<li>{{ a }}</li>
{% endwith %}
```

**4.自定义标签和过滤器**

**5.模板继承**

当模板需要重复使用时，为了减少冗余代码，可以直接引继承模板

```c
1. 在新创建的模板文件中,就可以引用模板文件全部代码
{% extend 'tmp.html' %}

2. 需要修改模板文件html/css代码，需要在模板文件中预留快
# 模板文件中预留快
{% block content %}
...
{% endblock %}

# 继承模板文件中进行对应修改即可
{% block content %}
	...
	<--!  若想保留模板中的值，可以使用block.super -->
    {{ block.super }}
{% endblock %}

```

**6.静态文件配置**

一般会将css,js,img等静态文件，放在一个文件夹下，引用时需指明路径

```
1.<link rel="stylesheet" href="/abc/css/x.css">		#直接使用静态文件夹路径别名
2.在html文件中 {% load static %}
	使用: <link rel="stylesheet" href="{% static 'css/x.css' %}">
3.在html文件中 {% load static %}
	使用: <link rel="stylesheet" href="{% get_static_prefix %}css/xx.css">
        
        
注：settings会有两个配置项，一个指定静态文件目录，一个指定静态文件别名，html文件中都是使用静态文件别名
STATIC_URL  = '/abc/' #静态文件夹别名
STATICFILES_DIRS = [
        os.path.join(BASE_DIR,'staticdir')
]	 #静态文件夹路径
```

**7.组件**

就是一些写好的html，css等模板文件，可以直接在html中引用

```c
{% include '组件文件名称'.html %}
```



## 6.4 ORM 对象关系映射

### 1.连接数据库

**object relational mapping**

类对象-->sql-->pymysql-->mysql服务端-->磁盘

**1.创建表：**

在models.py文件中：

```c
class book(models.Model):

    id = models.AutoField(primary_key=True) #自增，主键
    title = models.CharField(max_length=64,null=True)
    state = models.BooleanField()
        
        
对应的sql：
create table book (
	id int primary key auto_inrcement;
    title varchar(64);
    state boolean not null;
)
```

**2.同步到数据库**

```c
python manage.py makemigrations		#生成迁移文件
python manage.py migrate		#执行对应的迁移文件
```

**3.连接自定义数据库**

**配置连接mysql：**

```c
1.在mysql中创建一个库
> create database orm01 character set utf8mb4; 

2.修改settings配置文件
# 配置都是固定写法，切必须大写
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'orm01',
        'HOST': '192.168.183.132',
        'PORT': 3306,
        'USER': 'chuan',
        'PASSWORD': 'chuan'
    }
}

3.指定Django连接mysql的python模块
	a.下载pymysql

    b.指定连接模块，需要在项目主目录下的__init__.py文件中指定
    
    	import pymysql
		pymysql.install_as_MySQLdb()   
```

**4.执行数据库同步指令**

```c
python manage.py makemigrations		#生成迁移文件,会将变动更新为一个文件
python manage.py migrate		#执行对应的迁移文件
```

### 2.model类的属性参数

```c
1. null
如果为True，Django将使用NULL来站在数据库中存储空值。默认是False
    
2. blank
如果为True，该字段允许不填。默认为False
    
3. default
字段的默认值。可以是一个值或者可调用对象。如果可调用，每次新对象被创建它都会被调用，如果你的字段没有设置可以为空，那么将来如果我们后添加一个字段，这个字段就要给一个default值
    
4. primary_key
如果为True，这个字段就是模型的主键。如果你没有指定任何一个字段的primary_key=True，Django就会自动添加一个IntegerField字段作为主键，所以除非你想覆盖默认的主键行为，否则没有必要设置任何一个字段的primary_key=true
    
5. unique
如果该值设置为true，这个数据字段的值在整张表中必须是唯一的，唯一键
    
6. choices
由二元组组成的一个可迭代对象(例如列表或元组)，用来给字段提供选择项。如果设置了choices，默认的表单将是一个选择框而不是标准的文本框，<br>而且这个选择框的选项就是choices中的选项
    
7. db_index
如果db_index=True，则表示此字段设置为数据库索引
    
DatetimeField、DateField、TimeField这三个时间字段，都可以设置如下属性
    
8.auto_now_add
配置auto_now_add=True，创建数据记录的时候会把当前时间添加到数据库
    
9. auto_now
配置上auto_now=True，每次更新数据记录的时候会更新该字段，标识这条记录最后一次的修改时间
    
```

**ORM字段与数据库实际字段的对应关系:**

可以在db下mysql包里的base文件里面查看

```c
'AutoField': 'integer AUTO_INCREMENT',
'BigAutoField': 'bigint AUTO_INCREMENT',
'BinaryField': 'longblob',
'BooleanField': 'bool',
'CharField': 'varchar(%(max_length)s)',
'CommaSeparatedIntegerField': 'varchar(%(max_length)s)',
'DateField': 'date',
'DateTimeField': 'datetime',
'DecimalField': 'numeric(%(max_digits)s, %(decimal_places)s)',
'DurationField': 'bigint',
'FileField': 'varchar(%(max_length)s)',
'FilePathField': 'varchar(%(max_length)s)',
'FloatField': 'double precision',
'IntegerField': 'integer',
'BigIntegerField': 'bigint',
'IPAddressField': 'char(15)',
'GenericIPAddressField': 'char(39)',
'NullBooleanField': 'bool',
'OneToOneField': 'integer',
'PositiveIntegerField': 'integer UNSIGNED',
'PositiveSmallIntegerField': 'smallint UNSIGNED',
'SlugField': 'varchar(%(max_length)s)',
'SmallIntegerField': 'smallint',
'TextField': 'longtext',
'TimeField': 'time',
'UUIDField': 'char(32)',
```

### 3.ORM增删改查

**1.插入数据**

**插入单条数据：**

```c
def add_book(request):

    # 插入数据方式一
    book_obj = apps.models.book(title="鲁滨孙漂流记",state=True,price=55)
    
    print(book_obj)
    print(book_obj.title)     
    book_obj.save()

    # 插入数据方式二
    book_obj = apps.models.book.objects.create(title="斗破苍穹",state=True,price=66)

    book_obj.save()

    print(book_obj)
    print(book_obj.title)
        
    return HttpResponse('add_book2 is ok')
```

**批量插入数据：**

```c
def add_book(request):
	
    book_lst = []
    for i in range(1,10):
        obj = apps.models.book(title="水浒传{}".format(i),state=True,price=i*i)

        book_lst.append(obj)

    apps.models.book.objects.bulk_create(book_lst)

    return HttpResponse("add_book3 is ok")
```

**2.删除数据**

```c
def delete_book(request):

    # 方式一，根据查询结果对象来更新，只能删除一条记录
    # obj = apps.models.book.objects.get(id=5).delete()

    # 方式二
    # obj = apps.models.book.objects.filter(id=5).delete()
    # 删除所有数据
    obj = apps.models.book.objects.all().delete()

    print(obj)


    return HttpResponse("delete_book is ok")
```



**3.修改数据**

```
def update_book(request):

    # 方式一，根据查询结果对象来更新
    # obj = apps.models.book.objects.get(id=5)
    # obj.state = False
    # obj.save()
    #
    # return HttpResponse("update_book is ok")

    # 方式二，根据条件更新
    # 全量
    apps.models.book.objects.update(
        state = False
    )
	
    # apps.models.book.objects.all().update(
    #     state=False
    # )

	# 根据条件过滤
    # apps.models.book.objects.filter(id=5).update(
    #     state=False
    # )

    # return HttpResponse("update_book2 is ok")

	# 方式三，查询到就更新，没有就创建，内部调用get方法，查询记录只能一条
    obj = apps.models.book.objects.update_or_create(
        id=20,
        defaults={
            "title":"西游记",
            "state":False,
            "price":22
        }
    )

    # 方式四，查询到就返回查询结果，查询不到就添加记录,内部调用get方法，查询记录只能一条
    obj = apps.models.book.objects.get_or_create(
        id=20,
        defaults={
            "title": "西游记",
            "state": False,
            "price": 22
        }
    )

```



**4.查询数据**

```python
def get_book(request):
    # print(obj_lst[0])
    # return HttpResponse("get_book1 all is ok")

    # 查询所有数据
    # obj_lst = apps.models.book.objects.all()
    # print(obj_lst)
    # return render(request, "get_book.html", {"obj_lst": obj_lst})

    # where id=5;
    # obj = apps.models.book.objects.filter(id=5)
    # print(obj)
    # return render(request, "get_book.html", {"obj_lst": obj})

    # filter 与 get 的区别在于：
    #   1. get返回的是一个对象，且查询的结果只能是一个，不可迭代
    #   2. get查看不到结果会报错，filter为空
    obj = apps.models.book.objects.get(id=5)
    print(obj)
    return render(request, "get_book.html", {"obj_lst": obj})

```

**查询的多个API接口:**

```c
def all(self)
    # 获取所有的数据对象

def filter(self, *args, **kwargs)
    # 条件查询
    # 条件可以是：参数，字典，Q
    apps.models.book.objects.filter(title='linux',price=50)    # select * from table where title='linux' and price=50
	apps.models.book.objects.filter(**{title='linux',price=50})
    
def order_by(self,*fields)
    # 默认按照参数升序排序，降序参数直接加上一个 - 就行 ，如果没有参数，默认使用id进行排序
    obj = apps.models.book.objects.order_by("price")	# select * from table order_by price;
    obj = apps.models.book.objects.order_by("-price")	# select * from table order_by price desc;

    models.UserInfo.objects.all().order_by('-id','age')  # 当有两个参数时，以第一个参数为准，当第一参数值相同时使用第二个参数 
    
    
def exclude(self, *args, **kwargs)
    # 条件查询
    # 条件可以是：参数，字典，Q
        
def exists(self):
   # 是否有结果
	apps.models.book.objects.filter(id=5).exists()	#判断过滤的条件是否是有数据返回

def select_related(self, *fields)
    性能相关：表之间进行join连表操作，一次性获取关联的数据。

    总结：
    1. select_related主要针一对一和多对一关系进行优化。
    2. select_related使用SQL的JOIN语句进行优化，通过减少SQL查询的次数来进行优化、提高性能。

def prefetch_related(self, *lookups)
    性能相关：多表连表操作时速度会慢，使用其执行多次SQL查询在Python代码中实现连表操作。

    总结：
    1. 对于多对多字段（ManyToManyField）和一对多字段，可以使用prefetch_related()来进行优化。
    2. prefetch_related()的优化方式是分别查询每个表，然后用Python处理他们之间的关系。

def annotate(self, *args, **kwargs)
    # 用于实现聚合group by查询

    from django.db.models import Count, Avg, Max, Min, Sum

    v = models.UserInfo.objects.values('u_id').annotate(uid=Count('u_id'))
    # SELECT u_id, COUNT(ui) AS `uid` FROM UserInfo GROUP BY u_id

    v = models.UserInfo.objects.values('u_id').annotate(uid=Count('u_id')).filter(uid__gt=1)
    # SELECT u_id, COUNT(ui_id) AS `uid` FROM UserInfo GROUP BY u_id having count(u_id) > 1

    v = models.UserInfo.objects.values('u_id').annotate(uid=Count('u_id',distinct=True)).filter(uid__gt=1)
    # SELECT u_id, COUNT( DISTINCT ui_id) AS `uid` FROM UserInfo GROUP BY u_id having count(u_id) > 1

def distinct(self, *field_names)
    # 用于distinct去重
    models.UserInfo.objects.values('nid').distinct()
    # select distinct nid from userinfo

    注：只有在PostgreSQL中才能使用distinct进行去重

def extra(self, select=None, where=None, params=None, tables=None, order_by=None, select_params=None)
    # 构造额外的查询条件或者映射，如：子查询

    Entry.objects.extra(select={'new_id': "select col from sometable where othercol > %s"}, select_params=(1,))
    Entry.objects.extra(where=['headline=%s'], params=['Lennon'])
    Entry.objects.extra(where=["foo='a' OR bar = 'a'", "baz = 'a'"])
    Entry.objects.extra(select={'new_id': "select id from tb where id > %s"}, select_params=(1,), order_by=['-nid'])

 def reverse(self):
    # 倒序
    models.UserInfo.objects.all().order_by('-nid').reverse()
    # 注：如果存在order_by，reverse则是倒序，如果多个排序则一一倒序


 def defer(self, *fields):
    models.UserInfo.objects.defer('username','id')
    或
    models.UserInfo.objects.filter(...).defer('username','id')
    #映射中排除某列数据

 def only(self, *fields):
    #仅取某个表中的数据
     models.UserInfo.objects.only('username','id')
     或
     models.UserInfo.objects.filter(...).only('username','id')

 def using(self, alias):
     指定使用的数据库，参数为别名（setting中的设置）

def raw(self, raw_query, params=None, translations=None, using=None):
    # 执行原生SQL
    models.UserInfo.objects.raw('select * from userinfo')

    # 如果SQL是其他表时，必须将名字设置为当前UserInfo对象的主键列名
    models.UserInfo.objects.raw('select id as nid from 其他表')

    # 为原生SQL设置参数
    models.UserInfo.objects.raw('select id as nid from userinfo where nid>%s', params=[12,])

    # 将获取的到列名转换为指定列名
    name_map = {'first': 'first_name', 'last': 'last_name', 'bd': 'birth_date', 'pk': 'id'}
    Person.objects.raw('SELECT * FROM some_other_table', translations=name_map)

    # 指定数据库
    models.UserInfo.objects.raw('select * from userinfo', using="default")

    ################### 原生SQL ###################
    from django.db import connection, connections
    cursor = connection.cursor()  # cursor = connections['default'].cursor()
    cursor.execute("""SELECT * from auth_user where id = %s""", [1])
    row = cursor.fetchone() # fetchall()/fetchmany(..)


def values(self, *fields):
    # 获取每行数据为字典格式
	# obj = apps.models.book.objects.all().values()
    obj = apps.models.book.objects.values("id","title")		# 取指定字段，不指定取全部字段
	# <QuerySet [{'id': 1, 'title': '鲁滨孙漂流记', 'state': False, 'price': 55}, {}>
        
def values_list(self, *fields, **kwargs):
    # 获取每行数据为元祖
	obj = apps.models.book.objects.values_list("id","title")		# 取指定字段，不指定取全部字段
	# <QuerySet [( 1, 鲁滨孙漂流记' ), ()>

def dates(self, field_name, kind, order='ASC'):
    # 根据时间进行某一部分进行去重查找并截取指定内容
    # kind只能是："year"（年）, "month"（年-月）, "day"（年-月-日）
    # order只能是："ASC"  "DESC"
    # 并获取转换后的时间
        - year : 年-01-01
        - month: 年-月-01
        - day  : 年-月-日

    models.DatePlus.objects.dates('ctime','day','DESC')

def datetimes(self, field_name, kind, order='ASC', tzinfo=None):
    # 根据时间进行某一部分进行去重查找并截取指定内容，将时间转换为指定时区时间
    # kind只能是 "year", "month", "day", "hour", "minute", "second"
    # order只能是："ASC"  "DESC"
    # tzinfo时区对象
    models.DDD.objects.datetimes('ctime','hour',tzinfo=pytz.UTC)
    models.DDD.objects.datetimes('ctime','hour',tzinfo=pytz.timezone('Asia/Shanghai'))

    """
    pip3 install pytz
    import pytz
    pytz.all_timezones
    pytz.timezone(‘Asia/Shanghai’)
    """

def none(self):
    # 空QuerySet对象


####################################
# METHODS THAT DO DATABASE QUERIES #
####################################

def aggregate(self, *args, **kwargs):
   # 聚合函数，获取字典类型聚合结果
   from django.db.models import Count, Avg, Max, Min, Sum
   result = models.UserInfo.objects.aggregate(k=Count('u_id', distinct=True), n=Count('nid'))
   ===> {'k': 3, 'n': 4}

def count(self):
   # 获取个数

def get(self, *args, **kwargs):
   # 获取单个对象

def create(self, **kwargs):
   # 创建对象

def bulk_create(self, objs, batch_size=None):
    # 批量插入
    # batch_size表示一次插入的个数
    objs = [
        models.DDD(name='r11'),
        models.DDD(name='r22')
    ]
    models.DDD.objects.bulk_create(objs, 10)

def get_or_create(self, defaults=None, **kwargs):
    # 如果存在，则获取，否则，创建
    # defaults 指定创建时，其他字段的值
    obj, created = models.UserInfo.objects.get_or_create(username='root1', defaults={'email': '1111111','u_id': 2, 't_id': 2})

def update_or_create(self, defaults=None, **kwargs):
    # 如果存在，则更新，否则，创建
    # defaults 指定创建时或更新时的其他字段
    obj, created = models.UserInfo.objects.update_or_create(username='root1', defaults={'email': '1111111','u_id': 2, 't_id': 1})

def first(self):
   # 获取第一个

def last(self):
   # 获取最后一个

def in_bulk(self, id_list=None):
   # 根据主键ID进行查找
   id_list = [11,21,31]
   models.DDD.objects.in_bulk(id_list)

def delete(self):
   # 删除

def update(self, **kwargs):
    # 更新


```

**模糊查询：**

```c
Book.objects.filter(price__in=[100,200,300]) #price值等于这三个里面的任意一个的对象
Book.objects.filter(price__gt=100)  #大于，大于等于是price__gte=100，别写price>100，这种参数不支持
Book.objects.filter(price__lt=100)
Book.objects.filter(price__range=[100,200])  #sql的between and，大于等于100，小于等于200
Book.objects.filter(title__contains="python")  #title值中包含python的
Book.objects.filter(title__icontains="python") #不区分大小写
Book.objects.filter(title__startswith="py") #以什么开头，istartswith  不区分大小写
Book.objects.filter(title__endswith="py") #以什么开头，iendswith  不区分大小写
Book.objects.filter(pub_date__year=2012)
```

