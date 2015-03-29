#!/usr/bin/python3
#coding: utf-8

'''
测试用, 模拟client
'''

import socket
import time
import random

def ran():
    return random.random()/10000.0

if "__main__" == __name__:

    address = ("localhost",514)
    
    client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #data = bytes("<2>viruslog: 2014-12-10 16:24:03 0x0103000000000000 SV1313060137 Trojan.Win32.Generic.14B62827 木马 中 未知传毒单位名 111.161.66.157 80 hit 192.168.140.83 59389 http GET&nbsp;http://www.qm123.com.cn/shuazhuaqi.rar<--http://down.zdnet.com.cn/link/43/426146.shtml 338762 ","utf-8")

    data = bytes("evtip:192.168.54.33;evtname:HTTP_directory.php_任意命令尝试;eid:152518787;counts:4;se:20;rspmode:65541;secutype:9;proto:HTTP;sr:192.168.3.50;dest:219.234.94.233;sport:0;dport:0;smac:00-0d-60-fb-19-4b;dmac:00-0d-60-fb-19-4b;param:主机名称=219.234.94.233;URL长度=39;URL名称=/directory.php?dir=%3Bcat%20/etc/passwd","utf-8")
    #data = bytes("APT~2~1~2014-19-20 16:24:03~212.212.212.212:90~192.168.140.40:20~2~木马~lalalala~高~121~www.baidu.com~232132","utf-8")

    count = 3
    
    for i in range(count):
        print(i)
        client.sendto(data,address)
        time.sleep(ran())
        

       


