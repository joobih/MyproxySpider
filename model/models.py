#!/usr/bin/env python
# coding=utf-8

from pony.orm import *

from db import db
from datetime import datetime

class Proxy(db.Entity):
    ip = Optional(str)              #ip地址
    port = Optional(str)            #port端口号
    anonymous = Optional(str)       #匿名度 (高匿名)
    protocol_type = Optional(str)   #协议类型(HTTP/HTTPS--0,HTTP--1,HTTPS--2,SOCKE5--3)
    support = Optional(str)         #GET/POST 支持(GET/POST--0,GET--1,POST--2)
    address = Optional(str)         #地址,位置
    respond_speed = Optional(int)   #响应速度
    last_verification = Optional(datetime)  #最后验证时间
    is_available = Optional(str)    #是否可用  YES,NO
    fail_time_start = Optional(datetime)    #累计失败起始时间 (当失败时间累计超过多少就考虑不验证该ip) 
