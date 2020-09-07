	net.ipv4.tcp_syn_retries = 5
	net.ipv4.tcp_synack_retries = 5
	net.ipv4.tcp_keepalive_time = 900
	net.ipv4.tcp_keepalive_probes = 9
	net.ipv4.tcp_fin_timeout = 60
	net.ipv4.tcp_ip_local_port_range = 32768 65500
	net.core.rmem_default = 262144
	net.core.rmem_max = 4194304
	net.core.wmem_default = 262144
	net.core.wmem_max = 1048576
	kernel.sem = 1024 32000 100 256
	kernel.core_uses_pid = 1
	kernel.shmmni = 4096
	fs.file-max = 6815744
	net.ipv4.ip_forward = 1
	net.ipv4.tcp_max_orphans = 131072
	net.ipv4.tcp_retries2 = 7
	vm.max_map_count = 262144
	vm.dirty_background_ratio = 10
	vm.dirty_ratio = 5
	net.netfilter.nf_conntrack_max = 524288
	net.bridge.bridge-nf-call-iptables = 1
	net.bridge.bridge-nf-call-ip6tables = 1
	kernel.core_pattern = core-%e-%p-%t
	#vm_min_free_kbytes = 131072
```c
net.ipv4.ip_forward = 0
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.default.accept_source_route = 0
kernel.sysrq = 0
kernel.core_uses_pid = 1
net.ipv4.tcp_syncookies = 1
kernel.msgmnb = 65536
kernel.msgmax = 65536
kernel.shmmax = 68719476736
kernel.shmall = 4294967296
net.ipv4.tcp_max_tw_buckets = 120000
net.ipv4.tcp_sack = 1
net.ipv4.tcp_window_scaling = 1
net.ipv4.tcp_rmem = 4096 87380 4194304
net.ipv4.tcp_wmem = 4096 16384 4194304
net.core.wmem_default = 8388608
net.core.rmem_default = 8388608
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.core.netdev_max_backlog = 262144
net.core.somaxconn = 262144
net.ipv4.tcp_max_orphans = 3276800
net.ipv4.tcp_max_syn_backlog = 262144
net.ipv4.tcp_timestamps = 0
net.ipv4.tcp_synack_retries = 1
net.ipv4.tcp_syn_retries = 1
net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_mem = 94500000 915000000 927000000
net.ipv4.tcp_fin_timeout = 1
net.ipv4.tcp_keepalive_time = 1200
net.ipv4.ip_local_port_range = 1024 65535

net.nf_conntrack_max = 1048576
net.netfilter.nf_conntrack_max = 1048576

#net.netfilter.nf_conntrack_tcp_timeout_established = 120
#net.netfilter.nf_conntrack_tcp_timeout_established = 180
#net.netfilter.nf_conntrack_tcp_timeout_established = 1200
net.netfilter.nf_conntrack_tcp_timeout_established = 7200

net.netfilter.nf_conntrack_tcp_timeout_time_wait = 120
net.netfilter.nf_conntrack_tcp_timeout_close_wait = 60
net.netfilter.nf_conntrack_tcp_timeout_fin_wait = 120

net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
```

