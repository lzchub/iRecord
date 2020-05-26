# SSR 问题处理

###1.GWF是什么?

	GWF的全称是中国长城防火墙(英文名称Great Firewall of China)，其首要设计者是被称为“国家防火墙之父”北京邮电大学原校长方滨兴。有些人天天喊着要翻墙，咱们也经常说“我的域名被墙了”，这些“墙”就是中国长城防火墙。

	GWF是中国对互联网信息内容中含政治议论、色情、重要人物名讳、邪教传播等不符合国家法律法规或在法律法规之外任何有损国家正常发展的敏感内容的一种自动审查与过滤，由计算机和网络设备等硬件组成的监控系统。GWF对互联网信息审查、监控、过滤主要采取以下4种技术：

	1)、国家入口网关的IP封锁，通过封锁IP地址来防止被过滤网站内容被用户搜索和访问到;

	2)、过滤阻断主干路由器关键字，这中国实现关键字过滤得益于路由器设备生产商的帮助，其中以思科公司为首，中国路由器占八成都是思科公司生产的;

	3)、劫持网站域名，主要是用路由器提供的IDS系统监测劫持域名，阻止用户的进一步搜索和访问;

	4)、HTTPS证书过滤，简单地说是对服务器证书进行过滤;

	综合而言，凡是被封锁的网站究其根本原因就是在网站上发布了咱们政府能容忍范围之外的内容，或者是受这些封锁网站的牵连。

###2.Chrome插件安装时程序包无效:"CRX_HEADER_INVALID"

	1. 打开chorme的扩展程序（设置——>更多工具——>扩展程序），选择开发者模式
	2. 将插件文件 .crx 后缀改为 .rar 
	3. 解压文件，进行安装

# SSR 服务器

	IP：161.117.249.204
	用户：root
	密码：kxsw.517na.com

# SSR 操作

	~]# ./ssr.sh 		#家目录下有操作脚本
		ShadowsocksR 一键管理脚本 [v2.0.38]
	  	---- Toyo | doub.io/ss-jc42 ----
	
	  	1. 安装 ShadowsocksR
	  	2. 更新 ShadowsocksR
	  	3. 卸载 ShadowsocksR
	  	4. 安装 libsodium(chacha20)
		————————————
	  	5. 查看 账号信息
	  	6. 显示 连接信息
	  	7. 设置 用户配置
	  	8. 手动 修改配置
	  	9. 切换 端口模式
		————————————
	 	10. 启动 ShadowsocksR
	 	11. 停止 ShadowsocksR
	 	12. 重启 ShadowsocksR
	 	13. 查看 ShadowsocksR 日志
		————————————
	 	14. 其他功能
	 	15. 升级脚本
	 
	 	当前状态: 已安装 并 已启动
	 	当前模式: 单端口
	
		请输入数字 [1-15]：