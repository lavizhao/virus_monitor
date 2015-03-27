#!/usr/bin/python3

'''
插入样例语句
'''

import sys
sys.path.append("..")

import unittest

from monitor.db_info import field,kvtuple,table
from monitor.db import mydb

#mdb = mydb(host='localhost',port='3306',user='root',passwd='')
mdb = mydb(host='192.168.140.98',port='3306',user='root',passwd='hitjin')

from monitor.table_info import my_table,get_table

dbname = "virus"

if __name__ == '__main__':
    #插入设备基本信息表
    record1 = {\
               "device_name":"SV123456789",\
               "device_ip":"192.168.140.98",\
               "device_access":"test",\
               "device_access_interval":"test",\
               "manage_access_interval":"test",\
               "manage_access":"test"\
           }

    tb = get_table("device_info")

    insert_str = tb.insert_str(record1)
    mdb.execute_sql(insert_str,dbname)

    #插入探针信息表
    record2 = {\
               "device_name":"SV123456789",\
               "device_port":"33598",\
               "device_type":"ruixing",\
               "virus_statistic":"test",\
               "network_segment":"test"\
           }

    tb = get_table("probe_info")

    insert_str = tb.insert_str(record2)
    mdb.execute_sql(insert_str,dbname)

    #插入探针型号信息表
    record3 = {\
               "device_type":"ruixing",\
               "brand":"unknown",\
               "coding_type":"utf-8",\
               "matching_rule":r"<(.+?)>viruslog: \\S+ \\S+ \\S+ \\S+ (.+?) (.+?) \\S+ \\S+ (.+?) (.+?) \\S+ (.+?) (.+?) \\S+ GET\\S+ \\S+ ",\
               "matching_position":"log_level:0 virus_name:1 virus_type:2 spread_device_ip:3 spread_device_port:4 infected_device_ip:5 infected_device_port:6"\
           }

    tb = get_table("probe_type_info")

    insert_str = tb.insert_str(record3)
    mdb.execute_sql(insert_str,dbname)

#==========================================================================    
    
    #插入探针型号信息表
    record4 = {\
               "device_type":"xingyun",\
               "brand":"unknown",\
               "coding_type":"utf-8",\
               "matching_rule":r"\\S+;evtname:(.+?);eid:(.+?);\\S+;se:(.+?);\\S+;\\S+;\\S+;sr:(.+?);dest:(.+?);sport:(.+?);dport:(.+?);\\S+;\\S+",\
               "matching_position":"log_level:2 virus_name:0 virus_type:1 spread_device_ip:3 spread_device_port:5 infected_device_ip:4 infected_device_port:6"\
           }

    tb = get_table("probe_type_info")

    insert_str = tb.insert_str(record4)
    mdb.execute_sql(insert_str,dbname)

    #插入设备基本信息表
    record5 = {\
               "device_name":"SV98654321",\
               "device_ip":"127.0.0.3",\
               "device_access":"test",\
               "device_access_interval":"test",\
               "manage_access_interval":"test",\
               "manage_access":"test"\
           }

    tb = get_table("device_info")

    insert_str = tb.insert_str(record5)
    mdb.execute_sql(insert_str,dbname)

    #插入探针信息表
    record6 = {\
               "device_name":"SV98654321",\
               "device_port":"33598",\
               "device_type":"xingyun",\
               "virus_statistic":"test",\
               "network_segment":"test"\
           }

    tb = get_table("probe_info")

    insert_str = tb.insert_str(record6)
    mdb.execute_sql(insert_str,dbname)

#======================================================

 #插入设备基本信息表
    record1 = {\
               "device_name":"SV9999",\
               "device_ip":"127.0.0.1",\
               "device_access":"test",\
               "device_access_interval":"test",\
               "manage_access_interval":"test",\
               "manage_access":"test"\
           }

    tb = get_table("device_info")

    insert_str = tb.insert_str(record1)
    mdb.execute_sql(insert_str,dbname)

    #插入探针信息表
    record2 = {\
               "device_name":"SV9999",\
               "device_port":"33598",\
               "device_type":"APT",\
               "virus_statistic":"test",\
               "network_segment":"test"\
           }

    tb = get_table("probe_info")

    insert_str = tb.insert_str(record2)
    mdb.execute_sql(insert_str,"virus")

    #插入探针型号信息表
    record3 = {\
               "device_type":"APT",\
               "brand":"unknown",\
               "coding_type":"utf-8",\
               "matching_rule":r"APT~\\S+~1~.+~(.+?):(.+?)~(.+?):(.+?)~\\S+~(.+?)~\\S+~(.+?)~(.+?)~\\S+~\\S+",\
               "matching_position":"log_level:5 virus_name:4 virus_type:6 spread_device_ip:0 spread_device_port:1 infected_device_ip:2 infected_device_port:3"\
           }

    tb = get_table("probe_type_info")

    insert_str = tb.insert_str(record3)
    mdb.execute_sql(insert_str,dbname)    
