#!/usr/bin/python3
#coding: utf-8

'''
这个脚本的目的是管理mysql中的表数据
'''
import sys

#import pymysql as mysql
import mysql.connector
import logging 

class mydb:
    def __init__(self,host,port,user,passwd):
        self.count = 0
        #设置mysql连接
        try:
            self.conn = mysql.connector.connect(host=host,user=user,passwd=passwd,port=port)
        except Exception as err:
            logging.error(err)

    def create_db(self,db_name):
        try:        
            cur = self.conn.cursor()
            cur.execute("CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARSET utf8"%(db_name))
            self.conn.commit()
        except Exception as err:
            logging.error(err)

    def drop_db(self,db_name):
        try :
            cur = self.conn.cursor()
            cur.execute("drop database if exists %s;"%(db_name))
            self.conn.commit()
        except Exception as err:
            logging.error(err)

    def execute_sql(self,sql_str,db_name):
        try :
            cur = self.conn.cursor()
            cur.execute("use %s"%(db_name))
            cur.execute(sql_str)
            self.conn.commit()
        except Exception as err:
            logging.error(err)

    def insert_sql(self,sql_str,db_name):
        try :
            self.count += 1
            cur = self.conn.cursor()
            cur.execute("use %s"%(db_name))
            cur.execute(sql_str)
            if self.count % 1 == 0:
                self.conn.commit()
                self.count = 0
        except Exception as err:
            logging.error(err)

        
    def select_sql(self,sql_str,db_name):
        try:
            cur = self.conn.cursor()
            
            cur.execute("use %s"%(db_name))
            cur.execute(sql_str)
            
            result = cur.fetchall()
            #self.conn.commit()
            
            return result
            
        except Exception as err:
            logging.error(err)
            logging.error("select error")

