#!/usr/bin/env python
# coding=utf-8

from pony.orm import *

from db import db
from datetime import datetime

class Proxy(db.Entity):
    ip = Optional(str)              #ip地址
    port = Optional(str)            #port端口号
    anonymous = Optional(str)       #匿名度 (高匿名)
    protocal_type = Optional(str)   #协议类型(HTTP--0,HTTPS--1,SOCKE5--2)
    support = Optional(str)         #GET/POST 支持(GET--0,POST--1)
    address = Optional(str)         #地址,位置
    respond_speed = Optional(int)   #响应速度
    last_verification = Optional(datetime)  #最后响应时间
    is_available = Optional(str)    #是否可用  YES,NO

