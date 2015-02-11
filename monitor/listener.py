'''
用来监听的主类
'''

import socket
import socketserver
import sys
import logging

from socketserver import UDPServer as UDP
from socketserver import DatagramRequestHandler as DRH

from .db import mydb

from .table_info import my_table,get_table

#得到探针日志信息表
probe_log_info = get_table("probe_log_info")

server_ip = '0.0.0.0'
server_port = 514
server_address = (server_ip,server_port)
data_payload = 2048
db_name = "virus"

import re

import time

def get_time_str():
    return time.strftime('%Y-%m-%d %H:%M:%S')

class listener(DRH):

    #执行监听任务
    def handle(self):
        self.db = mydb(host='localhost',user="root",passwd='',port='3306')
        
        #建socket
        #sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        #确保reuse
        #sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

        #绑定端口
        #sock.bind(server_address)

        #接收的信息
        #data,addr = sock.recvfrom(data_payload)
        data = self.request[0]

        #如果有数据
        if data:
            print("data",data)

            #解端口
            ip,port = self.client_address
            print("ip %s port %s"%(ip,port))

            #step1 获取设备名
            device_name = self.get_probe_name_from_ip_port(ip,port)
            print("device_name",device_name)

            #step2 从探针信息表中获取syslog端口, 探针型号, 病毒日志统计, 监控网段
            device_port,device_type,virus_statistic,network_segment = self.get_all_info_from_probe_info(device_name)
            print("设备端口",device_port)
            print("设备型号",device_type)
            print("病毒统计",virus_statistic)
            print("监控网段",network_segment)

            #step3 从探针型号信息表中得到全部信息
            brand,coding_type,matching_rule,matching_position = self.get_all_from_probe_type_info(device_type)
            print("品牌信息",brand)
            print("编码格式",coding_type)
            print("匹配规则",matching_rule)
            print("映射字段",matching_position)

            #step4 将data转码, 转成utf-8
            data = str(data,encoding=coding_type)
            data = data.encode()
            data = str(data,encoding="utf-8")

            print("data now is : ",data)

            #step5 用正则表达式抓取
            pattern = re.compile(matching_rule,re.DOTALL)
            print("匹配规则|%s|"%(matching_rule))
            temp_position = pattern.findall(data)[0]
            print(temp_position)


            #step6 检验合法性=====未做

            #step 7 映射字段
            ndict = self.get_matching_position(temp_position,matching_position)
            ##填写其他信息
            ndict["log_id"] = "test"
            ndict["probe_ip"] = ip
            ndict["infected_time"] = get_time_str()

            print(ndict)

            #step 8 存
            insert_str = probe_log_info.insert_str(ndict)
            print("============================================")
            print("插入语句",insert_str)
            self.db.execute_sql(insert_str,db_name)
                
        else:
            logging.warning("no data recived, client error")


    #matching position 形式如下: col:0 0表示正则表达式抓出来的pattern的位置
    def get_matching_position(self,position,matching_position):
        sp = matching_position.split()

        ndict = {}
        
        for kv in sp:
            t = kv.split(":")
            key,value = t[0],int(t[1])

            ndict[key] = position[value]

        return ndict
            
    #封装sql语句,起到的作用是数据#
    #sql1 通过ip和port查找数据库中的探针名
    #====== 这里没有用port, 因为udp的port每次都会变 =======
    def get_probe_name_from_ip_port(self,ip,port):
        sql_str = "select * from device_info where device_ip = \"%s\";"%(ip)
        result = self.db.select_sql(sql_str,db_name)

        #如果结果大于1, 说明数据库录入有错误
        if len(result) > 1:
            logging.error("more than one record has been found, error in device_info")
        elif len(result) == 0:
            logging.error("no record has been found, error in device_info")
        else:
            pass

        result = result[0]
        #这里是采取硬结构进行编码, 因为返回的就是个list, 后面考虑修改    
        return result[0]

    #sql2 从探针信息表中获取syslog端口, 探针型号, 病毒日志统计, 监控网段
    def get_all_info_from_probe_info(self,device_name):
        sql_str = "select * from probe_info where device_name = \"%s\";"%(device_name)
        result = self.db.select_sql(sql_str,db_name)

        #如果结果大于1, 说明数据库录入有错误
        if len(result) > 1:
            logging.error("more than one record has been found, error in device_info")
        elif len(result) == 0:
            logging.error("no record has been found, error in device_info")
        else:
            pass

        result = result[0]
        
        device_port = result[1]
        device_type = result[2]
        virus_statistic = result[3]
        network_segment = result[4]
        
        #这里是采取硬结构进行编码, 因为返回的就是个list, 后面考虑修改    
        return device_port,device_type,virus_statistic,network_segment

    #sql3 从探针型号信息表中得到数据
    def get_all_from_probe_type_info(self,device_type):
        sql_str = "select * from probe_type_info where device_type = \"%s\";"%(device_type)
        result = self.db.select_sql(sql_str,db_name)

        #如果结果大于1, 说明数据库录入有错误
        if len(result) > 1:
            logging.error("more than one record has been found, error in device_info")
        elif len(result) == 0:
            logging.error("no record has been found, error in device_info")
        else:
            pass

        result = result[0]
        
        brand = result[1]
        coding_type = result[2]
        matching_rule = result[3]
        matching_position = result[4]
        
        #这里是采取硬结构进行编码, 因为返回的就是个list, 后面考虑修改    
        return brand,coding_type,matching_rule,matching_position
