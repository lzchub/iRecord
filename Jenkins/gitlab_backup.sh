#!/bin/bash
# author by liuzc

HOMEDIR='/mmkt/gitlab'

# 克隆地址
CLONEURL='ssh://git@192.168.5.132:2289'

# 遍历仓库
SRCDIR='/mmkt/gitlab/data/git-data/repositories'

#临时存放到的本机目录
TMPDIR='/tmp/gitlab'

# 项目列表
SRCREPO=(mmkt mmkt-web)

# 拷贝到目的主机
DEST_IP='192.168.5.131'

# 仅拷贝使用到的项目下的仓库
function repo_backup() {
        # 遍历所有项目
        for repo in ${SRCREPO[@]}
        do
                # 遍历所有使用到的项目下的所有仓库
                for src in `ls $SRCDIR/$repo | grep -v wiki`
                do
                        # 本机临时存放目录，不存在创建
                        if [ ! -d $TMPDIR/$repo ];then
                                mkdir -p $TMPDIR/$repo
                        fi

                        echo $src

                        # 克隆仓库
                        #git clone $CLONEURL/$repo/$src $TMPDIR/$repo/$src
                        sleep 1
                done
        done

        cd $TMPDIR

        # 按时间打包
        tar czf $(basename $TMPDIR)_$(date +"%Y%m%d%H%M").tar.gz . &> /dev/null

        # 传输到存储服务器上，需要做无交互认证，且需在存储服务器上创建目录
        #scp *.tar.gz $DEST_IP:$TMPDIR

        # 测试
        #mv *.tar.gz /tmp

        # 删除临时目录
        rm -rf $TMPDIR
}

# 拷贝gitlab所有文件，data,config
function all_backup() {

        cp -r $HOMEDIR $TMPDIR

        cd $TMPDIR

        tar czf $(basename $TMPDIR)_all_$(date +"%Y%m%d%H%M").tar.gz . &> /dev/null

        #scp *.tar.gz $DEST_IP:$TMPDIR

        #mv *.tar.gz /tmp

        rm -rf $TMPDIR

}

# repo为只备份代码仓库，all为备份所有文件
case $1 in
        repo)
                repo_backup
        ;;
        all)
                all_backup
        ;;
        *)
                echo "Usage:[ repo | all ]"
        ;;
esac