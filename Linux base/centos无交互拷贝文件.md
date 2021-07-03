# 无交互传输文件

```c
#!/usr/bin/expect

###########################################################
#  description: scp without interactive                   #
#  author     :  lzc                                      #
###########################################################

set timeout 60
set host 10.25.171.110
set name liuzichuan_cmsc18
set port 22300
set password YzMyYzIxNjkwYWVh
set file /home/liuzichuan_cmsc18/programlist.txt
spawn scp -P $port $name@$host:$file /home/liuzichuan_cmsc18/
    expect {
        "(yes/no)?"
        {
            send "yes\n"
            expect "*assword:" { send "$password\n"}
        }
        "*assword:"
        {
            send "$password\n"
        }
    }
#interact 这个不行，需要用下面几行
set timeout 60
expect eof
exit 0
```

注：需要先下载expect工具

```c
yum install -y expect
```

