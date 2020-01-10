**vm.memory.size[<mode>]：**

	内存大小，以字节：整数 

	total - 总物理内存.
	free - 可用内存.
	active - 内存当前使用或最近使用，所以它在RAM中。
	inactive - 未使用内存.
	wired - 被标记为始终驻留在RAM中的内存，不会移动到磁盘。
	pinned - 和'wired'一样。
	anon - 与文件无关的内存(不能重新读取)。
	exec - 可执行代码，通常来自于一个(程序)文件。
	file - 缓存最近访问文件的目录。
	buffers - 缓存文件系统元数据。
	cached - 缓存为不同事情。
	shared - 可以同时被多个进程访问的内存。
	used - active + wired 内存。
	pused - active + wired 总内存的百分比。
	available - inactive + cached + free 内存。
	pavailable - inactive + cached + free memory 占'total'的百分比。

	注：vm.memory.size[used] 和 vm.memory.size[available] 的和不是必需等于总内存。 例如, 在FreeBSD中 active, inactive, wired, cached被认为是使用的内存， 因为他们存储一些有用的信息。同样，inactive, cached, free 也被认为是可用内存， 因为这些内存可以立即被分配给需要更多内存的线程。 所以不活动的内存是同时可以是使用和可用的。 正因为如此, item vm.memory.size[used] 只用来获得信息, 监控项 vm.memory.size[available] 在触发器中使用


**system.cpu.util[<cpu>,<type>,<mode>]**

	CPU 利用率：浮点型 

	cpu：CPU 数量或者all(默认值)	system.cpu.util[0,user,avg5]
	type：可能的值 idle, nice, user(默认值),system(Windows系统默认值),iowait, interrupt,softirq,steal, guest
	mode：avg1 (1分钟平均值,默认值), avg5, avg15

**vfs.fs.size[fs,<mode>]**

	磁盘空间，以字节为单位，用百分比表示。 整数 - 针对字节   浮点- 针对百分比
	fs：文件系统
	mode：可能的值 total(默认),free,used,pfree(剩余,百分比),pused(已用,百分比)
