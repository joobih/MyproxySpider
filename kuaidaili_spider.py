#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append("submodule/BaseSpider")

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from base_spider import BaseSpider
import useful
import ConfigParser
import httplib
import time

httplib.HTTPConnection.debuglevel = 1

from model.models import *

class KuaidailiSpider(BaseSpider):

    def __init__(self):
        BaseSpider.__init__(self)

        #子类调用父类方法的其他方式
#        super(KuaidailiSpider,self).__init__(url)

    def parser_data(self,html):
        try:
            html = html.decode("utf-8")
            bs = BeautifulSoup(html,"html.parser")
            ip_dict = []
            divs = bs.find_all("div",id = "list")
            if not divs:
                print "html have not ip list"
                return []
            divs = divs[0]
            tbody = divs.find_all("tbody")
            if not tbody:
                return []
            tbody = tbody[0]
            trs = tbody.find_all("tr")
            for tr in trs:
                tds = tr.find_all("td")
                ip = tds[0].text
                port = tds[1].text
                anonymous = tds[2].text
                protocol_type = tds[3].text
                support = "GET/POST"                 #GET/POST
                address = tds[4].text
                respond_speed = tds[5].text
                respond_speed = float(respond_speed[:-1])
                last_verification = tds[6].text
                is_available = "NO"
                fail_time_start = datetime.now()
                data = {
                    "ip":ip,
                    "port":port,
                    "anonymous":anonymous,
                    "protocol_type":protocol_type,
                    "support":support,
                    "address":address,
                    "respond_speed":respond_speed,
                    "last_verification":last_verification,
                    "fail_time_start":fail_time_start,
                    "is_available":is_available
                }
                ip_dict.append(data)
            return ip_dict
        except Exception,e:
            print "KuaidailiSpider parser_data occure a Exception:{}".format(e)
            return None

    def parser_url(self):
        urls = []
        for i in range(1,1475):
            url = "http://www.kuaidaili.com/free/inha/{}/".format(i)
            urls.append(url)
            url = "http://www.kuaidaili.com/free/intr/{}/".format(i)
            urls.append(url)
            url = "http://www.kuaidaili.com/free/outtr/{}/".format(i)
            urls.append(url)
            url = "http://www.kuaidaili.com/free/outha/{}/".format(i)
            urls.append(url)
#            print url
        return urls

    @db_session
    def save_to_db(self,data):
        print data
        try:
            for d in data:
                p = get(p for p in Proxy if p.ip == d["ip"] and p.port == d["port"])
                if not p:
                    new_ip = Proxy(ip = d["ip"],port = d["port"],anonymous = d["anonymous"],protocol_type = d["protocol_type"],
                                  support = d["support"],address = d["address"],respond_speed = d["respond_speed"],
                                  last_verification = d["last_verification"],fail_time_start = d["fail_time_start"],is_available = d["is_available"])
                    commit()
        except Exception,e:
            print "KuaidailiSpider save_to_db occure a Exception:{}".format(e)
            return

    def run(self):   
#        html = self.index()
        urls = self.parser_url()
#        result = []
        proxy = {
            "http":"http://118.123.245.154:3128"
        }
        for u in urls:
            print u
            r = self.s.get(u,headers = self.headers)#,proxies = proxy)
            time.sleep(2)
            html = r.content
            print html
            data = self.parser_data(html)
            if data: 
                self.save_to_db(data)
                #result.extend(data)
#        return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "python _spider.py *.conf"
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

    kuaidaili_spider = KuaidailiSpider()
    kuaidaili_spider.run()
