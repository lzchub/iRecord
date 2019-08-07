#1.二进制安装tomcat
##1.1 安装jdk

	~]# tar xf jdk-8u60-linux-x64.tar.gz -C /usr/local/
	~]# ln -s /usr/local/jdk1.8.0_60/ /usr/local/jdk
	~]# echo 'export JAVA_HOME=/usr/local/jdk' > /etc/profile.d/jdk.sh
	~]# echo 'export PATH=$JAVA_HOME/bin:$PATH' >> /etc/profile.d/jdk.sh
	~]# . /etc/profile.d/jdk.sh
	~]# java -version
	java version "1.8.0_60"
	Java(TM) SE Runtime Environment (build 1.8.0_60-b27)
	Java HotSpot(TM) 64-Bit Server VM (build 25.60-b23, mixed mode)

##1.2 安装tomcat

	~]# tar xf apache-tomcat-8.5.37.tar.gz -C /usr/local/
	~]# ln -s /usr/local/apache-tomcat-8.5.37/ /usr/local/tomcat 
	~]# echo "export CATALINA_HOME=/usr/local/tomcat" > /etc/profile.d/tomcat.sh
	~]# echo 'export PATH=$CATALINA_HOME/bin:$PATH' >> /etc/profile.d/tomcat.sh
	~]# . /etc/profile.d/tomcat.sh
	~]# version.sh
	Using CATALINA_BASE:   /usr/local/tomcat
	Using CATALINA_HOME:   /usr/local/tomcat
	Using CATALINA_TMPDIR: /usr/local/tomcat/temp
	Using JRE_HOME:        /usr/local/jdk
	Using CLASSPATH:       /usr/local/tomcat/bin/bootstrap.jar:/usr/local/tomcat/bin/tomcat-juli.jar
	Server version: Apache Tomcat/8.5.37
	Server built:   Dec 12 2018 12:07:02 UTC
	Server number:  8.5.37.0
	OS Name:        Linux
	OS Version:     3.10.0-862.el7.x86_64
	Architecture:   amd64
	JVM Version:    1.8.0_60-b27
	JVM Vendor:     Oracle Corporation

##1.3 yum安装tomcat
```
yum install tomcat-webapps tomcat-admin-webapps tomcat java-1.8.0-openjdk
```
#2.配置管理界面
server status:
manager app:
```
~]# vim /usr/local/tomcat/conf/tomcat-users.xml
<tomcat-users ...>
... 
  <role rolename="admin-gui"/>
  <role rolename="manager-gui"/>
  <user username="chuan" password="123456" roles="manager-gui,admin-gui"/>
</tomcat-users>

~]# vim /usr/local/tomcat/conf/Catalina/localhost/manager.xml
<?xml version="1.0" encoding="UTF-8"?>
<Context docBase="${catalina.home}/webapps/manager" 
        antiResourceLocking="false" privileged="true" >
  <Valve className="org.apache.catalina.valves.RemoteAddrValve"
         allow="^.*$" />
</Context>
```
host manager
```
~]# cp /usr/local/tomcat/conf/Catalina/localhost/manager.xml /usr/local/tomcat/conf/Catalina/localhost/host-manager.xml
~]# sed -i s/manager/host-manager/ /usr/local/tomcat/conf/Catalina/localhost/host-manager.xml
```
#3.虚拟主机
```
测试页：
	
~]# cat index.jsp 
	<%@ page language="java" %>
	<%@ page import="java.util.*" %>
	<html>
	  <body>
	    <% out.println("hello world! this is /usr/local/tomcat/chuan/xuexi dir"); %>
	  </body>
	</html>

添加host组件即可：

 	  <Host name="www.chuan1.com"  appBase="/www/chuan"
            unpackWARs="true" autoDeploy="true">
          <Context path="" docBase="/www/chuan" reloadable="true" />
          <Context path="/xuexi" docBase="xuexi" reloadable="true" />
        <Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
               prefix="longshuai_access_log" suffix=".txt"
               pattern="%h %l %u %t &quot;%r&quot; %s %b" />
      </Host>

      <Host name="www.chuan2.com"  appBase="webapps/chuan"
            unpackWARs="true" autoDeploy="true">
          <Context path="" docBase="" reloadable="true" />
          <Context path="/xuexi" docBase="xuexi" reloadable="true" />
        <Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
               prefix="xiaofang_access_log" suffix=".txt"
               pattern="%h %l %u %t &quot;%r&quot; %s %b" />
      </Host>

注：
	1.使用绝对路径则路径就为该路径，若使用相对路径，则前面要加上 $CATALINA_BASE 路径.
	2.若Host组件中未指定Context，则默认路径为APPBase/ROOT/目录。
```
#4.反代实现负载均衡
##4.1 模型一
![](./picture/4.png)
**nginx反代：**
```
	upstream tomcat_servers {
        server 192.168.179.111:8080 weight=1 max_fails=2 fail_timeout=2;
        server 192.168.179.113:8080 weight=2 max_fails=2 fail_timeout=2;
    }

    server {
        listen 80;
        server_name 192.168.179.110;

        location / {
            root /www/html;
            index index.html index.htm;
        }

        location ~* \.(jsp|jspx|do) {
            proxy_pass http://tomcat_servers;
        }
    }
```
**httpd反代：**
```
AJP协议：
	]# cat ajp.conf
	<VirtualHost 192.168.179.110:80>
	    serverName www.ilinux.io
	    DirectoryIndex index.html
	    DocumentRoot /www/html
	
		#<proxy balancer://TomcatLB>
        #	BalancerMember ajp://192.168.179.111:8009 loadfactor=5
        #	BalancerMember ajp://192.168.179.113:8009 loadfactor=10
    	#</Proxy>	

	    ProxyVia off
	    ProxyRequests off
	    ProxyPreserveHost off
	 
	    ProxyPassMatch "^/(.*\.jsp)$" ajp://192.168.179.111:8009/$1
	    ProxyPassReverse "^/(.*\.jsp)$" ajp://192.168.179.111:8009/$1
	
		#ProxyPassMatch "^/(.*\.jsp)$" balancer://TomcatLB/$1
    	#ProxyPassReverse "^/(.*\.jsp)$" balancer://TomcatLB/$1

	    <Directory /www/html>
	        AllowOverride None
	        Require all granted
	    </Directory>
	
	    <Proxy *>
	        Require all granted
	    </Proxy>
	</VirtualHost>
```
```
http协议：

	]# cat http.conf
	<VirtualHost 192.168.179.110:80>
	    serverName www.ilinux.io
	    DirectoryIndex index.html
	    DocumentRoot /www/html
	
	    ProxyVia off
	    ProxyRequests off
	    ProxyPreserveHost off
	 
	    ProxyPassMatch "^/(.*\.jsp)$" http://192.168.179.111:8080/$1
	    ProxyPassReverse "^/(.*\.jsp)$" http://192.168.179.111:8080/$1
	
	    <Directory /www/html>
	        AllowOverride None
	        Require all granted
	    </Directory>
	
	    <Proxy *>
	        Require all granted
	    </Proxy>
	</VirtualHost>
```

##4.2 模型二
![](./picture/5.png)