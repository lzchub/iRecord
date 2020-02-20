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