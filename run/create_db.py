#!/usr/bin/python3

'''
建表
'''

import sys
sys.path.append("..")

from monitor.table_info import drop,drop_table,main

if __name__ == '__main__':
    drop()
    main()
    #drop_table()


