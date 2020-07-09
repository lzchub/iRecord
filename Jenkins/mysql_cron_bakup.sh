#!/bin/bash
#Author huangjiaxin@love.com

DB_HOSTNAME="rm-bp168c33t9lw12b2d.mysql.rds.aliyuncs.com" 				# Mysql所在主机的主机名
DB_USERNAME="develop"                			 # MySQL登录用户名
DB_PASSWORD="Rhty@007"          			 # mysql登录密码

# 备份的数据库名
DATABASES=(
            "mmkt_comm_data"                          
            "mmkt_consult_callback"
            "mmkt_course"                          
            "mmkt_leave"                          
            "mmkt_msg"                          
            "mmkt_psychological_test"                          
            "mmkt_question"                          
            "mmkt_sign"                          
            "mmkt_user"                          
            "mmkt_wx"                          
)

BACKUP_FOLDERNAME="/home/delivery/bakup/bak_mysql"		# 数据库备份文件的主目录 ("/").

echo "Bash Database Backup Tool"

# CURRENT_DATE=$(date +%F)             			 #定义当前日期为变量
CURRENT_DATE=$(date -d today +"%Y-%m-%d.%H%M")            			 #定义当前日期为变量
BACKUP_FOLDER="${BACKUP_FOLDERNAME}/${CURRENT_DATE}"      #存放数据库备份文件的目录
mkdir -p  $BACKUP_FOLDER          #创建数据库备份文件目录

RESULT="0"
#循环这个数据库名称列表然后逐个备份这些数据库
for DATABASE in ${DATABASES[@]};do
    echo "[+] Mysql-Dumping: ${DATABASE}"
    echo -n "   Began:  ";echo $(date)

    if $(mysqldump -h${DB_HOSTNAME}  -u${DB_USERNAME} -p${DB_PASSWORD} --set-gtid-purged=OFF --default-character-set=utf8   ${DATABASE}  > "${BACKUP_FOLDER}/${DATABASE}.sql");then
	echo "  Dumped successfully!"
        echo "[+] Packaging and compressing the backup folder..."  
	RESULT="0"
    else
        echo "  Failed dumping this database!"
        # send email notification
        ##########################################################
        # echo "  Sent mail OK!"
	RESULT="1"
    fi

done

echo "[+] Finish" $(date)

#写创建备份日志 
if [ ${RESULT} -eq 0 ];then
    echo "success --  $(date +%F) -- 数据库备份成功 " >> ${BACKUP_FOLDERNAME}/log.txt 
else
    echo "error   --  $(date +%F) -- 数据库备份失败！！！" >> ${BACKUP_FOLDERNAME}/log.txt
fi


