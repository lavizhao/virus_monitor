# virus_monitor
主要有一个监控病毒的server, 和数据库建表文件和一些常用的处理函数

##文件夹作用

`monitor/` 监控程序防止的位置
`util` 常用函数存放位置, 这个主要是为了方便日后其他人调用
`test` 测试

##执行

###monitor

`./create_db.py` 建立数据库, 执行main函数则建数据库, 建表, drop则删除整个数据库

###test

`./db.py` 测试table的一些基本命令, 数据库的命令没有测试, 因为不好测, 都是实际写的

