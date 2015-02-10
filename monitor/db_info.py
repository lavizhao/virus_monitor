'''
存储db信息, 写死在里面了, 也没有必要单独弄
'''

import logging

pk_string = "PRIMARY KEY"
auto_string = "AUTO_INCREMENT"

#属性值大小
class field():
    def __init__(self):
        self.__value = {'ip':'varchar(40)',\
                        'port':'varchar(20)',\
                        'small':'varchar(50)',\
                        'normal' : 'varchar(150)',\
                        'big' : 'varchar(1000)',\
                        'large' : 'varchar(3000)',\
                        'datetime' : 'datetime',\
                        'int':'int'\
                    }

        for k in self.__value:
            v = self.__value[k]
            setattr(self,k,v)
        
    def __getitem__(self,k):
        return self.__value[k]

    def __contains__(self,k):
        return k in self.__value

nf = field()
        
#建值对, 比如device_name , normal, is_pk 是主键的意思
class kvtuple():
    def __init__(self,k,v,is_pk=False,is_auto=False):
        self.__key = k
        self.__value = v
        self.key = k
        self.value = v
        
        if self.__value not in nf:
            logging.error("kvtuple value %s not in field"%(self.__value))
            
        self.__is_pk = is_pk
        self.__is_auto = is_auto    

    #建表时候的字符串
    def __str__(self):
        result = "%s %s"%(self.__key,nf[self.__value])
        if self.__is_pk :
            result += " %s"%(pk_string)
        if self.__is_auto:
            result += " %s"%(auto_string)
            
        return result 


#表类
#表类支撑起整个create table的功能, 初始化用dict, + 表名, 来实现        
class table:
    def __init__(self,name,ndict):
        self.__name = name
        self.__ndict = ndict
        self.__kvtuple = []
        self.name = name
        
        for k,v in ndict:
            
            if len(v) >=3:
                kv = kvtuple(k,v[0],is_pk=True,is_auto=True)
            elif len(v) == 2:
                kv = kvtuple(k,v[0],is_pk=True)
            else:
                kv = kvtuple(k,v[0])

            self.__kvtuple.append(kv)

    #建表时候的创建语句
    def sql_str(self):
        result = "create table %s("%(self.__name)
        for indx in range(len(self.__kvtuple)):
            kv = self.__kvtuple[indx]
            if indx != len(self.__kvtuple) -1:
                result += "%s, "%(str(kv))
            else:
                result += "%s"%(str(kv))

        result += ")"
        return result

    def drop_str(self):
        return "drop table %s"%(self.__name)

    #ndict构成: {col1:value1,...} col表示字段, value表示值
    #注意, 插入的语句是这么写的 :  insert links (name,url) values('jerichen','gdsz'),('alone','gdgz');    
    def insert_str(self,ndict):
        result = "insert into %s("%(self.name)
        result1 = "values("
        
        for indx in range(len(self.__kvtuple)):
            kv = self.__kvtuple[indx]

            #字段
            col = kv.key

            #值 #注意, 这里没有考虑auto increment的情况
            try :
                if kv.value != "auto":
                    value = ndict[col]
                else:
                    pass

                result += "%s"%(col)
                result1 += "\'%s\'"%(value)
                    
            except Exception as err:
                logging.error(err)
                logging.error("引入非法字段")

            if indx != len(self.__kvtuple) -1:
                result += ", "
                result1 += ", "

        result += ")"
        result1 += ")"
        return result + result1
