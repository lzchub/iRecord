##控制单元类型 

	定义控制单元 [Unit]

	在 Systemd 中，所有引导过程中 Systemd 要控制的东西都是一个单元。Systemd 单元类型有：
	
	系统服务
	套接字（socket）
	设备
	挂载点
	自动挂载点
	SWAP 文件
	分区
	启动对象（startup target）
	文件系统路径
	定时器


##Systemd编写服务管理脚本

####1. service unit文件格式

	/usr/lib/systemd/system	：每个服务最主要的启动脚本设置，类似于之前的/etc/init.d/
	/run/systemd/system		：系统执行过程中所产生的服务脚本，比上面目录优先运行
	/etc/systemd/system		：管理员建立的执行脚本，类似于/etc/rc.d/rcN.d/Sxx类的功能，比上面目录优先运行

**示例：**

	[Unit]
	Description=The Apache HTTP Server
	After=network.target remote-fs.target nss-lookup.target
	Documentation=man:httpd(8)
	Documentation=man:apachectl(8)
	
	[Service]
	Type=notify
	EnvironmentFile=/etc/sysconfig/httpd
	ExecStart=/usr/sbin/httpd $OPTIONS -DFOREGROUND
	ExecReload=/usr/sbin/httpd $OPTIONS -k graceful
	ExecStop=/bin/kill -WINCH ${MAINPID}
	# We want systemd to give httpd some time to finish gracefully, but still want
	# it to kill httpd after TimeoutStopSec if something went wrong during the
	# graceful stop. Normally, Systemd sends SIGTERM signal right after the
	# ExecStop, which would kill httpd. We are sending useless SIGCONT here to give
	# httpd time to finish.
	KillSignal=SIGCONT
	PrivateTmp=true
	
	[Install]
	WantedBy=multi-user.target

#### 2. 服务类型 unit 的详细配置

	配置文件分为三个部分，每个部分中都可以提供详细的配置信息

	[Unit]		：定义与Unit类型无关的通用选项，用于提供unit的描述信息、unit行为及依赖关系等
	[Service]	：与特定类型相关的专用选项，此处为Service类型
	[Install]	：定义由"systemctl enable"以及"systemctl disable"命令在实现服务启用或禁用时用到的一些选项

	[Unit]
		Description    	：关于该 unit 的简易说明
		Documentation  	：文档相关的内容，man手册或者官网文链接等
		After    	   	：说明本 unit 是在哪个服务启动之后才启动的意思，仅是说明服务启动的顺序而已，并没有强制要求
		Before    		：与 After 的意义相反，在指定的服务启动前最好启动本个服务的意思，仅是说明服务启动的顺序而已，并没有强制要求
		Requires   		：本 unit 需要在哪个服务启动后才能够启动！就是设置服务间的依赖性，如果在此项设置的前导服务没有启动成功，那么本 unit 就不会被启动
		Wants    		：与 Requires 刚好相反，规范的是这个 unit 之后还要启动什么服务，如果这 Wants 后面接的服务如果没有启动成功，其实不会影响到这个 unit 本身
		Conflicts    	：这个项目后面接的服务如果有启动，那么本 unit 就不能启动！如果本 unit 启动了，则指定的服务就不能启动

	[Service]
		User			：启动服务的用户
		Group			：启动服务的用户组
		Type			
				simple	：默认值，这个服务主要由 ExecStart 设置的程序来启动，启动后常驻于内存中
				forking	：由 ExecStart 指定的启动的程序通过 spawns 产生子进程提供服务，然后父进程退出
				oneshot	：与 simple 类似，不过这个程序在工作完毕后就结束了，不会常驻在内存中
				dbus	：与 simple 类似，但这个服务必须要在取得一个 D-Bus 的名称后，才会继续运行！因此设置这个项目时，通常也要设置 BusName= 才行
				idle	：与 simple 类似，意思是，要执行这个服务必须要所有的工作都顺利执行完毕后才会执行。这类的服务通常是开机到最后才执行即可的服务
				notify	：与 simple 类似，但这个服务必须要收到一个 sd_notify() 函数发送的消息后，才会继续运行

		ExecStart		：就是实际执行此服务的程序。接受 "命令 参数 参数..." 的格式，不能接受 <, >, >>, |, & 等特殊字符，很多的 bash 语法也不支持。所以，要使用这些特殊的字符时，最好直接写入到脚本里面去
		ExecStartPre 	：服务启动前，执行额外的命令
		ExecStartPost	：服务启动后，执行额外的命令
		ExecStop 		：用来实现 systemctl stop 命令，关闭服务
		ExecReload 		：用来实现 systemctl reload 命令，重新加载服务的配置信息
		Restart 		：当设置为 Restart=1 时，如果服务终止，就会自动重启此服务
		RestartSec 		：与 Restart 配合使用，在服务终止多长时间之后才重新启动它，默认是 100ms
		KillMode		：默认值，如果是 process 则服务终止时，只会终止主要的程序(ExecStart接的后面那串指令)
						  如果是 control-group 时，则由此 daemon 所产生的其他 control-group 的程序，也都会被关闭
						  如果是 none 的话，则没有程序会被关闭
		TimeoutSec		：若这个服务在启动或者是关闭时，因为某些缘故导致无法顺利 "正常启动或正常结束" 的情况下，则我们要等多久才进入 "强制结束" 的状态
		RemainAfterExit	：当设置为 RemainAfterExit=1 时，则当这个服务所属的所有程序都终止之后，此服务会再尝试启动。这对于 Type=oneshot 的服务很有帮助
		Environment 	：用来设置环境变量，可以使用多次，一行一个变量 "Environment=ENV_NAME=name"
		EnvironmentFile	:通过文件的方式设置环境变量,文件中 "ENV_NAME=name"
		
	[Install]
		WantedBy		:个设置后面接的大部分是 *.target unit，意思是，这个 unit 本身是附挂在哪个 target unit 下面
		Also			：当目前这个 unit 被 enable 时，Also 后面接的 unit 也要 enable 的意思
		Alias			：当 systemctl enable 相关的服务时，则此服务会进行链接文件的创建
		RequiredBy		：被哪些units所依赖，强依赖

#### 3. 加载进内核

	~]# systemctl daemon-reload