#!/usr/bin/python
#coding: utf-8

'''
监听程序的主体, 都是在这个部分跑的
'''

from SocketServer import ThreadingUDPServer as UDP
from SocketServer import DatagramRequestHandler as DRH
from multiprocessing import Process,Queue
import time

import sys,logging
sys.path.append("..")
from monitor.listener import processer
from monitor.read_conf import config

cf = config("server.conf")

gqueue = Queue(int(cf["queue_size"]))

def handle():
    print("handle start")
    count = 0
    ps = processer(cf)
    
    while 1:
        if gqueue.qsize() > 0:
            data,address = gqueue.get()
            ps.handle(data,address)
            count += 1
            print(count,"=")
        else:
            time.sleep(0.001)

            
server_ip = cf["server_ip"]
server_port = int(cf["server_port"])
server_address = (server_ip,server_port)

class listener(DRH):
        
    def handle(self):
        gqueue.put((self.request[0],self.client_address))


if __name__ == '__main__':

    print("begin to listen")
    num = int(cf["num_threads"])
    
    for i in range(num):
        p = Process(target=handle,args=(tuple()))
        p.start()

    try :
        server = UDP(server_address,listener)

    except Exception as err:
        logging.error(err)
        logging.error("no server has been built")

    server.serve_forever()    
        
    print("end listen")
    
