# 1. Redis搭建

https://www.cnblogs.com/chenmh/p/5121849.html

# 2. Redis常用操作

## 2.1 Redis 主从添加密码认证

```c
1.从库添加密码
    ~]# config set requirepass MzJiMGE1YzRm
    
2.主库添加密码
    ~]# config set requirepass MzJiMGE1YzRm
    
3.从库设置与主库使用密码认证同步
    ~]# config set masterauth MzJiMGE1YzRm
    
4.修改主从库配置文件
   主库: 
   		requirepass MzJiMGE1YzRm
            
   从库:
		requirepass MzJiMGE1YzRm
		masterauth MzJiMGE1YzRm
            
注：
  1.使用中的按照此步骤，新建集群可以添加密码认证后在进行主从同步
  2.主从认证添加完成后，master会重新 sync ,所以要保证主库内存空间足够，否则会同步失败
```



# 3. Redis集群构建

# 4. Redis状态分析

```c
~]# redis-cli -h 172.188.3.18 -p 7000 -a cosepgyTW#d8jf
```

## 4.1 集群信息

```c
> cluster info 
    cluster_state:ok
    cluster_slots_assigned:16384
    cluster_slots_ok:16384
    cluster_slots_pfail:0
    cluster_slots_fail:0
    cluster_known_nodes:6
    cluster_size:3
    cluster_current_epoch:14
    cluster_my_epoch:12
    cluster_stats_messages_ping_sent:13907407
    cluster_stats_messages_pong_sent:13901786
    cluster_stats_messages_sent:27809193
    cluster_stats_messages_ping_received:13901786
    cluster_stats_messages_pong_received:13905626
    cluster_stats_messages_auth-req_received:1
    cluster_stats_messages_received:27807413
```

## 4.2 **集群节点**

```c
> CLUSTER NODES
    0e6c4c01... 172.188.3.18:7001@17001 slave c0807a20... 0 1600842500044 5 connected
    ddec4f02... 172.188.3.20:7001@17001 slave 1aa4abe2... 0 1600842502050 11 connected
    1a9cc886... 172.188.3.18:7000@17000 myself,slave 4b62dc27... 0 1600842498000 1 connected
    c0807a20... 172.188.3.20:7000@17000 master - 0 1600842501045 5 connected 10923-16383
    1aa4abe2... 172.188.3.19:7000@17000 master - 0 1600842500000 11 connected 5461-10922
    4b62dc27... 172.188.3.19:7001@17001 master - 0 1600842501000 12 connected 0-5460
```

## 4.3 当前节点信息

获取 server 信息，包括 version, OS, port 等信息

```c
> INFO server
    # Server
    redis_version:4.0.14
    redis_git_sha1:00000000
    redis_git_dirty:0
    redis_build_id:99030a98a9c82229
    redis_mode:cluster
    os:Linux 3.10.0-957.el7.x86_64 x86_64
    arch_bits:64
    multiplexing_api:epoll
    atomicvar_api:atomic-builtin
    gcc_version:4.8.5
    process_id:226198
    run_id:4c5bce67f220821f429440f785c6d54dee59e314
    tcp_port:7000
    uptime_in_seconds:11905177
    uptime_in_days:137
    hz:10
    lru_clock:7007098
    executable:/data/server/redis-4.0.14/src/redis-server
    config_file:/data/server/redis-cluster/7000/redis.conf
```

## 4.4 获取实例客户端连接状态

```c
> INFO clients
    # Clients
    connected_clients:3326
    client_longest_output_list:0
    client_biggest_input_buf:0
    blocked_clients:0
```

**解读 Redis 连接数的意义：**

```c
clients 包含了连接数，输入输出缓冲和阻塞命令连接数等情况。

      connected_clients：客户端连接的数量。
      client_longest_output_list：当前的客户端连接之中最长的输出列表。
      client_biggest_input_buf：当前的客户端连接之中最大的输入缓冲区。
      blocked_clients：由于阻塞调用（BLPOP、BRPOP、BRPOPLPUSH）而等待的客户端的数量。

连接数其实对于 Redis 来说可以看做是一种有限资源，一般 Redis 都配置有最大连接数限制，因此了解这个对于确保应用正常连接也是相当重要的。 client_longest_output_list 过高则很可能说明现在 Redis 出现了异常，可能要结合clients list 来排查客户端连接情况。使用了阻塞命令时，blocked_clients 也需要重点关注。
```

## 4.5 获取实例内存使用信息

```c
> INFO memory
    # Memory
    used_memory:196868440
    used_memory_human:187.75M
    used_memory_rss:222228480
    used_memory_rss_human:211.93M
    used_memory_peak:1052362384
    used_memory_peak_human:1003.61M
    used_memory_peak_perc:18.71%
    used_memory_overhead:59567916
    used_memory_startup:1458424
    used_memory_dataset:137300524
    used_memory_dataset_perc:70.26%
    total_system_memory:201399148544
    total_system_memory_human:187.57G
    used_memory_lua:37888
    used_memory_lua_human:37.00K
    maxmemory:0
    maxmemory_human:0B
    maxmemory_policy:noeviction
    mem_fragmentation_ratio:1.13
    mem_allocator:jemalloc-4.0.3
    active_defrag_running:0
    lazyfree_pending_objects:0
         
```

**深度剖析 Redis 最重要的 memory：**

```c
对于 Redis 来说，内存是最重要的资源，所以本文首先介绍 Redis 内存状态信息怎么查看， 也就是 memory 这一栏：

      used_memory：Redis 分配器分配的内存量，也就是实际存储数据的内存总量。
      used_memory_human：以可读格式显示 used_memory。
      used_memory_rss：以操作系统的角度，显示 Redis 进程占用的总物理内存。
      used_memory_rss_human：以可读格式显示 used_memory_rss
      mem_fragmentation_ratio：used_memory_rss /used_memory 比值，表示内存碎片率。
    						  其中 used_memory 反映了当前 Redis 存储数据的内存使用情况，当内存使用率达到

Redis 设置的 maxmemory 时，Redis 就会根据设置内存数据逐出策略，以不同的方式移除存储在内存中的数据。比如，如果设置的策略为 noeviction，那么 Redis 会直接返回错误提示。

mem_fragmentation_ratio 表示的内存碎片率，理解这一指标，对优化 Redis 实例的资源性能是非常重要的。内存碎片率稍大于 1 是比较合理的范围，此时内存碎片率还比较低，同时也说明  Redis 没有发生  swap。但如果内存碎片率的值超过了 1.5，那就说明 Redis 消耗了实际需要物理内存的 150%，其中有 50%是内存碎片率，可以直接判定为 Redis 内存碎片过大。内存碎片率是不是越低就越好呢？答案是否定的。当内存碎片率低于 1 时，说明 Redis 内存分配超出了物理内存，操作系统正在进行 swap，Redis 可能会把部分数据交换到硬盘上。swap 会严重影响 Redis 的性能，造成极大的延迟。
```

## 4.6 获取实例持久化信息

```c
> info persistence
    # Persistence
    loading:0
    rdb_changes_since_last_save:783289310
    rdb_bgsave_in_progress:0
    rdb_last_save_time:1588937493
    rdb_last_bgsave_status:ok
    rdb_last_bgsave_time_sec:0
    rdb_current_bgsave_time_sec:-1
    rdb_last_cow_size:729088
    aof_enabled:1
    aof_rewrite_in_progress:0
    aof_rewrite_scheduled:0
    aof_last_rewrite_time_sec:1
    aof_current_rewrite_time_sec:-1
    aof_last_bgrewrite_status:ok
    aof_last_write_status:ok
    aof_last_cow_size:15253504
    aof_current_size:116928063
    aof_base_size:88463545
    aof_pending_rewrite:0
    aof_buffer_length:0
    aof_rewrite_buffer_length:0
    aof_pending_bio_fsync:0
    aof_delayed_fsync:0
```

## 4.7 获取实例状态信息

```c
> info stats
    # Stats
    total_connections_received:272607297
    total_commands_processed:20009649429
    instantaneous_ops_per_sec:1835
    total_net_input_bytes:14804165434122
    total_net_output_bytes:30816365513221
    instantaneous_input_kbps:848.49
    instantaneous_output_kbps:1458.88
    rejected_connections:0
    sync_full:1
    sync_partial_ok:0
    sync_partial_err:1
    expired_keys:782647716
    expired_stale_perc:14.31
    expired_time_cap_reached_count:0
    evicted_keys:0
    keyspace_hits:3797855482
    keyspace_misses:6369530907
    pubsub_channels:0
    pubsub_patterns:0
    latest_fork_usec:15816
    migrate_cached_sockets:0
    slave_expires_tracked_keys:0
    active_defrag_hits:0
    active_defrag_misses:0
    active_defrag_key_hits:0
    active_defrag_key_misses:0
```

**stats 帮你全面理解 Redis 状态：**

```c
stats 可以统计 Redis 的基础信息，比如 Redis 的连接数、命令、网络、同步状态等非常重要的信息。下面介绍以下几个比较重要的信息：

      total_connections_received：连接过的客户端总数。
      total_commands_processed：处理过的命令总数。
      instantaneous_ops_per_sec：每秒处理的命令数。
      keyspace_hits：keyspace 命中次数。
      keyspace_misses：keyspace 未命中次数。
      rejected_connections：由于 maxclients 限制而拒绝的连接数量。
      expired_keys：key 过期事件的总数。
      evicted_keys：由于 maxmemory 限制，而被回收内存的 key 的总数。

total_connections_received 和 total_commands_processed 反映了 Redis 服务器自从启动以来，所有处理过的连接数和命令数。instantaneous_ops_per_sec 反应了 Redis 服务器的忙碌状态。当 rejected_connections 的值不为 0 时，说明应用的连接数过多， 或者 maxclients 配置的太小。对于应用来说，keyspace_hits 和 keyspace_misses 这两项指标是非常关键的。Redis 对其所有的命令都设置了专门的标识属性，如“只读”，“写”或者“管理命令”之类，在 Redis 源码中，查看一下 redisCommand 结构体中 sflags 成员属性字段，就可以知道这个命令是具有哪些属性。比如，w 表示一个写命令（如  set，del 命令），r 表示是一个只读命令（ get ， hmget 命令）， a 则表示一个管理命令(config,shutdown) 。其中keyspace_hits 和 keyspace_misses 都是针对具备只读属性的 Redis 操作命令做统计，如果 info 统计出来的 keyspace_misses 值过高，或者在过去一段时间内增长很快，那么就说明这一段时间从  Redis 中获取数据都没有拿到，这时也许就需要检查一下应用数据在Redis 中的存放和访问情况了。如果 key 在明确的时间周期内被使用，或者旧的 key 将来可能不会被使用，就可以用 Redis 过期时间命令(expire,expireat, pexpire, pexpireat 等)去设置过期时间，这样  Redis 就会在  key 过期时自动删除  key，这个信息可以通过expired_keys 去查看。当内存使用达到设置的最大阀值 maxmemory 时，Redis 则会根据设置的 key 逐出策略，淘汰 Redis 中存储的数据，这个信息可以根据 evicted_keys 查看。
```

## 4.8 获取实例主从配置信息

```
> info replication
    # Replication
    role:master
    connected_slaves:1
    slave0:ip=172.188.3.20,port=7001,state=online,offset=14204629320059,lag=1
    master_replid:92a0ca26a881101fc1d4115612c557ba9649dd5e
    master_replid2:0000000000000000000000000000000000000000
    master_repl_offset:14204629393958
    second_repl_offset:-1
    repl_backlog_active:1
    repl_backlog_size:1048576
    repl_backlog_first_byte_offset:14204628345383
    repl_backlog_histlen:1048576
```

## 4.9 获取实例CPU使用信息

```c
> info cpu 
	# CPU
    used_cpu_sys:908378.62
    used_cpu_user:390942.38
    used_cpu_sys_children:29123.46
    used_cpu_user_children:3722.54
```

## 4.10 获取实例各DB key数量

```c
> info keyspace 
    # Keyspace
    db0:keys=5585,expires=5516,avg_ttl=58020
```

**Keyspace 帮你了解数据状态：**

```c
Keyspace 主要提供关于每个 Redis 数据库的主字典的统计数据。这些统计数据包括键的数量、具有过期时间的 key 的数量和平均生存时间。对于每个数据库来说，keyspace 栏显示的每行信息格式如下所示： dbX: keys=X,expires=X,avg_ttl=X

其中，第一个 X 表示数据库的编号，第二个 X 表示键的数量，第三个 X 表示具有过期时间的键的数量，第四个 X 表示键的平均生存时间。举个

例子：
	db0:keys=6,expires=0,avg_ttl=0：这就表示当前数据库0的 key 总数有6个，带有过期时间的 key 总数0个，平均存活时间为0。

Redis Info 命令的其它信息，在这里也简要介绍一下：如 server 栏，是会显示关于 Redis 服务器自身的一些信息， 如版本号， 操作系统， 端口等。Persistence 和replication 则与数据库持久化和主备复制有关，cpu 反映了 Redis 服务器 CPU 使用信息，commandstas 是显示  Redis 所有命令执行的详细信息，包括命令调用次数、命令消耗的CPU 时间总量、每次执行命令消耗 CPU 时间的平均值。Cluster 主要用来反应集群特性。关于更多 Redis 的使用指南，可以到华为云 Redis 官网上了解，也可以试用免费的Redis，来体验一下内存数据库的使用感受：http://www.huaweicloud.com/product/dcs.html。分布式缓存服务  DCS 是华为云上的Redis 内存数据库服务，基于双机热备的高可用架构，拥有丰富的缓存类型，能够很好地满足用户高读写性能及快速数据访问的业务诉求。分布式缓存服务能够有效加快应用的处  理速度，提升热点数据访问速度，大幅降低数据库读写频率，降低业务对整体架构的压力， 具有高可靠、在线扩展、一键运维等特点。
```

