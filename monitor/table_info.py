#!/usr/bin/python3
#coding: utf-8

'''
表的基本信息
'''

import logging

from .db_info import field,kvtuple,table
from .db import mydb

#mdb = mydb(host='localhost',port='3306',user='root',passwd='')
mdb = mydb(host='192.168.140.98',port='3306',user='root',passwd='hitjin')

mf = field()
tbl = []

#tbl 1.  控制设备信息表
tbl1 = (\
        "control_device_info",\
        [\
         ("device_name",      ["normal","pk"]),\
         ("management",       ["normal"]),\
         ("user_name",        ["normal"]),\
         ("user_password",    ["normal"]),\
         ("telnet_port",      ["port"]),\
         ("device_type",      ["normal"]),\
         ("network_segment",  ["big"])
     ]\
    )
tbl.append(tbl1)

#tbl 2. 控制设备型号信息表
tbl2 = (\
        "control_device_type_info",\
        [\
         ("device_type",     ["normal","pk"]),\
         ("brand",           ["normal"]),\
         ("control_command", ["normal"])\
     ]\
    )
tbl.append(tbl2)

#tbl 3. 探针日志信息表
tbl3 = (\
        "probe_log_info",\
        [\
         ("log_id",                ["int","pk","auto"]),\
         ("probe_ip",              ["ip"]),\
         ("log_level",             ["small"]),\
         ("virus_name",            ["normal"]),\
         ("virus_type",            ["normal"]),\
         ("infected_device_ip",    ["ip"]),\
         ("infected_device_port",  ["port"]),\
         ("spread_device_ip",      ["ip"]),\
         ("spread_device_port",    ["port"]),\
         ("infected_time",         ["datetime"])\
     ]\
    )
tbl.append(tbl3)

#tbl 4. 设备基本信息表
tbl4 = (\
        "device_info",\
        [\
         ("device_name",                ["normal","pk"]),\
         ("device_ip",                  ["ip"]),\
         ("device_access_interval",     ["small"]),\
         ("device_access",              ["small"]),\
         ("manage_access_interval",     ["small"]),\
         ("manage_access",              ["small"])\
     ]\
    )
tbl.append(tbl4)

#tbl 5. 探针信息表
tbl5 = (\
        "probe_info",\
        [\
         ("device_name",           ["normal","pk"]),\
         ("device_port",           ["port"]),\
         ("device_type",           ["normal"]),\
         ("virus_statistic",       ["normal"]),\
         ("network_segment",       ["big"])\
     ]\
    )
tbl.append(tbl5)

#tbl 6. 探针型号信息表
tbl6 = (\
        "probe_type_info",\
        [\
         ("device_type",              ["normal","pk"]),\
         ("brand",                    ["normal"]),\
         ("coding_type",              ["small"]),\
         ("matching_rule",            ["big"]),\
         ("matching_position",        ["big"])\
     ]\
    )
tbl.append(tbl6)

#tbl 7. 计划任务信息表
tbl7 = (\
        "plan_task_info",\
        [\
         ("task_id",        ["int","pk","auto"]),\
         ("task_name",      ["normal"]),\
         ("task_ip",        ["large"]),\
         ("task_operation", ["big"]),\
         ("device_name",    ["normal"]),\
         ("task_finish",    ["small"])\
     ]\
    )
tbl.append(tbl7)

#tbl 8. 时间计划表
tbl8 = (\
        "task_info",\
        [\
         ("task_id",     ["int","pk","auto"]),\
         ("task_period", ["normal"]),\
         ("task_time",   ["normal"]),\
         ("task_begin",  ["datetime"]),\
         ("task_end",    ["datetime"])\
     ]\
    )
tbl.append(tbl8)

#tbl 9.操作条件表
tbl9 = (\
        "operation_condition",\
        [\
         ("task_id",              ["int","pk","auto"]),\
         ("device_name",          ["normal"]),\
         ("trigger_condition",    ["normal"]),\
         ("trigger_threshold",    ["normal"])\
     ]\
    )
tbl.append(tbl9)

#tbl 10. 地址信息簿表
tbl10 = (\
         "address_info",\
         [\
          ("address_id",          ["int","pk","auto"]),\
          ("address_operation",   ["normal"]),\
          ("address_name",        ["normal"])\
      ]\
     )
tbl.append(tbl10)

#tbl 11. 白名单信息表
tbl11 = (\
         "white_list",\
         [\
          ("network_segment",   ["big"]),\
          ("network_mask",      ["ip"]),\
          ("device_name",       ["normal"]),\
          ("begin",             ["datetime"]),\
          ("duration",          ["normal"])\
      ]\
     )
tbl.append(tbl11)

#tbl 12. 黑名单信息表
tbl12 = (\
         "black_list",\
         [\
          ("network_segment",   ["big"]),\
          ("network_mask",      ["ip"]),\
          ("task_operation",    ["normal"]),\
          ("device_name",       ["normal"]),\
          ("begin",             ["datetime"]),\
          ("duration",          ["normal"])\
      ]\
     )
tbl.append(tbl12)

#13. web系统基本信息表
tbl13 = (\
         "system_info",\
         [\
          ("system_ip",           ["ip"]),\
          ("system_mask",         ["ip"]),\
          ("system_gateway",      ["ip"]),\
          ("system_port",         ["port"]),\
          ("system_timeout",      ["normal"]),\
          ("user_name",           ["normal"]),\
          ("user_password",       ["normal"])\
      ]\
     )
tbl.append(tbl13)

#tbl 14. 管理员信息表
tbl14 = (\
         "admin_info",\
         [\
          ("user_name",           ["normal"]),\
          ("user_password",       ["normal"]),\
          ("user_rights",         ["normal"]),\
          ("user_address",        ["big"]),\
          ("user_email",          ["normal"])\
      ]\
     )
tbl.append(tbl14)

#tbl15. 系统日志信息表
tbl15 = (\
         "system_log",\
         [\
          ("log_time",["datetime"]),\
          ("log_level",["small"]),\
          ("log_content",["normal"])\
      ]\
     )
tbl.append(tbl15)

my_table = []
for tb in tbl:
    my_table.append(table(tb[0],tb[1]))


def drop():
    mdb.drop_db("virus")

def drop_table():
    for tb in my_table:
        if tb.name == "white_list":
            mdb.execute_sql(tb.drop_str(),"virus")

def main():

    mdb.create_db("virus")
    for tb in my_table:
        mdb.execute_sql(tb.sql_str(),"virus")


def get_table(tb_name):
    for tb in my_table:
        if tb_name == tb.name:
            return tb

    logging.error("can not find table")
