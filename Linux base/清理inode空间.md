

```c
~]# df -li		#查看inode空间
    
~]# for i in /*; do echo $i; find $i | wc -l; done		#查找哪个文件占用inode数量较大

```

测试一下Linux下面删除大量文件的效率。



首先建立50万个文件

- 

```
$ test   for i in $(seq 1 500000);do echo text >>$i.txt;done
```

**1.  rm删除**

```
$ time rm -f *zsh: sure you want to delete all the files in /home/hungerr/test [yn]? yzsh: argument list too long: rmrm -f *  3.63s user 0.29s system 98% cpu 3.985 total由于文件数量过多，rm不起作用。
```

**2.  find删除**

```
 $ time find ./ -type f -exec rm {} \;find ./ -type f -exec rm {} \;  49.86s user 1032.13s system 41% cpu 43:19.17 total大概43分钟,我的电脑。。。。。。边看视频边删的。
```

**3.  find with delete**

```
$ time find ./ -type f -deletefind ./ -type f -delete  0.43s user 11.21s system 2% cpu 9:13.38 total用时9分钟。
```

**4.  rsync删除**

```
# 首先建立空文件夹blanktest$ time rsync -a --delete blanktest/ test/rsync -a --delete blanktest/ test/  0.59s user 7.86s system 51% cpu 16.418 total16s，很好很强大。
```

**5.  Python删除**

```
import osimport timeitdef main():    for pathname,dirnames,filenames in os.walk('/home/username/test'):        for filename in filenames:            file=os.path.join(pathname,filename)            os.remove(file)            if __name__=='__main__':t=timeit.Timer('main()','from __main__ import main')print t.timeit(1)　　12$ python test.py529.309022903大概用时9分钟。
```

**6.  Perl删除**

```
$ time perl -e 'for(<*>){((stat)[9]<(unlink))}'perl -e 'for(<*>){((stat)[9]<(unlink))}'  1.28s user 7.23s system 50% cpu 16.784 total16s，这个应该最快了。
```

**7、结果：**

```
rm：文件数量太多，不可用find with -exec 50万文件耗时43分钟find with -delete 9分钟Perl  16sPython 9分钟rsync with -delete  16s
```

结论：删除大量小文件rsync最快，最方便。



