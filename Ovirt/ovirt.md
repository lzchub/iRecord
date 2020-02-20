# ovirt测试环境搭建

###实验准备

	192.168.5.40 ovirt-engine.com
	192.168.5.41 ovirt-node.com

###ovirt-engine
	
	~]# hostnamectl set-hostname ovirt-engine.com

	~]# yum install https://resources.ovirt.org/pub/yum-repo/ovirt-release43.rpm
	
	~]# yum update

	~]# yum install ovirt-engine

	~]# engine-setup --accept-defaults
	
	~]# cat /etc/hosts
		192.168.5.40 ovirt-engine.com
		192.168.5.41 ovirt-node.com	
	
	setup成功后就可以通过浏览器访问engine的WEB管理台门户了，因为ovirt从4.x版本后默认通过域名访问了，所以要修改访问PC机器的hosts文件

	~]# systemctl enable ovirt-engine

###ovirt-node

	由于在一台物理机上的两个虚拟机进行测试，所以node节点需要开启二重虚拟化

	宿主机：
	~]# cat /etc/default/grub | grep GRUB_CMDLINE_LINUX			#在最后加上 kvm-intel.nested=1
		GRUB_CMDLINE_LINUX="crashkernel=auto rd.lvm.lv=centos/root rd.lvm.lv=centos/swap rhgb quiet kvm-intel.nested=1"
		
	~]# grub2-mkconfig -o /boot/grub2/grub.cfg		#更新grub

	~]# reboot   #重启服务器

	~]# cat /sys/module/kvm_intel/parameters/nested
		Y	

	~]# cat /etc/libvirt/qemu/ovirt-node.xml | grep "cpu mode"		#将mode修改为 host-passthrough
  		<cpu mode='host-passthrough' check='partial'>	

	#	<feature policy='require' name='vmx'/>  或是添加此行

	~]# virsh shutdown ovirt-node
	~]# virsh start ovirt-start

	
	虚拟机：
	~]# hostnamectl set-hostname ovirt-node.com

	~]# yum install https://resources.ovirt.org/pub/yum-repo/ovirt-release43.rpm
	
	~]# yum update


	
	