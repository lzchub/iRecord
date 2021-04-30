问题一：日志索引被集群设置为只读

	cluster.routing.allocation.disk.watermark.low: 默认 85% 当达到时，replica 不再写入 
	cluster.routing.allocation.disk.watermark.high: 默认 90% 当达到时，shards 会尝试写入其他节点
	cluster.routing.allocation.disk.watermark.flood_stage: 默认 95% 当达到时，所有索引变为 readonly状态
	
	报错：logstash.outputs.elasticsearch] retrying failed action with response code: 403 ({"type"=>"cluster_block_exception", "reason"=>"blocked by: [FORBIDDEN/12/index read-only / allow delete (api)]
	
	kibana dev tools:
	
		PUT _settings
		{
		    "index": {
		    	"blocks": {
		    		"read_only_allow_delete": "false"
		    	}
		    }
		}
		
	命令行：
		~]# curl -XPUT -H "Content-Type: application/json" http://170.100.104.47:9200/_all/_settings -d '{"index.blocks.read_only_allow_delete": null}'
		
		 如果单个索引的话可以使用 “索引名/setting” 
	
		#磁盘低水位线为90%（不再分配分片），高水位线为95%（将分片分配到其他节点）
		PUT _cluster/settings
		{
		  "transient": {
		    "cluster.routing.allocation.disk.watermark.low": "90%",
		    "cluster.routing.allocation.disk.watermark.high": "95%",
		    "cluster.info.update.interval": "1m"
		  }
		}

问题二：kafka消息堆积，磁盘被kafka占用完，写不进es

	1、停掉kafka进程
	2、将kafka的server.properties中的log.retention.hours=1/60   #将日志数据保留1分钟
	3、重启kafka

问题三：清理es索引

```c
~]# curl -XDELETE http://IP:PORT/INDICES_NAME
```

知识点整理 

https://blog.csdn.net/laoyang360/article/details/106464359