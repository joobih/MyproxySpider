#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append("submodule/BaseSpider")
sys.path.append("submodule/Common")

from datetime import datetime
import time
import requests
from threading import Thread
import ConfigParser

from proxy_check import proxy_check
from model.models import *


class SearchServer(Thread):
    def __init__(self):
        Thread.__init__(self)

    @db_session
    def run(self):
        while True:
            s = time.time()
            all_p = select(p for p in Proxy)
            for p in all_p:
                result = proxy_check(p.ip,p.port)
                if result and result["is_available"]:
                    p.is_available = "YES"
                    p.last_verification = datetime.now()
                    p.fail_time_start = datetime.now()
                    p.respond_speed = result["respond_speed"]
                    print p.ip,p.port,"YES"
                    commit()
            e = time.time()
            print "check all ip use time:{}".format(e-s)
            time.sleep(60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "python search.py *.conf"
        exit(0)
    conf_file = sys.argv[1]
    conf = ConfigParser.ConfigParser()
    conf.read(conf_file)
    m_host = conf.get("mysql","host")
    m_db = conf.get("mysql","db")
    m_user = conf.get("mysql","user")
    m_password = conf.get("mysql","password")
    db.bind("mysql",host = m_host,passwd = m_password,user = m_user,db = m_db)
    db.generate_mapping(check_tables = True,create_tables = True)
    t = SearchServer()
    t.start()
