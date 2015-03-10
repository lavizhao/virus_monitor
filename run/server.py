#!/usr/bin/python3

'''
监听程序的主体, 都是在这个部分跑的
'''

from socketserver import ThreadingUDPServer as UDP

import sys,logging
sys.path.append("..")

from monitor.listener import listener

server_ip = '0.0.0.0'
server_port = 514
server_address = (server_ip,server_port)


if __name__ == '__main__':

    print("begin to listen")

    try :
        #lis = listener()

        server = UDP(server_address,listener)

    except Exception as err:
        logging.error(err)
        logging.error("no server has been built")

    #lis.run()
    server.serve_forever()    
        
    print("end listen")
    
