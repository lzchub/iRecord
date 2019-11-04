#1.安装kubernetes集群

实验环境：centos7.6
	
	master:	192.168.65.52
	node1:	192.168.65.53
	node2:	192.168.65.54
	node3:	192.168.65.55

前提：

	1.借助NTP服务器设置各节点时间精确同步
		centos7有自动同步时间服务 chronyd，可自己设置时间服务器，/etc/chrony.conf 重启服务等待同步

	2.通过DNS完成各节点主机名解析，测试可写hosts文件

	3.关闭各节点防火墙，关闭selinux

	4.各节点禁用所有Swap设备
		~]# swapoff -a		#临时关闭所有swap设备,永久关闭修改/etc/fstab

	5.若要使用ipvs模型的proxy，各节点还需要载入ipvs相关的各模块
		~]# cat /etc/sysconfig/modules/ipvs.modules
			#!/bin/bash
			
			ipvs_mods_dir="/usr/lib/modules/$(uname -r)/kernel/net/netfilter/ipvs"
			for mod in $(ls $ipvs_mods_dir | grep -o "^[^.]*");do
			        /sbin/modinfo -F filename $mod &> /dev/null
			        if [ $? -eq 0 ];then
			                /sbin/modprobe $mod
			        fi
			done

		~]# chmod a+x /etc/sysconfig/modules/ipvs.modules
		~]# bash /etc/sysconfig/modules/ipvs.modules	#手动加载进内核
		~]# lsmod | grep ip_vs		#查看内核模块是否加载

初始化master：

	注：CPU至少2核

	~]# wget https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo -P /etc/yum.repos.d/

	选择docker版本：
	~]# yum list docker-ce --showduplicates
	~]# yum install -y docker-ce

	#~]# yum install -y --setopt=obsoletes=0 docker-ce-18.06.1.ce-3.el7

	~]# vim /usr/lib/systemd/system/docker.service
		...
		ExecStartPost=/usr/sbin/iptables -P FORWARD ACCEPT		#添加此行
		...

	~]# systemctl daemon-reload 

	~]# cat /etc/yum.repos.d/kubernetes.repo 
		[kubernetes]
		name=kubernetes repo
		baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
		gpgcheck=1
		gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
			   https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
		enabled=1

	#~]# rpm --import yum-key.gpg 

	~]# yum install kubelet kubeadm kubectl -y

	注：
		kubeadm：是Kubernetes官方提供的用于快速安装Kubernetes集群的工具，伴随Kubernetes每个版本的发布都会同步更新，kubeadm会对集群配置方面的一些实践做调整，通过实验kubeadm可以学习到Kubernetes官方在集群配置上一些新的最佳实践。
		
		kubelet：是运行于集群中每个节点上的kubernetes dialing程序，它的核心功能在于通过API Server获取调度至自身运行的Pod资源的PodSpec并依之运行Pod。事实上，以自托管方式部署的Kubernetes集群，除了kubelet和Docker之外的所有组件均以Pod对象的形式运行。

		kubectl: 操作集群的命令行工具。通过 kubectl 可以部署和管理应用，查看各种资源，创建、删除和更新各种组件。

	~]# systemctl start docker
	#不能先启动kubelet，否则会报错
	
	~]# systemctl enable kubelet docker

	注：
		若不关闭交换分区
		修改内核参数：
			~]# cat /proc/sys/vm/swappiness
			~]# vim /etc/sysctl.d/k8s.conf
				vm.swappiness=0				#swappiness=0的时候表示最大限度使用物理内存，然后才是 swap空间，swappiness＝100的时候表示积极的使用swap分区，并且把内存上的数据及时的搬运到swap空间里面。
			~]# sysctl -p /etc/sysctl.d/k8s.conf

		允许跳过此错误：
			~]# cat /etc/sysconfig/kubelet
				KUBELET_EXTRA_ARGS="--fail-swap-on=false"


	查看初始化配置：
		~]# kubeadm config print init-defaults
			apiVersion: kubeadm.k8s.io/v1beta2
			bootstrapTokens:
			- groups:
			  - system:bootstrappers:kubeadm:default-node-token
			  token: abcdef.0123456789abcdef
			  ttl: 24h0m0s
			  usages:
			  - signing
			  - authentication
			kind: InitConfiguration
			localAPIEndpoint:
			  advertiseAddress: 1.2.3.4
			  bindPort: 6443
			nodeRegistration:
			  criSocket: /var/run/dockershim.sock
			  name: master-k8s
			  taints:
			  - effect: NoSchedule
			    key: node-role.kubernetes.io/master
			---
			apiServer:
			  timeoutForControlPlane: 4m0s
			apiVersion: kubeadm.k8s.io/v1beta2
			certificatesDir: /etc/kubernetes/pki
			clusterName: kubernetes
			controllerManager: {}
			dns:
			  type: CoreDNS
			etcd:
			  local:
			    dataDir: /var/lib/etcd
			imageRepository: k8s.gcr.io
			kind: ClusterConfiguration
			kubernetesVersion: v1.16.0
			networking:
			  dnsDomain: cluster.local
			  serviceSubnet: 10.96.0.0/12
			scheduler: {}


	初始化master节点方法：
	1.命令初始化
	2.配置文件初始化，同上 yml格式，使用init --config指定配置文件

	~]# echo "1" >/proc/sys/net/bridge/bridge-nf-call-iptables

	~]# kubeadm init --kubernetes-version=v1.16.1		#正在使用的k8s程序组件的版本号，需要与kubelet的版本号相同。 
		--pod-network-cidr=10.244.0.0/16 				#pod的网络地址，使用flannel插件时，默认是10.244.0.0/16
		--service-cidr=10.96.0.0/12 					#service的网络地址，默认地址为10.96.0.0/12
		--image-repository registry.aliyuncs.com/google_containers 	#默认仓库的gcr.io，国内无法访问，显示定义仓库地址
		#--ignore-preflight-errors=Swap					#忽略 swap分区未关闭的错误
		#apiserver-advertise-address=192.168.179.50		#apiserver通告给其他组件的IP地址，一般为该节点的地址，0.0.0.0表示节点上所有的可用地址
		...
		[addons] Applied essential addon: CoreDNS
		[addons] Applied essential addon: kube-proxy
		
		Your Kubernetes master has initialized successfully!
		
		To start using your cluster, you need to run the following as a regular user:
		
		  mkdir -p $HOME/.kube
		  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
		  sudo chown $(id -u):$(id -g) $HOME/.kube/config
		
		...
		
		kubeadm join 192.168.179.50:6443 --token z95afq.1lolsqdcy2gi4py2 --discovery-token-ca-cert-hash sha256:2c4a029e1816adf4ac438a9fb02e97d134f59f9c4c9b1457f639744f59cd7ff7

	#使用的root用户，建议使用普通用户
	~]# mkdir -p $HOME/.kube
	~]# cp -i /etc/kubernetes/admin.conf $HOME/.kube/config

	~]# kubectl get componentstatus	#查看集群状态信息
	~]# kubectl get cs
	~]# kubectl get nodes #查看节点信息

	安装flannel网络插件:

	~]# kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml		#访问不了quay.io需要修改镜像仓库

	~]# kubectl get ns #名称空间
	~]# kubectl get pods -n kube-system

	ingress-nginx:
		kubectl apply -f mandatory.yaml
		kubectl apply -f service-nodeport.yaml

nodes：
	
	~]# wget https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo -P /etc/yum.repos.d/

	~]# cat /etc/yum.repos.d/kubernetes.repo 
	[kubernetes]
	name=kubernetes repo
	baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
	gpgcheck=1
	gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
		   https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
	enabled=1

	#~]# rpm --import yum-key.gpg 

	~]# yum install kubelet kubeadm docker-ce -y

	~]# systemctl start docker
	~]# systemctl enable kubelet docker

	~]# cat /etc/sysconfig/kubelet		#关闭swap略过此步骤
		KUBELET_EXTRA_ARGS="--fail-swap-on=false"

	~]# kubeadm join 192.168.179.110:6443 --token 3s2fm9.xrtqmqwr4cvoxslk --discovery-token-ca-cert-hash sha256:019da38db9a6b0104d1528a8f7418f5e374b8f9d459b73bd832f58d261d16ab8 --ignore-preflight-errors=Swap

	master:
		~]# kubectl get nodes

	注:每个节点都要导入flannel镜像。


	注：忘记taken或者taken过期
	
	1.生成一条永久有效的token

		~]# kubeadm token create --ttl 0
	
		~]# kubeadm token list
			TOKEN                     TTL         EXPIRES                     USAGES                   DESCRIPTION   EXTRA GROUPS
			dxnj79.rnj561a137ri76ym   <invalid>   2018-11-02T14:06:43+08:00   authentication,signing   <none>        system:bootstrappers:kubeadm:default-node-token
			o4avtg.65ji6b778nyacw68   <forever>   <never>                     authentication,signing   <none>        system:bootstrappers:kubeadm:default-node-token

 
	2.获取ca证书sha256编码hash值
		~]# openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'
			2cc3029123db737f234186636330e87b5510c173c669f513a9c0e0da395515b0
 

	3.node节点加入

		~]# kubeadm join 192.168.65.52:6443 --token o4avtg.65ji6b778nyacw68 --discovery-token-ca-cert-hash sha256:2cc3029123db737f234186636330e87b5510c173c669f513a9c0e0da395515b0

##1.2 镜像加速
	~]# cat /etc/docker/daemon.json 
	{
	        "registry-mirrors":["https://registry.docker-cn.com"]
	}

#2.基本操作

	1.查询集群环境相关信息：
		~]# kubectl version [--short=true]
		~]# kubectl cluster-info

	2.查询资源对象：
		~]# kubectl get [pods|deployment|replicaset|service(svc)|namespace(ns)|nodes] [-o wide] [-n kube-system] [--show-labels|-l] [-w]	#查看命名空间[pod|svc]

	3.打印资源对象的详细信息：
		~]# kubectl describe [pods|svc|ns|nodes] NAME	#查看详细信息
		~]# kubectl get pods -l component=kube-apiserver -o yaml -n kube-system	#将标签为com...的pod资源信息以yaml格式输出
		~]# kubectl get pods etcd-k8s-master -o json -n kube-system				#将pod资源信息以json格式输出

	4.打印容器日志信息：
		~]# kubectl logs [-f] etcd-k8s-master -n kube-system

	5.在容器中执行命令：
		~]# kubectl exec -it POD_NAME -- /bin/sh	#进入容器
		~]# kubectl exec POD_NAME -- CMD	#执行命令
	
	6.删除资源
		~]# kubectl delete ([-f FILENAME] | TYPE [(NAME | -l label | --all)]) [options]
		
	7.创建资源
		~]# kubectl run nginx-deploy --image=nginx:1.14-alpine --port=80 --replicas=1		#启动pod

		~]# kubectl expose deployment/nginx-deploy --port=80 --protocol=TCP --name=nginx	#创建service
	
	8.扩缩容、滚动更新
		~]# kubectl scale --replicas=4 deployment myapp	#动态更改pod数量
		~]# kubectl set image deployment myapp myapp=ikubernetes/myapp:v2	#动态更新版本
	
	9.回退
		~]# kubectl rollout status deployment myapp	#查看更新版本信息
		~]# kubectl rollout undo deployment myapp 	#回滚
	
	10.资源查询对象清单
		~]# kubectl explain RESOURCE [options] 	#查看各种资源信息

	
	11.标签操作
		~]# kubectl label pod pod-test ver=stable			#动态打标
		~]# kubectl label -f pod-resources.yaml ver=stable	
		~]# kubectl get pod -l ver=stable

	12.通过资源清单创建资源对象
		~]# kubectl apply -f SOURCE_NAME.yaml	#可多次使用
		~]# kubectl create -f SOURCE_NAME.yaml
	
	13.临时动态编辑资源对象，而不用修改资源清单
		~]# kubectl edit (RESOURCE/NAME | -f FILENAME) [options]

	注：service，pod 地址都只能K8S集群内访问

##2.1 DNS服务	
 
	~]# yum install -y bind-utils
	~]# kubectl get svc -n kube-system
	NAME       TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)         AGE
	kube-dns   ClusterIP   10.96.0.10   <none>        53/UDP,53/TCP   20h

    ~]# dig A nginx @10.96.0.10
	~]# dig A nginx.default.svc.cluster.local @10.96.0.10

##2.2 动态扩缩容

	~]# kubectl get pods -l app=myapp -w	#动态更新信息

	~]# kubectl set image deployment deployment-myapp myapp=ikubernetes/myapp:v2	#升级镜像版本，默认滚动升级
	~]# kubectl patch deployment deployment-myapp -p {"spec":{"replicas":5}}	#扩缩容pod数量
	~]# kubectl rollout undo deployment deployment-myapp	#回退一个版本，可指定多个
	~]# kubectl set image deployment deployment-myapp myapp=ikubernetes/myapp:v2 && kubectl rollout pause deployment deployment-myapp	#更新一个pod后暂停更新，金丝雀发布
	~]# kubectl rollout resume deployment deployment-myapp	#继续执行
	~]# kubectl patch deployment deployment-myapp -p '{"spec":{"strategy":{"rollingUpdate":{"maxSurge":1,"maxUnavailable":0}}}}'	#更改更新参数

	~]# curl http://localhost:8080/api/v1/namespaces/default/services/myapp-svc
	~]# curl http://localhost:8080/apis/apps/v1/namespaces/default/deployments/myapp-deploy

## Ingress-nginx安装配置


	service的nodeport只能实现基于端口的tcp四层代理，ingress可实现基于http/https的七层代理
	常用反向代理：
		nginx、envoy、vulcand、haproxy、traefik
	
		GitHub地址：https://github.com/kubernetes/ingress-nginx/tree/master/deploy
	
	1.一键部署
	~]# wget https://github.com/kubernetes/ingress-nginx/blob/master/deploy/mandatory.yaml
		修改镜像拉取地址：registry.cn-hangzhou.aliyuncs.com/quay-image/nginx-ingress-controller:0.22.0
	
	~]# kubectl apply -f mandatory.yaml
	~]# kubectl get pod POD_NAME -n ingress-nginx
	
	2.暴露服务
	~]# kubectl apply -f service-nodeport.yaml


	k8s:1.16.2
	https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/mandatory.yaml

## Dashboard搭建

	github地址：https://github.com/kubernetes/dashboard
	
	1.获取资源清单
		~]# wget https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml
	
	2.修改镜像拉取地址，暴露服务(使用nodeport暴露服务)
	
	  修改镜像拉取地址（若需要其他版本，可到阿里云（https://cr.console.aliyun.com/）或其他可访问到的仓库查找）：
	  registry.cn-hangzhou.aliyuncs.com/quay-image/kubernetes-dashboard:v1.10.1	
	
	  service中暴露端口：
			spec:
	  		  type: NodePort
	  	 	  ports:
	   		  - port: 443
	      		targetPort: 8443
	      		nodePort: 30888
	3.访问
	
		注意使用的是https，访问时需要为 https://IP:PORT，高版本google可能无法访问，可使用firefox或其他浏览器
	
	4.认证
		支持 kubeconfig 和 令牌 认证，我这儿使用令牌认证
		绑定管理员角色：
			~]# kubectl apply -f clusterrolebinding-dashboard.yaml
		得到令牌：
			~]# kubectl describe secret -n kube-system `kubectl get secret -n kube-system | grep dashboard-admin | awk '{print $1}'`
	
	5.得到token输入即可登录


##部署canal提供网络策略功能

	flannel插件提供了pod网络，但是没提供网络策略功能，需要借助calico来实现网络策略，而且官网也说了可以flannel+calico一起使用。
	官网地址：https://docs.projectcalico.org/v3.5/getting-started/kubernetes/installation/flannel
	
	~]# wget https://docs.projectcalico.org/v3.5/getting-started/kubernetes/installation/hosted/canal/canal.yaml
	修改镜像拉取地址后直接部署即可
	~]# kubectl apply -f canal.yamld

	
	~]# kube-apiversions
	admissionregistration.k8s.io/v1beta1
	apiextensions.k8s.io/v1beta1
	apiregistration.k8s.io/v1
	apiregistration.k8s.io/v1beta1
	apps/v1
	apps/v1beta1
	apps/v1beta2
	authentication.k8s.io/v1
	authentication.k8s.io/v1beta1
	authorization.k8s.io/v1
	authorization.k8s.io/v1beta1
	autoscaling/v1
	autoscaling/v2beta1
	autoscaling/v2beta2
	batch/v1
	batch/v1beta1
	certificates.k8s.io/v1beta1
	coordination.k8s.io/v1beta1
	crd.projectcalico.org/v1
	events.k8s.io/v1beta1
	extensions/v1beta1
	metrics.k8s.io/v1beta1
	networking.k8s.io/v1
	policy/v1beta1
	rbac.authorization.k8s.io/v1
	rbac.authorization.k8s.io/v1beta1
	scheduling.k8s.io/v1beta1
	storage.k8s.io/v1
	storage.k8s.io/v1beta1
	v1



	for file in aggregated-metrics-reader.yaml auth-delegator.yaml auth-reader.yaml metrics-apiservice.yaml metrics-server-deployment.yaml metrics-server-service.yaml resource-reader.yaml;do wget https://raw.githubusercontent.com/kubernetes-incubator/metrics-server/master/deploy/1.8%2B/$file;done

	 containers:
	      - name: metrics-server
	        image: registry.cn-hangzhou.aliyuncs.com/chucai/metrics-server-amd64:v0.3.1
	        command:
	        - /metrics-server
	        - --metric-resolution=30s
	        - --kubelet-insecure-tls
	        - --kubelet-preferred-address-types=InternalIP,Hostname,InternalDNS,ExternalDNS,ExternalIP
	        imagePullPolicy: IfNotPresent

kubernetes资源：

	一切皆为资源

	集群级别资源：
		node
		namespace
		pv

	名称空间级资源：
		

pod接入流量方法：
	
	service：nodeport
	hostpod
	hostnetwork

Pod安全级别：

	pod.spec.secrutiyContext
	pod.spec.containers.[].secruityContext
		capabilities

容器资源需求及资源限制

	CPU属于可压缩型资源，即资源额度可按需收缩，而内存则时不可压缩资源，对其执行收缩操作可能会导致某种程度的问题
	CPU资源的计量方式：一个核心相当于1000个微核心，即1=1000m,0.5=500m
	内存资源的计量方式：默认单位为字节，也可以使用E、P、T、G、M和K后缀单位，或Ei、Pi、Ti、Gi、Mi和Ki后缀形式的单位后缀

Pod服务质量类别：
	
	根据Pod对象的requests和limits属性，Kubernetes把Pod对象归类到BestEffort、Burstable、Guaranteed三个服务质量类别
	Guaranteed：每个容器都为CPU资源设置了具有相同值的requests和limits属性，以及每个容器都为内存资源设置了具有相同值的requests和limits属性的pod资源会自动归属此类别，这类pod资源具有最高优先级
	Burstable：至少有一个容器设置了CPU或内存资源的requests属性，但不满足Guaranteed类别要求的pod资源自动归属此类别，它们具有中等优先级
	BestEffort：未为任何一个容器设置requests或limits属性的pod资源自动归属此类别，它们的优先级为最低级别

开启IPVS规则（每个节点都需要）：

	~]# cat /etc/sysconfig/modules/ipvs.modules 
	#!/bin/bash
	
	ipvs_mods_dir="/usr/lib/modules/$(uname -r)/kernel/net/netfilter/ipvs"
	for mod in $(ls $ipvs_mods_dir | grep -o "^[^.]*");do
	        /sbin/modinfo -F filename $mod &> /dev/null
	        if [ $? -eq 0 ];then
	                /sbin/modprobe $mod
	        fi
	done

	~]# chmod a+x ipvs.modules
	~]# bash ipvs.modules
	~]# lsmod | grep ip_vs
		ip_vs_wrr              12697  0 
		ip_vs_wlc              12519  0 
		ip_vs_sh               12688  0 
		ip_vs_sed              12519  0 
		ip_vs_rr               12600  0 
		ip_vs_pe_sip           12740  0 
		nf_conntrack_sip       33780  1 ip_vs_pe_sip
		ip_vs_nq               12516  0 
		ip_vs_lc               12516  0 
		ip_vs_lblcr            12922  0 
		ip_vs_lblc             12819  0 
		ip_vs_ftp              13079  0 
		ip_vs_dh               12688  0 
		ip_vs                 145497  26 ip_vs_dh,ip_vs_lc,ip_vs_nq,ip_vs_rr,ip_vs_sh,ip_vs_ftp,ip_vs_sed,ip_vs_wlc,ip_vs_wrr,ip_vs_pe_sip,ip_vs_lblcr,ip_vs_lblc
		nf_nat                 26583  5 ip_vs_ftp,nf_nat_ipv4,nf_nat_ipv6,xt_nat,nf_nat_masquerade_ipv4
		nf_conntrack          139224  10 ip_vs,nf_nat,nf_nat_ipv4,nf_nat_ipv6,xt_conntrack,nf_nat_masquerade_ipv4,nf_conntrack_netlink,nf_conntrack_sip,nf_conntrack_ipv4,nf_conntrack_ipv6
		libcrc32c              12644  4 xfs,ip_vs,nf_nat,nf_conntrack

配置容器化应用的方式

	1.自定义命令行参数：arg
	
	2.把配置文件写入镜像

	3.环境变量：
		(1) Cloud Native的应用程序一般可直接通过环境变量加载配置
		(2) 通过entrypoint脚本来预处理变量为配置文件中的配置信息

	4.存储卷
		configmap：
			1.通过命令创建，引用key/value键值对创建，然后在资源文件中进行引用，云原生服务支持通过环境变量定义配置
			2.通过命令创建，引用文件创建，然后在资源文件中进行引用，修改文件后，会在容器中配置自动重载，但服务还是不会重载

		secret：与configmap操作类似
		
		secret解码：
			~]# kubectl get secret SECRET_NAME -o yaml		#拿到加密后的数据
			~]# echo DATA | base64 -d	即可解码
