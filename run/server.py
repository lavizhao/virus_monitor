#!/usr/bin/python
#coding: utf-8

'''
监听程序的主体, 都是在这个部分跑的
'''

from SocketServer import ThreadingUDPServer as UDP
from SocketServer import DatagramRequestHandler as DRH
from multiprocessing import Process,Queue
import time

import sys,logging,logging.handlers
sys.path.append("..")
from monitor.listener import processer
from monitor.read_conf import config

#配置log
LOG_FILE = 'crash.log'  
  
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024) # 实例化handler    
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'  
  
formatter = logging.Formatter(fmt) 
handler.setFormatter(formatter)    
  
logger = logging.getLogger('crash')
logger.addHandler(handler)         
logger.setLevel(logging.DEBUG)

cf = config("server.conf")

gqueue = Queue(int(cf["queue_size"]))


def handle():
    print("handle start")
    count = 0
    ps = processer(cf,logger)
    
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
        logger.error("不能建立server，建立server有问题，err为%s"%(err))

    server.serve_forever()    
        
    print("end listen")
    
