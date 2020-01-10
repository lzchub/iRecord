# yum安装ansible #

	~]# cat <<eof>>/etc/yum.repos.d/my.repo
	[epel]
	name=epel
	baseurl=http://mirrors.aliyun.com/epel/7Server/x86_64/
	enable=1
	gpgcheck=0
	eof

	~]# yum list --showduplicates ansible	#可选择版本进行安装，ansible基于Python开发，会依赖安装Python
	~]# ansible --version
		ansible 2.8.0
		  config file = /etc/ansible/ansible.cfg
		  configured module search path = [u'/root/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
		  ansible python module location = /usr/lib/python2.7/site-packages/ansible
		  executable location = /usr/bin/ansible
		  python version = 2.7.5 (default, Oct 30 2018, 23:45:53) [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
	
	注意：需要将公钥发到控制机器上
	~]# ssh-keygen -t rsa	#回车

	~]# cat sendpub.sh 
		#!/bin/bash
		
		#author by chuan
		
		IP=192.168.164
		PASSWD=960711
		USER=root
		PORT=22
		
		for i in {137,139,141,142,143}
		do
		        sshpass -p $PASSWD ssh-copy-id root@$IP.$i &> /dev/null
		        [ $? -eq 0 ] && {
		                echo "public key send to $IP.$i... "
		        }
		        sleep 1
		done

	~]# vi /etc/ansible/hosts			#配置主机
		[GROUP_NAME]
		HOST

	

#1. ansible
##1.1 常用参数

	1. -a MODULE_ARGS，--args=MODULE_ARGS：传递参数给模块。
	2. -C，--check：不对远程主机做出一些改变，而是预测某些可能发生的改变。
	3. -e EXTRA_VARS，--extra-vars=EXTRA_VARS：配置额外的配置变量(key=value或者YAML/JSON格式)。
	4. -i INVENTORY，--inventory-file=INVENTORY：指定inventory文件，多个文件使用逗号分隔。默认为/etc/ansible/hosts。
	5. -m MODULE_NAME，--module-name=MODULE_NAME：指定要执行的模块名，默认的模块为"command"。
	6. -o，--one-line：简化输出(一行输出模式)。
	7. --syntax-check：检查playbook的语法，不会执行。

##1.2 常用模块
###1.查看所有匹配到的主机

	~]# ansible all --list-hosts		#列出所有匹配到的地址

###2.测试是否连接

	~]# ansible all -m ping		#测试是否能连接

###3.指定inventory文件
多个文件使用逗号分隔。默认为/etc/ansible/hosts

	~]# ansible all -i /root/hosts -m ping	#指定hosts文件	

###4.查看模块信息

	~]# ansible-doc -l		#查看所有模块
	~]# ansible-doc -s MODULE	#查看某个模块	

###5.copy
copy模块：拷贝文件

	ansible-doc -s copy
	- name: Copies files to remote locations.
	action: copy
	    backup=[yes|no]   # 拷贝的同时也创建一个包含时间戳信息的备份文件，默认为no
	    dest=             # 目标路径，只能是绝对路径，如果拷贝的文件是目录，则目标路径必须也是目录
	    content           # 直接以content给定的字符串或变量值作为文件内容保存到远程主机上，它会替代src选项
	    directory_mode    # 当对目录做递归拷贝时，设置了directory_mode将会使得只拷贝新建文件，
	                      # 旧文件不会被拷贝。默认未设置
	    follow=[yes|no]   # 是否追踪到链接的源文件。
	    force=[yes|no]    # 设置为yes(默认)时，将覆盖远程同名文件。设置为no时，忽略同名文件的拷贝。
	    group             # 设置远程文件的所属组
	    owner             # 设置远程文件的所有者
	    mode=             # 设置远程文件的权限。使用数值表示时不能省略第一位，如0644。
	                      # 也可以使用'u+rwx'或'u=rw,g=r,o=r'等方式设置。
	    src=              # 拷贝本地源文件到远程，可使用绝对路径或相对路径。如果路径是目录，且目录后加了
	                      # 斜杠"/"，则只会拷贝目录中的内容到远程，如果目录后不加斜杠，则拷贝目录本身和
	                      # 目录内的内容到远程。
	
	~]# ansible all -m copy -a "src=test.txt dest=/tmp/test.txt"	#将本地test.txt文件拷贝到目标机器中
	~]# ansible all -m copy -a "content='test page' dest=/tmp/content.txt"	#将content中的字符串当做输入
	~]# ansible all -m copy -a "src=test.txt dest=/tmp/content.txt mode=0770 owner=sshd group=sshd backup=yes" -o  	#指定用户，组，且使用一行输出
	~]# ansible all -m copy -a "src=/root/a dest=/tmp" -o	#a，a/*都将拷贝
	~]# ansible all -m copy -a "src=/root/a/ dest=/tmp" -o		#a/*都将拷贝
###6.shell
shell模块，command模块（默认）：执行指定命令

	
	ansible-doc -s shell
	- name: Execute commands in nodes.
	- action: shell
	      chdir       # 在执行命令前，先cd到指定的目录下
	      creates     # 用于判断命令是否要执行。如果指定的文件(可以使用通配符)存在，则不执行。
	      removes     # 用于判断命令是否要执行。如果指定的文件(可以使用通配符)不存在，则不执行。


	~]# ansible all -m command -a "ls /tmp"		
	~]# ansible all -m shell -a "echo $PATH"
###7.file
file文件模块：管理文件、目录的属性，也可以创建文件或目录。

	ansible-doc -s file
	- name: Sets attributes of files
	  action: file
      group       # file/directory的所属组
      owner       # file/directory的所有者
      mode        # 修改权限，格式可以是0644、'u+rwx'或'u=rw,g=r,o=r'等
      path=       # 指定待操作的文件，可使用别名'dest'或'name'来替代path
      recurse     # (默认no)递归修改文件的属性信息，要求state=directory
      src         # 创建链接时使用，指定链接的源文件
      state       # directory:如果目录不存在则递归创建
                  # file:文件不存在时，不会被创建(默认值)
                  # touch:touch由path指定的文件，即创建一个新文件，或修改其mtime和atime
                  # link:修改或创建软链接
                  # hard:修改或创建硬链接
                  # absent:目录和其中的文件会被递归删除，文件或链接将取消链接状态

	~]# ansible all -m file -a "path=/tmp/x/y/z state=directory group=root owner=root mode=0755 recurse=yes"	
	~]# ansible all -m file -a "src=/tmp/x/y/z state=link dest=/tmp/linktest"
###8.fetch
fetch拉取文件模块：和copy工作方式类似，只不过是从远程主机将文件拉取到本地端，存储时使用主机名作为目录树，且只能拉取文件不能拉取目录。

	ansible-doc -s fetch
	- name: Fetches a file from remote nodes
	  action: fetch
      dest=               # 本地存储拉取文件的目录。例如dest=/data，src=/etc/fstab，
                          # 远程主机名host.exp.com，则保存的路径为/data/host.exp.com/etc/fstab。
      fail_on_missing     # 当设置为yes时，如果拉取的源文件不存在，则此任务失败。默认为no。
      flat                # 改变拉取后的路径存储方式。如果设置为yes，且当dest以"/"结尾时，将直接把源文件
                          # 的basename存储在dest下。显然，应该考虑多个主机拉取时的文件覆盖情况。
      src=                # 远程主机上的源文件。只能是文件，不支持目录。在未来的版本中可能会支持目录递归拉取。
      validate_checksum   # fetch到文件后，检查其md5和源文件是否相同。

	~]# ansible 192.168.179.111 -m fetch -a "src=/etc/fstab dest=/tmp" 
	~]# ansible 192.168.179.111 -m fetch -a "src=/etc/fstab dest=/tmp/ flat=yes"

###9.yum
yum包管理模块:

	ansible-doc -s yum
	- name: Manages packages with the `yum' package manager
	action: yum
    disable_gpg_check   # 安装包时禁止gpgcheck，仅在state=present或latest时生效。
    disablerepo         # 禁用指定的repoid，多个repoid使用逗号分隔。
    enablerepo          # 明确使用该repoid
    exclude             # 排除哪些包不安装，仅在state=present或latest时生效。
    list                # 类似于yum list
    name=               # 指定安装的包名，可带上版本号.
    state               # 状态。('present'、'installed','latest')用于安装包，
                        # ('absent'、'removed')用于移除已安装包。
    update_cache        # 强制更新yum的cache。

	~]# ansible all -m yum -a "list=ansible"
	~]# ansible all -m yum -a "name=httpd state=installed"
	~]# ansible centos -m yum -a "name=httpd state=removed"
	~]# ansible centos -m yum -a "name=/tmp/*.rpm exclude=*unix* state=present"		#安装本地的包，且排除某些包不安装。

###10.yum_repository 
yum_repository配置yum源模块:用于配置yum源。可以实现非常完整的yum仓库配置。但是一般只需简单的添加yum源即可。

	ansible-doc -s yum_repository
	- name: Add or remove YUM repositories
    action: yum_repository
      baseurl      # 地址
      mirrorlist   # 设置mirrorlist地址
      description  # 描述信息
      enabled      # 是否启用该仓库，默认为yes
      file         # 保存此仓库的文件，不设置该项的话则默认以name选项中的名称命名，将自动以".repo"后缀结尾。
      gpgcheck     # 是否要进行gpgcheck
      name=        # 仓库的名称，要保证名称的唯一性
      reposdir     # 保存.repo文件的目录，默认/etc/yum.repos.d/
      state        # repo文件的状态，present/absent，默认present。

	~]# ansible 192.168.100.63 -m yum_repository -a 'name=aliyun_epel description="epel repo" baseurl=http://mirrors.aliyun.com/epel/7/$basearch/ gpgcheck=no enabled=yes'

	例如：
	- name: Add repository
	  yum_repository:
	    name: aliyun_epel
	    description: EPEL YUM repo
	    baseurl: http://mirrors.aliyun.com/epel/7/$basearch/
		gpgcheck: no
	
	- name: Add multiple repositories into a file
	  yum_repository:
	    name: epel
	    description: EPEL YUM repo
	    file: sohu_epel
	    baseurl: http://mirrors.sohu.com/fedora-epel/7/$basearch/
	    gpgcheck: no



###11.service
service服务管理模块：

	ansible-doc -s service
	- name: Manage services.
	  action: service
      enabled   # 设置服务为开机自启动，默认为no
      name=     # 服务名
      state     # 'started'和'stoped'分别启动和停止服务，它们是幂等操作，多次启动或停止服务的结果是一样的，
                # 也就是说对于运行中的服务不会再执行启动操作，同理停止也是一样。'restarted'总是重启服务，
                # 'reloaded'总是重读配置文件，如果服务是未运行状态，则'reloaded会启动服务。
                # (state和enabled两者至少要给一个)

	~]# ansible all -m service -a "name=httpd state=started"
	~]# ansible all -m service -a "name=httpd enabled=yes"

###12.user
user用户管理模块：同理还有组管理模块group，就不多做说明了。

	ansible-doc -s user
	- name: Manage user accounts
	action: user
      name=            # 要创建、修改、移除的用户名。
      password         # 设置用户密码。此处只能使用加密密码作为值。
      system           # 设置为yes表示创建一个系统用户，只能用于创建，不能用于修改已有用户为系统用户。
      state            # 创建用户(present)还是删除用户(absent)。默认为present。
      createhome       # 创建家目录，或者已有的用户但家目录不存在也会创建。设置为no则不创建家目录。
      home             # 指定要创建的家目录路径
      move_home        # 如果设置为yes，则"home="则表示将家目录移动到此选项指定的路径下。
      uid              # 设置用户的uid
      group            # 设置用户的primary group
      groups           # 将用户加入到辅助组列表中。如果设置"groups="，则会将此用户从所有辅助组中移除。
      shell            # 设置用户的shell。
      force            # 配合'state=absent'时，等价于'userdel --force'，即强制删除用户、家目录和邮件列表。
      remove           # 配合'state=absent'时，等价于'userdel --remove'，即删除家目录和邮件列表。
      update_password  # user是幂等模块，"always"将总是修改密码。"on_create"将只在创建用户时设置密码。

	~]# ansible all -m user -a "name=chuan system=yes shell=/sbin/nologin"

	~]# openssl passwd -1 123456
	$1$9jwmFoVU$MVz7ywscpoPS5WXC.srcP/
	~]# ansible all -m user -a "name=chuan password='$1$fAGodLjd$XvKeD.4J.o0phHQPXHoRE/' update_password=always"

	~]# ansible all -m user -a "name=chuan state=absent"

###13.debug
debug模块：用于输出自定义的信息，类似于echo、print等输出命令。ansible中的debug主要用于输出变量值、表达式值，以及用于when条件判断时。

	ansible-doc -s debug
	- name: Print statements during execution
	action: debug
      msg        # 输出自定义信息。如果省略，则输出普通字符。
      var        # 指定待调试的变量。只能指定变量，不能指定自定义信息，且变量不能加{{}}包围，而是直接的变量名。
      verbosity  # 控制debug运行的调试级别，有效值为一个数值N。		

	~]# ansible all -m debug -a "msg='i want to print this message'"

	可以输出变量值，不过一般使用到变量的时候都会在playbook中使用debug模块，以下是一个示例：
	tasks:
	  - name: print any messages
	      debug: msg="you name is {{ name }}"

###14.cron
cron定时任务模块：cron模块用于设置定时任务，也用于管理定时任务中的环境变量。

	ansible-doc -s cron
	- name: Manage cron.d and crontab entries.
    action: cron
      backup         # (yes/no)如果设置了，则会在修改远程cron_file前备份这些文件
      cron_file      # 自定义cron_file的文件名，使用相对路径则表示在/etc/cron.d中。必须同时指定user选项
      user           # 指定哪个用户的crontab将要被修改，默认为root
      disabled       # 禁用crontab中的某个job，要求state=present
      env            # (yes/no)设置一个环境变量，将添加在crontab的顶端。使用name和value定义变量名和值
      job            # 需要执行的命令。如果设置了env，则表示环境变量的值，此时job="XXXX"等价于value="XXXX"。
                     # 要求state=present
      minute         # 分(0-59, *, */N)，不写时，默认为*
      hour           # 时(0-23, *, */N)，不写时，默认为*
      day            # 日(1-31, *, */N)，不写时，默认为*
      month          # 月(1-12, *, */N)，不写时，默认为*
      weekday        # 周(0-6 for Sunday-Saturday, *)，不写时，默认为*
      name           # 描述crontab任务的字符串。但如果设置的是env，则name为环境变量的名称。要求state=absent
                     # 注意，若未设置name，且state=present，则总会创建一个新job条目，即使cron_file中已经存在
                     # 同样的条目
      special_time   # 定时任务的别称，用于定义何时运行job条目。
                     # 有效值有reboot/hourly/daily/weekly/monthly/yearly/annually。
      state          # job或者env的状态是present(默认)还是absent。present用于创建，absent用于移除

	~]# ansible all -m cron -a "name='update' job='/usr/sbin/ntpdate ntp1.aliyun.com' minute=*/10"
	~]# ansible all -m shell -a "crontab -l"
		192.168.179.112 | CHANGED | rc=0 >>
		#Ansible: update
		*/10 * * * * /usr/sbin/ntpdate ntp1.aliyun.com
		
		192.168.179.111 | CHANGED | rc=0 >>
		#Ansible: update
		*/10 * * * * /usr/sbin/ntpdate ntp1.aliyun.com
	~]# ansible all -m cron -a "name='update' state=absent"

	~]# ansible centos7 -m cron -a 'name="ntpdate" job="/usr/sbin/ntpdate ntp1.aliyun.com" cron_file=ntpdate_cron user=root minute=*/2' -o
	~]# ansible centos7 -m cron -a 'name="ntpdate" state=absent cron_file=ntpdate_cron user=root' -o

###15.archive
archive归档模块：于在远端压缩文件。当然，前提是在远端主机上要有对应的压缩工具。支持zip/gz/tar/bz2。
	
	ansible-doc -s archive 
	- name: Creates a compressed archive of one or more files or trees.
    action: archive
      dest         # 目标归档文件名。除非path指定要压缩的是单文件，否则需要dest选项
      format       # 指定压缩格式，默认为gz格式
      group        # 文件/目录的所属组
      owner        # 文件/目录的所有者
      mode         # 设置文件/目录的的权限，支持'0644'或'u+rwx'或'u=rw,g=r,o=r'等格式
      path=        # 要压缩的文件，可以是绝对路径，也可以是glob统配的路径，还可以是文件列表
      remove       # 压缩后删除源文件

	例如：
	# 将目录/path/to/foo/压缩为/path/to/foo.tgz
	- archive:
	    path: /path/to/foo
	    dest: /path/to/foo.tgz
	
	# 压缩普通文件/path/to/foo为/path/to/foo.gz并删除源文件，由于压缩的是单文件，所以可以省略dest选项
	- archive:
	    path: /path/to/foo
	    remove: True
	
	# 将单文件/path/to/foo压缩为zip格式
	- archive:
	    path: /path/to/foo
	    format: zip
	
	# 将给定的文件列表压缩为bz2格式，压缩包路径为/path/file.tar.bz2
	- archive:
	    path:
	        - /path/to/foo
	        - /path/wong/foo
	    dest: /path/file.tar.bz2
	    format: bz2

###16.unarchive
unarchive解包模块：默认复制ansible端的归档文件到被控主机，然后在被控主机上进行解包。如果设置选项remote_src=yes，则表示解包被控主机上的归档文件。要求在被控主机上有对应的解包命令。unzip命令用于解压".zip"文件，gtar(tar包提供)命令用于解压".tar"、".tar.gz"、".tar.bz2"和".tar.xz"。

	ansible-doc -s unarchive
	- name: Unpacks an archive after (optionally) copying it from the local machine.
    action: unarchive
      creates      # 如果指定的文件存在则不执行该任务。可用于实现幂等性
      dest=        # 远程机器上需要被解包的归档文件，要求是绝对路径
      exclude      # 列出解包过程中想要忽略的目录和文件
      group        # 文件/目录的所属组
      owner        # 文件/目录的所有者
      mode         # 设置文件/目录的的权限，支持'0644'或'u+rwx'或'u=rw,g=r,o=r'等格式
      keep_newer   # 在解包过程中，如果目标路径中和包中有同名文件，且比包中的文件更新，则保留新的文件
      list_files   # 设置为true时，将返回归档文件中的文件列表
      remote_src   # 设置为yes表示远程主机上已有目标归档文件，即不再从本地复制归档文件到远端，直接在远端解包。
                   # 默认为no
      src=         # 如果remote_src=no,将复制本地归档文件到远端，可相对路径也可绝对路径. 
                     如果remote_src=yes, 将解包远程已存在的归档文件
                     如果remote_src=yes且src中包含了"://",将指挥远程主机从url中下载文件并解包

	例如：
	# 复制ansible端的foo.tgz文件到远端并解包
	- unarchive:
	    src: foo.tgz
	    dest: /var/lib/foo
	
	# 直接解包远端已经存在的文件- unarchive:
	    src: /tmp/foo.zip
	    dest: /usr/local/bin
	    remote_src: True
	
	# 从url上下载压缩包，然后进行解压
	- unarchive:
	    src: https://example.com/example.zip
	    dest: /usr/local/bin
	    remote_src: True

###17.script
script模块：用于控制远程主机执行脚本。在执行脚本前，ansible会将本地脚本传输到远程主机，然后再执行。在执行脚本的时候，其采用的是远程主机上的shell环境。

	ansible-doc -s script
	- name: Runs a local script on a remote node after transferring it
    action: script
      chdir         # 在远程执行脚本前先切换到此目录下。
      creates       # 当此文件存在时，不执行脚本。可用于实现幂等性。
      removes       # 当此文件不存在时，不执行脚本。可用于实现幂等性。
      free_form=    # 本地待执行的脚本路径、选项、参数。之所以称为free_form，是因为它是脚本名+选项+参数。

	例如，将ansible端/tmp/a.sh发送到各被控节点上执行，但如果被控节点的/tmp下有hello.txt，则不执行。
    - hosts: centos
      remote_user: root
      tasks:
        - name: execute /tmp/a.sh,but only /tmp/hello.txt is not yet created
          script: /tmp/a.sh hello
          args:
            creates: /tmp/hello.txt

###18.template
template模块：template模块用法和copy模块用法基本一致，它主要用于复制配置文件（配合jinja2模板使用）。

	ansible-doc -s template
	- name: Templates a file out to a remote server.
    action: template
      backup    # 拷贝的同时也创建一个包含时间戳信息的备份文件，默认为no
      dest=     # 目标路径
      force     # 设置为yes (默认)时，将覆盖远程同名文件。设置为no时，忽略同名文件的拷贝
      group     # 设置远程文件的所属组
      owner     # 设置远程文件的所有者
      mode      # 设置远程文件的权限。使用数值表示时不能省略第一位，如0644。
                # 也可以使用'u+rwx' or 'u=rw,g=r,o=r'等方式设置
      src=      # ansible控制器上Jinja2格式的模板所在位置，可以是相对或绝对路径
      validate  # 在复制到目标主机后但放到目标位置之前，执行此选项指定的命令。
                # 一般用于检查配置文件语法，语法正确则保存到目标位置。
                # 如果要引用目标文件名，则使用%s，下面的示例中的%s即表示目标机器上的/etc/nginx/nginx.conf。

	~]# ansible centos -m template -a "src=/tmp/nginx.conf.j2 dest=/etc/nginx/nginx.conf mode=0770 owner=root group=root backup=yes validate='nginx -t -c %s'" -o -f 6

	- tasks: 
     - name: template file based var
       template: src=/templates/nginx{{ ansible_distribution_major_version }}.conf.j2 dest=/etc/nginx/nginx.conf validate="/usr/sbin/nginx -t -c %s"

###19.setup
	acts组件是用来收集被管理节点信息的，使用setup模块可以获取这些信息。


	ansible-doc -s setup
	- name: Gathers facts about remote hosts
  	action: setup:
      fact_path:             # path used for local ansible facts (`*.fact') - files in this dir will be run (if executable) and their results be added to `ansible_local'
                               facts if a file is not executable it is read. Check notes for Windows options. (from 2.1 on) File/results
                               format can be json or ini-format
      filter:                # if supplied, only return facts that match this shell-style (fnmatch) wildcard.
      gather_subset:         # if supplied, restrict the additional facts collected to the given subset. Possible values: `all', `min', `hardware', `network', `virtual',
                               `ohai', and `facter'. Can specify a list of values to specify a larger subset. Values can also be used with
                               an initial `!' to specify that that specific subset should not be collected.  For instance:
                               `!hardware,!network,!virtual,!ohai,!facter'. If `!all' is specified then only the min subset is collected.
                               To avoid collecting even the min subset, specify `!all,!min'. To collect only specific facts, use
                               `!all,!min', and specify the particular fact subsets. Use the filter parameter if you do not want to display
                               some collected facts.
      gather_timeout:        # Set the default timeout in seconds for individual fact gathering

	~]# ansible 192.168.179.111 -m setup


##1.3 playbook应用
###1.3.1 ansible-playbook参数

ansible-playbook命令的选项和ansible命令选项绝大部分都相同。但也有其特有的选项。以下是截取出来的帮助信息。

	~]# ansible-playbook --help
	Usage: ansible-playbook playbook.yml
	
	Options:
	  -e EXTRA_VARS,--extra-vars=EXTRA_VARS # 设置额外的变量，格式为key/value。-e "key=KEY"，
	                                        # 如果是文件方式传入变量，则-e "@param_file"
	  --flush-cache          # 清空收集到的fact信息缓存
	  --force-handlers       # 即使task执行失败，也强制执行handlers
	  --list-tags            # 列出所有可获取到的tags
	  --list-tasks           # 列出所有将要被执行的tasks
	  -t TAGS,--tags=TAGS    # 以tag的方式显式匹配要执行哪些tag中的任务
	  --skip-tags=SKIP_TAGS  # 以tag的方式忽略某些要执行的任务。被此处匹配的tag中的任务都不会执行
	  --start-at-task=START_AT_TASK # 从此task开始执行playbook
	  --step                 # one-step-at-a-time:在每一个任务执行前都进行交互式确认
	  --syntax-check         # 检查playbook语法

###1.3.2 nginx（反代）+ tomcat

实验环境：	
	192.168.179.110：ansible
	192.168.179.115：nginx
	192.168.179.111：tomcat1
	192.168.179.112：tomcat2


	roles/
	|-- jdk
	|   |-- default
	|   |-- files
	|   |   `-- java.sh
	|   |-- handlers
	|   |-- meta
	|   |-- tasks
	|   |   `-- main.yaml
	|   |-- templates
	|   `-- vars
	|       `-- main.yaml
	|-- nginx
	|   |-- default
	|   |-- files
	|   |   `-- lb.conf
	|   |-- handlers
	|   |   `-- main.yaml
	|   |-- meta
	|   |-- tasks
	|   |   `-- main.yaml
	|   |-- templates
	|   `-- vars
	`-- tomcat
	    |-- default
	    |-- files
	    |-- handlers
	    |   `-- main.yaml
	    |-- meta
	    |-- tasks
	    |   `-- main.yaml
	    |-- templates
	    |   `-- server.xml.j2
	    `-- vars

	nginx:
		~]# yum install -y ansible
		~]# cd /etc/ansible
		~]# mkdir -pv roles/{nginx,tomcat,jdk}/{files,templates,tasks,handlers,vars,meta,default} 
		~]# vim roles/nginx/tasks/main.yaml
			- name: install nginx
			  yum:
			    name: nginx
			    state: latest
			  when: 
			    - ansible_os_family == "RedHat"
			- name: copy conf file
			  copy:
			    src: lb.conf
			    dest: /etc/nginx/conf.d/
			  tags: conf
			  notify: restart nginx
			- name: start nginx
			  service:
			    name: nginx
			    state: started
			    enabled: yes
		~]# vim roles/nginx/handlers/main.html
			- name: restart nginx
			  service:
			    name: nginx
			    state: restarted
		~]# vim roles/nginx/files/lb.conf
			upstream tcsrvs {
	        server 192.168.179.111:8080;
	        server 192.168.179.112:8080;
			}
			server {
			        listen 192.168.179.115:80;
			        server_name www.ilinux.io;
			        location / {
			                proxy_pass http://tcsrvs;
			        }
			}

	tomcat:
		~]# cat roles/tomcat/handlers/main.yaml 
			- name: restart tomcat
  			service: name=tomcat state=restarted
		~]# cat tasks/main.yaml    
			- name: install packages
			  yum:
			#    name="{{item}}"
			#    state=latest
			    name: [tomcat,tomcat-admin-webapps,tomcat-webapps,tomcat-docs-webapp]
			    state: latest
			#  with_items:
			#    - tomcat
			#    - tomcat-admin-webapps
			#    - tomcat-webapps
			#    - tomcat-docs-webapp
			#  when:
			#    - ansible_os_family == "Redhat"
			- name: copy conf file
			  template: src=server.xml.j2 dest=/etc/tomcat/server.xml
			  tags: conf
			  notify: restart tomcat
			- name: start tomcat
			  service: name=tomcat state=started enabled=yes

	jdk:
		~]# cat tasks/main.yaml 
			- name: install jdk
			  yum: name=java-{{ version }}-openjdk-devel state=latest
			- name: config env file
			  copy: src=java.sh dest=/etc/profile.d/
			- name: flush env
			  shell: . /etc/profile.d/java.sh
		~]# cat vars/main.yaml 
			version: 1.8.0
		~]# cat files/java.sh 
			export JAVA_HOME=/usr
			export PATH=$JAVA_HOME/bin:$PATH


		~]# cat nt.yaml		#只要有nginx角色，任何主机都可运行
			- hosts: lbsrvs
			  remote_user: root
			  roles:
			  - nginx
			- hosts: tcsrvs
			  remote_user: root
			  roles:
			#  - { role: jdk, version: 1.8.0 }
			  - tomcat
			  - jdk