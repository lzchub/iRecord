#1.搭建kubernetes集群

实验环境：centos7.6
	
	master:	192.168.5.30
	node1:	192.168.5.31
	node2:	192.168.5.32
	node3:	192.168.5.33

###前提：

	1.借助NTP服务器设置各节点时间精确同步
		centos7有自动同步时间服务 chronyd，可自己设置时间服务器，/etc/chrony.conf 重启服务等待同步

	2.通过DNS完成各节点主机名解析，测试可写hosts文件

	3.关闭各节点防火墙，关闭selinux
		~]# systemctl stop firewalld
		~]# systemctl disable firewalld
	
		~]# setenforce 0
		~]# sed -i 's/SELINUX=enable/SELINUX=disabled/g' /etc/sysconfig/selinux

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

###初始化master：

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

	~]# yum install kubelet-1.15.7 kubeadm-1.15.7 kubectl-1.15.7 -y

	注：
		kubeadm：是Kubernetes官方提供的用于快速安装Kubernetes集群的工具，伴随Kubernetes每个版本的发布都会同步更新，kubeadm会对集群配置方面的一些实践做调整，通过实验kubeadm可以学习到Kubernetes官方在集群配置上一些新的最佳实践。
		
		kubelet：是运行于集群中每个节点上的kubernetes dialing程序，它的核心功能在于通过API Server获取调度至自身运行的Pod资源的PodSpec并依之运行Pod。事实上，以自托管方式部署的Kubernetes集群，除了kubelet和Docker之外的所有组件均以Pod对象的形式运行。

		kubectl: 操作集群的命令行工具。通过 kubectl 可以部署和管理应用，查看各种资源，创建、删除和更新各种组件。


	~]# mkdir /etc/docker			#启动镜像加速

	~]# vim /etc/docker/daemon.json
		{
	 		"registry-mirrors": ["https://nqq67ahg.mirror.aliyuncs.com"]
		}

	~]# systemctl daemon-reload
	~]# systemctl start docker 			#不能先启动kubelet，否则会报错
	
	~]# systemctl enable kubelet docker

	~]# echo "1" >/proc/sys/net/bridge/bridge-nf-call-iptables	#不设为1在启动容器时会报错	

	~]# kubeadm init --kubernetes-version=v1.15.7		#正在使用的k8s程序组件的版本号，需要与kubelet的版本号相同。 
		--pod-network-cidr=10.244.0.0/16 				#pod的网络地址，使用flannel插件时，默认是10.244.0.0/16
		--service-cidr=10.96.0.0/12 						#service的网络地址，默认地址为10.96.0.0/12
		--image-repository registry.aliyuncs.com/google_containers 		#默认仓库的gcr.io，国内无法访问，显示定义仓库地址
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
		
		kubeadm join 192.168.5.30:6443 --token j6st5n.rucdhhru9f00k3d6 --discovery-token-ca-cert-hash sha256:aa81f154a062b080fab45762b322573fbfccc5395b3e6d561ef2afe5db9fdd34		#通过此项加入集群

	#使用的root用户，建议使用普通用户
	~]# mkdir -p $HOME/.kube
	~]# cp -i /etc/kubernetes/admin.conf $HOME/.kube/config

	~]# kubectl get componentstatus	#查看集群状态信息
	~]# kubectl get cs
	~]# kubectl get nodes #查看节点信息

	安装flannel网络插件: flannel是coreos的一个子项目，托管与GitHub

	~]# kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml		#访问不了quay.io需要修改镜像仓库，可使用我的阿里仓库  registry.cn-hangzhou.aliyuncs.com/quay-image/

	~]# kubectl get ns #名称空间
	~]# kubectl get pods -n kube-system

	ingress-nginx:
		kubectl apply -f mandatory.yaml
		kubectl apply -f service-nodeport.yaml

### 初始化node：
	
	~]# wget https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo -P /etc/yum.repos.d/

	~]# cat /etc/yum.repos.d/kubernetes.repo 
		[kubernetes]
		name=kubernetes repo
		baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
		gpgcheck=1
		gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
			   https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
		enabled=1
	
	~]# mkdir /etc/docker
	~]# cat /etc/docker/daemon.json  # 可设置镜像加速
		{
		  "registry-mirrors": ["https://nqq67ahg.mirror.aliyuncs.com"]
		}

	~]# systemctl daemon-reload

	#~]# rpm --import yum-key.gpg 

	~]# yum install kubelet-1.15.7 kubeadm-1.15.7 docker-ce -y

	~]# systemctl start docker
	~]# systemctl enable kubelet docker

	~]# echo "1" >/proc/sys/net/bridge/bridge-nf-call-iptables	#不设为1在启动容器时会报错	

	~]# kubeadm join 192.168.5.30:6443 --token j6st5n.rucdhhru9f00k3d6 --discovery-token-ca-cert-hash sha256:aa81f154a062b080fab45762b322573fbfccc5395b3e6d561ef2afe5db9fdd34


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

		~]# kubeadm join 192.168.3.30:6443 --token o4avtg.65ji6b778nyacw68 --discovery-token-ca-cert-hash sha256:2cc3029123db737f234186636330e87b5510c173c669f513a9c0e0da395515b0

### 查看集群DNS(CoreDNS)服务	
 
	~]# yum install -y bind-utils
	~]# kubectl get svc -n kube-system
	NAME       TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)         AGE
	kube-dns   ClusterIP   10.96.0.10   <none>        53/UDP,53/TCP   20h

    ~]# dig A nginx @10.96.0.10
	~]# dig A nginx.default.svc.cluster.local @10.96.0.10

### 部署ingress-nginx


	service的nodeport只能实现基于端口的tcp四层代理，ingress可实现基于http/https的七层代理

	常用反向代理：
		nginx、envoy、vulcand、haproxy、traefik

	GitHub地址：https://github.com/kubernetes/ingress-nginx/tree/master/deploy
	
	1.一键部署
	~]# wget https://github.com/kubernetes/ingress-nginx/blob/master/deploy/mandatory.yaml	#修改镜像拉取地址：registry.cn-hangzhou.aliyuncs.com/quay-image/
	
	~]# kubectl apply -f mandatory.yaml
	~]# kubectl get pod POD_NAME -n ingress-nginx
	
	2.暴露服务
	~]# kubectl apply -f service-ingress-service.yaml

## Dashboard搭建

	github地址：https://github.com/kubernetes/dashboard		#最新
			   https://github.com/kubernetes/kubernetes/tree/release-1.15/cluster/addons/dashboard	#适配对应版本
	
	1.获取资源清单
		~]# wget https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml
	
	2.修改镜像拉取地址，暴露服务(使用nodeport暴露服务)
	
	  修改镜像拉取地址（若需要其他版本，可到阿里云（https://cr.console.aliyun.com/）或其他可访问到的仓库查找）：registry.cn-hangzhou.aliyuncs.com/quay-image/kubernetes-dashboard:v1.10.1	
	
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


## 部署canal提供网络策略功能

	flannel插件提供了pod网络，但是没提供网络策略功能，需要借助calico来实现网络策略，而且官网也说了可以flannel+calico一起使用。

	官网地址：https://docs.projectcalico.org/v3.5/getting-started/kubernetes/installation/flannel
	
	~]# wget https://docs.projectcalico.org/v3.5/getting-started/kubernetes/installation/hosted/canal/canal.yaml		#修改镜像拉取地址后直接部署即可

	~]# kubectl apply -f canal.yaml

## 部署Prometheus

	GitHub地址：https://github.com/kubernetes/kubernetes/tree/release-1.15/cluster/addons/prometheus
	
	修改镜像：
		registry.cn-hangzhou.aliyuncs.com/quay-image/kube-state-metrics:v1.3.0
		registry.cn-hangzhou.aliyuncs.com/quay-image/addon-resizer:1.8.5

	准备PV：需提前搭建nfs服务

		~]# cat nfs-pv.yaml 
			apiVersion: v1
			kind: PersistentVolume
			metadata:
			  name: nfs-pv-01
			  labels:
			    release: nfs-pv
			spec:
			  capacity:
			    storage: 2Gi
			  volumeMode: Filesystem
			  accessModes:
			    - ReadWriteOnce
			  persistentVolumeReclaimPolicy: Recycle
			  storageClassName: standard
			  mountOptions:
			    - hard
			  nfs:
			    path: "/data/nfs/v1"
			    server: nfs.k8s.io
			
			---
			apiVersion: v1
			kind: PersistentVolume
			metadata:
			  name: nfs-pv-02
			  labels:
			    release: nfs-pv
			spec:
			  capacity:
			    storage: 16Gi
			  volumeMode: Filesystem
			  accessModes:
			    - ReadWriteOnce
			  persistentVolumeReclaimPolicy: Recycle
			  storageClassName: standard
			  mountOptions:
			    - hard
			  nfs:
			    path: "/data/nfs/v2"
			    server: nfs.k8s.io

		~]# cat /etc/hosts
			IP nfs.k8s.io

		~]# cat prometheus-service.yaml 		#修改service暴露端口
			kind: Service
			apiVersion: v1
			metadata:
			  name: prometheus
			  namespace: kube-system
			  labels:
			    kubernetes.io/name: "Prometheus"
			    kubernetes.io/cluster-service: "true"
			    addonmanager.kubernetes.io/mode: Reconcile
			spec:
			  type: NodePort
			  clusterIP: 10.96.88.88
			  ports:
			    - port: 9090
			      name: http
			      protocol: TCP
			      nodePort: 30090
			  selector:
			    k8s-app: prometheus
			
	通过集群节点访问：
		http://192.168.5.30:30090

## 部署Grafana

	~]# cat grafana.yaml 
		apiVersion: extensions/v1beta1
		kind: Deployment
		metadata:
		  name: monitoring-grafana
		  namespace: kube-system
		spec:
		  replicas: 1
		  template:
		    metadata:
		      labels:
		        task: monitoring
		        k8s-app: grafana
		    spec:
		      containers:
		      - name: grafana
		        image: grafana/grafana:5.0.4
		        imagePullPolicy: IfNotPresent
		        ports:
		        - containerPort: 3000
		          protocol: TCP
		        volumeMounts:
		        - mountPath: /var
		          name: grafana-storage
		        env:
		        - name: INFLUXDB_HOST
		          value: monitoring-influxdb
		        - name: GF_SERVER_HTTP_PORT
		          value: "3000"
		          # The following env variables are required to make Grafana accessible via
		          # the kubernetes api-server proxy. On production clusters, we recommend
		          # removing these env variables, setup auth for grafana, and expose the grafana
		          # service using a LoadBalancer or a public IP.
		        - name: GF_AUTH_BASIC_ENABLED
		          value: "false"
		        - name: GF_AUTH_ANONYMOUS_ENABLED
		          value: "true"
		        - name: GF_AUTH_ANONYMOUS_ORG_ROLE
		          value: Admin
		        - name: GF_SERVER_ROOT_URL
		          # If you're only using the API Server proxy, set this value instead:
		          # value: /api/v1/namespaces/kube-system/services/monitoring-grafana/proxy
		          value: /
		      volumes:
		      - name: grafana-storage
		        emptyDir: {}
		      tolerations:
		      - key: node-role.kubernetes.io/master
		        value: ""
		        effect: NoSchedule
		      nodeSelector:
		        node-role.kubernetes.io/master: ""
		---
		apiVersion: v1
		kind: Service
		metadata:
		  name: monitoring-grafana
		  namespace: kube-system
		  annotations:
		    prometheus.io/scrape: 'true'
		    prometheus.io/tcp-probe: 'true'
		    prometheus.io/tcp-probe-port: '80'
		  labels:
		    # For use as a Cluster add-on (https://github.com/kubernetes/kubernetes/tree/master/cluster/addons)
		    # If you are NOT using this as an addon, you should comment out this line.
		    #kubernetes.io/cluster-service: 'true'
		    #kubernetes.io/name: monitoring-grafana
		spec:
		  type: NodePort
		  clusterIP: 10.96.66.66
		  selector:
		    k8s-app: grafana
		  ports:
		    - name: grafana
		      port: 3000
		      nodePort: 30088




		
















	
