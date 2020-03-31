问题一：日志索引被集群设置为只读

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

问题二：kafka消息堆积，磁盘被kafka占用完，写不进es

	1、停掉kafka进程
	2、将kafka的server.properties中的log.retention.hours=1/60   #将日志数据保留1分钟
	3、重启kafka
