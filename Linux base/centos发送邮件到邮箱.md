# 邮件发送脚本

```c
#/bin/bash
curdate=$(date -d "1 day ago" +"%Y%m%d")
subject="VAS非法请求日志统计(10.1.32.4)_${curdate}"
mailcc="scyw.list@ysten.com"
mailsend="xieweizhong@ysten.com songming@ysten.com"
filepath='/home/pukelei_cmsc06/vas_referer.log'
cat /data/nginxlogs/vas_*access.log$(date -d "1 day ago" +"%Y%m%d") | grep -E '/v3/cloudpay/payOrder|/v3/cloudpay/createOrder' | grep -vE "\"http://unionpay.sca.bcs.ottcn.com:838[1,2]|\"http://jtdsepg.cdzgys.cn" > ${filepath}
logrownum=$(cat $filepath | wc -l)
if [[ $logrownum -lt 100 ]];then
    echo -e "    各位好：以下是非法请求日志。请查收！\n异常日志条数：${logrownum}条\n\n$(cat ${filepath})" | mail -s "${subject}" -c "${mailcc}" "${mailsend}"
else
    cd /home/pukelei_cmsc06
    tar -czf vas_referer.log.tgz vas_referer.log
    echo -e "    各位好：附件是非法请求日志。请查收！\n常日志条数：${logrownum}条" | mail -a ${filepath}.tgz -s "${subject}" -c "${mailcc}" "${mailsend}"
fi
```



# 配置邮箱信息

```c
~]# cat /etc/mail.rc
set hold
set append
set ask
set crt
set dot
set keep
set emptybox
set indentprefix="> "
set quote
set sendcharsets=iso-8859-1,utf-8
set showname
set showto
set newmail=nopoll
set autocollapse
ignore received in-reply-to message-id references
ignore mime-version content-transfer-encoding
fwdretain subject date from to
set from=pukelei@ysten.com
set smtp=smtp.ysten.com
set smtp-auth-user=pukelei@ysten.com
set smtp-auth-password=PklPkl123
set smtp-auth=login
```

