#!/usr/bin/python3
#coding: utf-8

'''
测试用, 模拟client
'''

import socket

if "__main__" == __name__:

    address = ("localhost",514)
    
    client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    data = bytes("hello world","utf-8")

    client.sendto(data,address)

       


