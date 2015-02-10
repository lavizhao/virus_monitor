#!/usr/bin/python3

'''
插入样例语句
'''

import sys
sys.path.append("..")

import unittest

from monitor.db_info import field,kvtuple,table
from monitor.db import mydb

mdb = mydb(host='localhost',port='3306',user='root',passwd='')

from monitor.table_info import my_table,get_table

if __name__ == '__main__':
    #插入设备基本信息表
    record1 = {\
               "device_name":"SV123456789",\
               "device_ip":"192.168.140.82",\
               "device_access":"test",\
               "device_access_interval":"test",\
               "manage_access_interval":"test",\
               "manage_access":"test"\
           }

    tb = get_table("device_info")

    insert_str = tb.insert_str(record1)
    mdb.execute_sql(insert_str,"virus")

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
    mdb.execute_sql(insert_str,"virus")

    #插入探针型号信息表
    record3 = {\
               "device_type":"ruixing",\
               "brand":"unknown",\
               "coding_type":"test",\
               "matching_rule":"test",\
               "matching_position":"test"\
           }

    tb = get_table("probe_type_info")

    insert_str = tb.insert_str(record3)
    mdb.execute_sql(insert_str,"virus")
    
