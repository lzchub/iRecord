#!/bin/bash
# author by songyun,2020-01-07
# this script is used to get TCP connenction status

METRIC=$1

case $METRIC in
	CLOSED)
	    output=`ss -t -a | grep -v State | awk '/CLOSED/ {S[$1]++} END{for(a in S) print S[a]}'`
            if [ "$output" == "" ];then
               echo 0
            else
               echo $output
            fi
            ;;
        LISTEN)
	    output=`ss -t -a | grep -v State | awk '/LISTEN/ {S[$1]++} END{for(a in S) print S[a]}'`
            if [ "$output" == "" ];then
               echo 0
            else
               echo $output
            fi
            ;;
        SYN_RECV)
	    output=`ss -t -a | grep -v State | awk '/SYN-RECV/ {S[$1]++} END{for(a in S) print S[a]}'`
            if [ "$output" == "" ];then
               echo 0
            else
               echo $output
            fi
            ;;
        SYN_SENT)
	    output=`ss -t -a | grep -v State | awk '/SYN-SENT/ {S[$1]++} END{for(a in S) print S[a]}'`
            if [ "$output" == "" ];then
               echo 0
            else
               echo $output
            fi
            ;;
        ESTABLISHED)
	    output=`ss -t -a | grep -v State | awk '/ESTAB/ {S[$1]++} END{for(a in S) print S[a]}'`
            if [ "$output" == "" ];then
               echo 0
            else
               echo $output
            fi
            ;;
        TIME_WAIT)
	    output=`ss -t -a | grep -v State | awk '/TIME-WAIT/ {S[$1]++} END{for(a in S) print S[a]}'`
            if [ "$output" == "" ];then
               echo 0
            else
               echo $output
            fi
            ;;
        CLOSING)
	    output=`ss -t -a | grep -v State | awk '/CLOSING/ {S[$1]++} END{for(a in S) print S[a]}'`
            if [ "$output" == "" ];then
               echo 0
            else
               echo $output
            fi
            ;;
        CLOSE_WAIT)
	    output=`ss -t -a | grep -v State | awk '/CLOSE-WAIT/ {S[$1]++} END{for(a in S) print S[a]}'`
            if [ "$output" == "" ];then
               echo 0
            else
               echo $output
            fi
            ;;
        LAST_ACK)
	    output=`ss -t -a | grep -v State | awk '/LAST-ACK/ {S[$1]++} END{for(a in S) print S[a]}'`
            if [ "$output" == "" ];then
               echo 0
            else
               echo $output
            fi
            ;;
        FIN_WAIT_1)
	    output=`ss -t -a | grep -v State | awk '/FIN-WAIT-1/ {S[$1]++} END{for(a in S) print S[a]}'`
            if [ "$output" == "" ];then
               echo 0
            else
               echo $output
            fi
            ;;
        FIN_WAIT_2)
	    output=`ss -t -a | grep -v State | awk '/FIN-WAIT-2/ {S[$1]++} END{for(a in S) print S[a]}'`
            if [ "$output" == "" ];then
               echo 0
            else
               echo $output
            fi
            ;;
        *)
            echo -e "\e[033mUsage: $0 [CLOSED|CLOSING|CLOSE_WAIT|SYN_RECV|SYN_SENT|FIN_WAIT_1|FIN_WAIT_2|LISTEN|ESTABLISHED|LAST_ACK|TIME_WAIT]\e[0m"  
    esac
