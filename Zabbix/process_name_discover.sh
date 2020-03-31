#!/bin/bash
 
echo "{"
echo "  "\""data"\"":"[""
 
#for proc in `cat /app/tomcat/rclocal_start.sh | awk -F "/" '{print $4}' | awk -F "_" '{print $2}'`
for proc in `cat /app/tomcat/rclocal_start.sh | awk -F "/" '{print $4}'`
do
    echo "          {"
 
        name=$proc
        ip=`ip a | grep in | tail -n 1 | awk '{print $2}' | awk -F "/" '{print $1}'`
 
    echo "                  "\""{#IPP}"\"":"\""$ip"\"","
    echo "                  "\""{#NAMEE}"\"":"\""$name"\"""
 
    sleep 0.01
    echo "          },"
done
 
    echo "          {"
    echo "                  "\""{#IPP}"\"":"\""port"\"","
    echo "                  "\""{#NAAME}"\"":"\""name"\"""
    echo "          }"
 
echo "  ]"
echo "}"
