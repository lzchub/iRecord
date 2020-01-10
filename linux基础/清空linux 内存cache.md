
# 问题

	日志网站磁盘满了，但是删除文件后，可见磁盘有剩余，但是没有可用空间

	~]# cat /proc/sys/vm/drop_caches 		#默认为0
		0

	#sync 命令将所有未写的系统缓冲区写到磁盘中，包含已修改的 i-node、已延迟的块 I/O 和读写映射文件
	~]# sync && echo 1 > /proc/sys/vm/drop_caches		#清空内存cache  这里可以有 1 2 3 三个参数

	