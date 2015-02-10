#!/usr/bin/python3

import sys
sys.path.append("..")

import unittest

from monitor.db_info import field,kvtuple,table

class test(unittest.TestCase):

    def testField(self):
        f = field()
        self.assertEqual(f['ip'],"varchar(40)")
        self.assertEqual(f.normal,"varchar(150)")
        self.assertEqual('port' in f,True)
        self.assertEqual('hehe' in f,False)


    def testKvtuple(self):
        k = 'device_name'
        v = 'port'

        kv = kvtuple(k,v)
        self.assertEqual(str(kv),"device_name varchar(20)")

        kv = kvtuple(k,v,is_pk=True)
        self.assertEqual(str(kv),"device_name varchar(20) PRIMARY KEY")

        kv = kvtuple(k,v,is_pk=True,is_auto=True)
        self.assertEqual(str(kv),"device_name varchar(20) PRIMARY KEY AUTO_INCREMENT")


    def testTable(self):
        ndict = [\
                 ('indx',['int',1,1]),\
                 ('mip',['ip'])\
             ]    
        
        tbl = table("example",ndict)
        print(tbl.sql_str())
        
if __name__ == '__main__':
    unittest.main()
