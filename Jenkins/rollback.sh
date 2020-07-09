#!/bin/bash
# Author huangjiaxin@love.com
# 回滚操作
source /etc/profile 

# 获取当前目录的绝对路径
echo "call rollback.sh"
current_path=$(cd $(dirname $0);pwd)
echo "current_path=$current_path"

# 获取当前时间作为版本号(示例：20190508.1130)
CURRENT_TIME=$(date -d today +"%Y%m%d.%H%M")



if [ -n "$1" ];then
    #包含参数，回滚指定版本
    Spe_Version=$1
    # echo $Spe_Version
    # 复制以前版本，重命名
    cp bak/${Spe_Version} ${FNAME}.jar.0
    sh deploy.sh

else
    # 默认回滚上一个版本
    
    echo "上一个版本"
    Pre_Version=$(tail -n 1 Versions)
    # 获取jar包文件名
    FNAME=$(awk -F "." '{print $1}' Versions |tail -n 1 )
    # 复制以前版本，重命名
    cp bak/${Pre_Version} ${FNAME}.jar.0
    sh deploy.sh
fi

