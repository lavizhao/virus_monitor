# virus_monitor
主要有一个监控病毒的server, 和数据库建表文件和一些常用的处理函数

##执行

### for run

`sudo ./server.py` ，配置文件均在`server.conf`上

### for test

`./client.py`

###打成二进制

`cd run`

`pyinstaller --onefile -p ../ server.py`

请将`server.conf`拷入dist文件夹下使用
