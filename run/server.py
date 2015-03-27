#!/usr/bin/python
#coding: utf-8

'''
监听程序的主体, 都是在这个部分跑的
'''

from SocketServer import ThreadingUDPServer as UDP1
from SocketServer import DatagramRequestHandler as DRH
from multiprocessing import Process,Queue
import time
from gevent.server import DatagramServer as UDP

import sys,logging
sys.path.append("..")
from monitor.listener import processer

gqueue = Queue(100000)

def handle():
    print("handle start")
    count = 0
    ps = processer()
    
    while 1:
        if gqueue.qsize() > 0:
            data,address = gqueue.get()
            ps.handle(data,address)
            count += 1
            print(count,"=")
        else:
            time.sleep(0.001)



            
server_ip = '0.0.0.0'
server_port = 514
server_address = (server_ip,server_port)

class listener(UDP):
        
    def handle(self,data,address):
        gqueue.put((data,address))


if __name__ == '__main__':

    print("begin to listen")
    num = 1
    
    for i in range(num):
        p = Process(target=handle,args=(tuple()))
        p.start()

    try :
        #server = UDP(server_address,listener)
        server = listener('514')

    except Exception as err:
        logging.error(err)
        logging.error("no server has been built")

    #lis.run()
    server.serve_forever()    
        
    print("end listen")
    
