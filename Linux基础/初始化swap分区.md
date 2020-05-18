#创建Swap分区

```
	~]# dd if=/dev/zero of=/swap bs=1024 count=8192000

	~]# mkswap /swap
	~]# swapon /swap

	~]# echo "/swap swap swap defaults 0 0" >> /etc/fstab
```