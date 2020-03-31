#!/bin/bash
# author by songyun,2020-1-6
# this scripts is used to get CPU and MEM status for java process

METRIC=$1
PROC_NAME=$2

case $METRIC in
	CPU)
		output=`ps aux | grep $PROC_NAME | grep -v grep | awk '{print $3}'` 
		if [ "$output" == "" ];then
			echo 0
		else
			#echo $output | awk '{print int($0)}'
			echo $output | awk '{print $3}'
		fi
	;;
	MEM)
		output=`ps aux | grep $PROC_NAME | grep -v grep | awk '{print $5}'`
		if [ "$output" == "" ];then
			echo 0
		else
			#echo $output | awk '{print int($0)}'
			echo $output | awk '{print $3}'
		fi
	;;	
esac
