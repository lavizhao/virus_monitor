#coding: utf-8
'''
用来监听的主类
'''

import sys
import logging

from .db import mydb

from .table_info import my_table,get_table

#得到探针日志信息表
probe_log_info = get_table("probe_log_info")

server_ip = '0.0.0.0'
server_port = 514
server_address = (server_ip,server_port)
data_payload = 2048
db_name = "virus2"

import re

import time

suck = 0

def get_time_str():
    return time.strftime('%Y-%m-%d %H:%M:%S')

class processer:
    def __init__(self):
        #self.db = mydb(host='localhost',user="root",passwd='',port='3306')
        #self.db = mydb(host='192.168.140.98',user="root",passwd='hitjin',port='3306')
        self.db = mydb(host='192.168.140.98',user="zhao",passwd='111111111',port='3306')
    
    #执行监听任务
    def handle(self,data,address):
        
        #如果有数据
        if data:

            #解端口
            ip,port = address
            #print("探针ip %s port %s"%(ip,port))

            #step1 从设备基本信息表中获取设备名
            device_name = self.get_probe_name_from_ip_port(ip,port)

            #step2 从探针信息表中获取syslog端口, 探针型号, 病毒日志统计, 监控网段
            all_info = self.get_all_info_from_probe_info(device_name)
            if all_info == None:
                logging.warning("can not find any information in probe info")
                return None

            device_port,device_type = all_info

            #step3 从探针型号信息表中得到全部信息
            all_info = self.get_all_from_probe_type_info(device_type)
            if all_info == None:
                logging.warning("can not find any information in probe type info")
                return None
            brand,coding_type,matching_rule,matching_position = all_info

            #step4 将data转码, 转成utf-8
            #data = str(data,encoding=coding_type)
            #data = data.encode()
            #data = str(data,encoding="utf-8")
            data = data.decode(coding_type).encode("utf-8").strip()

            #step5 用正则表达式抓取
            pattern = re.compile(matching_rule.strip(),re.DOTALL)
            temp_position = pattern.findall(data)

            #如果正则表达式没有找出来, 说明不是病毒日志, 不进行存储 
            if len(temp_position) == 0:
                logging.warning("this is not a virus log")
                return None
            else:
                temp_position = temp_position[0]
            

            #step6 检验合法性=====未做

            #step 7 映射字段
            ndict = self.get_matching_position(temp_position,matching_position)
            ##填写其他信息
            ndict["log_id"] = "test"
            ndict["probe_ip"] = ip
            ndict["infected_time"] = get_time_str()

            ndict["infected_device_ip"] = self.extract_ip(ndict["infected_device_ip"])
            ndict["infected_device_port"] = self.extract_port(ndict["infected_device_port"])

            ndict["spread_device_ip"] = self.extract_ip(ndict["spread_device_ip"])
            ndict["spread_device_port"] = self.extract_port(ndict["spread_device_port"])

            
            #step 8 存
            insert_str = probe_log_info.insert_str(ndict)
            self.db.insert_sql(insert_str,db_name)

                
        else:
            logging.warning("no data recived, client error")


    #抓取ip
    def extract_ip(self,mip):
        ip = re.findall(r'\d+\.\d+\.\d+\.\d+',mip)
        return ip[0]

    def extract_port(self,mport):
        port = re.findall(r'\d+',mport)
        return port[0]
            
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
            return None
        else:
            pass

        result = result[0]
        #这里是采取硬结构进行编码, 因为返回的就是个list, 后面考虑修改    
        return result[0]

    #sql2 从探针信息表中获取syslog端口, 探针型号, 病毒日志统计, 监控网段
    def get_all_info_from_probe_info(self,device_name):
        sql_str = "select device_port,device_type_id from probe_info where device_name_id = \"%s\";"%(device_name)
        result = self.db.select_sql(sql_str,db_name)

        #如果结果大于1, 说明数据库录入有错误
        if len(result) > 1:
            logging.error("more than one record has been found, error in device_info")
            return None
        elif len(result) == 0:
            logging.error("no record has been found, error in probe_info")
            return None
        else:
            pass

        result = result[0]
        
        return result
        
    #sql3 从探针型号信息表中得到数据
    def get_all_from_probe_type_info(self,device_type):
        sql_str = "select brand,coding_type,matching_rule,matching_positon from probe_type_info where id = \"%s\";"%(device_type)
        result = self.db.select_sql(sql_str,db_name)

        #如果结果大于1, 说明数据库录入有错误
        if len(result) > 1:
            logging.error("more than one record has been found, error in device_info")
        elif len(result) == 0:
            logging.error("no record has been found, error in probe_type_info")
        else:
            pass

        result = result[0]
        
        #这里是采取硬结构进行编码, 因为返回的就是个list, 后面考虑修改    
        return result

