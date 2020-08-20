#!/bin/bash
# Author huangjiaxin@love.com

LUJING="/home/delivery"
NAME=$(basename $PWD)
NUM_V=3

cd ${LUJING}/${NAME}
uid=`ps -ef|grep java|grep ${NAME} |awk '{print $2}'`
# 循环杀死进程
kill -9 $uid

# 备份目录当前 jar 的后时间戳
BTIME=$(date -d today +"%Y%m%d.%H%M")

# 判断bak 文件夹是否存在
if [ ! -d "bak" ];then
    mkdir bak
# else
#   usleep
fi

# 判断 jar.* 新的文件是否存在
if [ -f  *.jar.* ];then
    mv ${NAME}.jar bak/${NAME}.jar.${BTIME}
    # 改名 jar.0 为 jar
    mv ${NAME}.jar.* ${NAME}.jar

    # 写入Versions
    echo ${NAME}.jar.${BTIME} >> Versions


    # 删除过期版本
    she=(`awk '{print $0}' Versions`)
    #printf "数组个数： ${#she[@]} \n"

    #需要删除的文件的名字
    arrnum=${#she[@]}
    n=`expr $arrnum - ${NUM_V}`

    if [ $arrnum -le ${NUM_V} ];then
        echo "数量不够- 未删除"
    else
        cd ./bak/
        for(( i=0;i<${n};i++ ));do
            #rm -rf ${she[i]}
            # printf "${she[i]} \n"
            rm -rf ${she[i]}
            sed -i "/^${she[i]}/"d ${LUJING}/${NAME}/Versions
        done
    fi

fi


# 启动 jar
nohup java  -Xmx3800m -Xms3800m -Xmn2g -Xss1024k -jar ${LUJING}/${NAME}/${NAME}.jar --spring.profiles.active=product-test >${LUJING}/${NAME}/nohup.out 2>&1 &
if [ $? -eq 0 ];then
    echo "Success - 命令运行 - 成功 ！！！ "
else
    echo "Error - 命令运行 - 失败，请检查日志！"
    return "error"
fi


