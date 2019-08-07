	<li>实验系统 CentOS 7 </li>
	<li>自动化安装系统 CentOS 7 </li>

若实验机未关闭SELinux，需先关闭SELinux
<pre>vim /etc/sysconfig/selinux
将SELINUX 修改为disabled 保存重启</pre>

<strong>1. 更新源</strong>
<pre>rpm -ivh http://mirrors.aliyun.com/epel/epel-release-latest-7.noarch.rpm</pre>
<strong>2. 下载需要的服务</strong>
<pre>yum install -y httpd dhcp tftp cobbler cobbler-web pykickstart xinetd</pre>
<strong>3. 开启httpd和cobblerd服务，关闭防火墙</strong>
<pre>systemctl start httpd
systemctl start cobblerd
systemctl stop firewall</pre>
<strong>4. cobbler check 可以查看步骤</strong>
<pre>The following are potential configuration items that you may want to fix:
1 : The 'server' field in /etc/cobbler/settings must be set to something other than localhost, or kickstarting features will not work.  This should be a resolvable hostname or IP for the boot server as reachable by all machines that will use it.
<code>vim /etc/cobbler/settings
384:server=192.168.179.132 (自己主机ip)</code>
2 : For PXE to be functional, the 'next_server' field in /etc/cobbler/settings must be set to something other than 127.0.0.1, and should match the IP of the boot server on the PXE network.
<code>272:next_server=192.168.179.132 (修改为自己主机ip，保存退出)</code>
3 : change 'disable' to 'no' in /etc/xinetd.d/tftp
<code>vim /etc/xinetd.d/tftp
将 disable = no 保存退出</code>
4 : Some network boot-loaders are missing from /var/lib/cobbler/loaders, you may run 'cobbler get-loaders' to download them, or, if you only want to handle x86/x86_64 netbooting, you may ensure that you have installed a *recent* version of the syslinux package installed and can ignore this message entirely.  Files in this directory, should you want to support all architectures, should include pxelinux.0, menu.c32, elilo.efi, and yaboot. The 'cobbler get-loaders' command is the easiest way to resolve these requirements.
<code>cobbler get-loaders</code>
5 : enable and start rsyncd.service with systemctl
<code>systemctl start rsyncd.service</code>
6 : debmirror package is not installed, it will be required to manage debian deployments and repositories
<code>安装centos系统略过此步骤</code>
7 : The default password used by the sample templates for newly installed machines (default_password_crypted in /etc/cobbler/settings) is still set to 'cobbler' and should be changed, try: "openssl passwd -1 -salt 'random-phrase-here' 'your-password-here'" to generate new one
<code>openssl passwd -1 -salt 'cobbler' 'cobbler'   生成密码，单引号中的内容可自己指定，这里使用cobbler
vim /etc/cobbler/settings
default_password_crypted="生成的密码"
</code>
8 : fencing tools were not found, and are required to use the (optional) power management features. install cman or fence-agents to use them
<code>虚拟机安装略过此步骤</code>
Restart cobblerd and then run 'cobbler sync' to apply changes.</pre>
<strong>5. dhcp配置</strong>
<pre>dhcp可单独配置，这儿推荐用cobbler管理dhcp服务
vim /etc/cobbler/dhcp.template   修改红框部分
<img src="http://39.108.135.113/wordpress/wp-content/uploads/2018/07/捕获-2.png" alt="" width="781" height="155" class="alignnone size-full wp-image-141" />
vim /etc/cobbler/settings
将 manage_dhcp=1 保存退出
systemctl restart cobblerd.service 重启服务
systemctl start xinetd</pre>
<strong>6. 镜像制作</strong>
查看是否挂载镜像，没挂载的需要挂载
<pre>mount /dev/cdrom /mnt
cobbler import --path=/mnt/ --name=CentOS-7-x86_64 --arch=x86_64
(镜像导入文件在 /var/www/cobbler/ks_mirror)
 cd /var/lib/cobbler/kickstarts/   
#将CentOS-7-x86_64.cfg放在该目录,文件如下
<code>#Kickstart Configurator for cobbler by Jason Zhao
#platform=x86,AMD64,or Intel EM64T
#System language
lang en_US
#System keyboard
keyboard us
#System timezone
timezone Asia/Shanghai
#Root password
rootpw --iscrypted $default_password_crypted
#Use text mode install
text
#Install OS instead of upgrade
install
#Use NFS installation Media
url --url=$tree
#System bootloader configuration
bootloader --location=mbr
#Clear the Master Boot Record
zerombr
#Partition clearing information
clearpart --all --initlabel
#Disk partitioning information
part /boot --fstype xfs --size 1024 --ondisk sda
part swap --size 16384 --ondisk sda
part / --fstype xfs --size 1 --grow --ondisk sda
#System authorization information
auth --useshadow --enablemd5
#Network information
$SNIPPET('network_config')
#network --bootproto=dhcp --device=em1 --onboot=on
#Reboot after installation
reboot
#Firewall configuration
firewall --disabled
#SELinux configuration
selinux --disabled
#Do not configure XWindows
skipx
#Package install information
%pre
$SNIPPET('log_ks_pre')
$SNIPPET('kickstart_start')
$SNIPPET('pre_install_network_config')
#Enable installation monitoring
$SNIPPET('pre_anamon')
%end

%packages
@ base
@ core
sysstat
iptraf
ntp
lrzsz
ncurses-devel
openssl-devel
zlib-devel
OpenIPMI-tools
mysql
nmap
screen
%end

%post
systemctl disable postfix.service
%end</code>
cobbler profile edit --name=CentOS-7-x86_64 --kickstart=/var/lib/cobbler/kickstarts/CentOS-7-x86_64.cfg  #自定义kickstart文件
cobbler profile edit --name=CentOS-7-x86_64 --kopts='net.ifnames=0 biosdevname=0'  #修改内核参数，使新装机网卡名为eth0
cobbler sync</pre>

<strong>当以上步骤完成时，即可自动化安装系统啦！！</strong>
最终完成图:
<img src="http://39.108.135.113/wordpress/wp-content/uploads/2018/07/1-1.png" alt="" width="753" height="454" class="alignnone size-full wp-image-139" />

<strong>*新装机指定</strong>
<pre>IP:192.168.10.10
主机名:linux-node1
掩码:255.255.255.0
网关:192.168.10.1
DNS:192.168.10.1
<code>cobbler system add --name=linux-node1 --mac=00:50:56:31:6C:DF --prefile=CentOS-7-x86_64 --ip-address=192.168.10.10 --subnet=255.255.255.0 --gateway=192.168.10.1 --interface=eth0 --static=1 --hostname=linux-node1 --name-servers="192.168.10.10" --kickstart=/var/lib/cobbler/kickstarts/CentOS-7-x86_64.cfg</code>
<code>cobbler sync</code></pre>
*yum install lrzsz 可跨系统传文件