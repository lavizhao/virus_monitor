#!/usr/bin/python3
#coding: utf-8

'''
测试用, 模拟client
'''

import socket

if "__main__" == __name__:

    address = ("localhost",514)
    
    client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    data = bytes("<2>viruslog: 2014-12-10 16:24:03 0x0103000000000000 SV1313060137 Trojan.Win32.Generic.14B62827 木马 中 未知传毒单位名 111.161.66.157 80 hit 192.168.140.83 59389 http GET&nbsp;http://www.qm123.com.cn/shuazhuaqi.rar<--http://down.zdnet.com.cn/link/43/426146.shtml 338762 ","utf-8")

    client.sendto(data,address)

       


