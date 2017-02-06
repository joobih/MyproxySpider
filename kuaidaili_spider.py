#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append("supmodule/BaseSpider")

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from base_spider import BaseSpider
import useful
import ConfigParser

from model.models import *

class KuaidailiSpider(BaseSpider):

    def __init__(self):
        BaseSpider.__init__(self)

        #子类调用父类方法的其他方式
#        super(KuaidailiSpider,self).__init__(url)

    def parser_data(self,html):
        try:
            bs = BeautifulSoup(html,"html.parser")
            ip_dict = []
            divs = bs.find_all("div",id = "list")[0]
            tbody = divs.find_all("tbody")[0]
            trs = tbody.find_all("tr")
            for tr in trs:
                tds = tr.find_all("td")
                ip = tds[0].text
                port = tds[1].text
                anonymous = tds[2].text
                protocol_type = tds[3].text
                support = 0                 #GET/POST
                address = tds[4].text
                respond_speed = tds[5].text
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
                    "fail_time_start":fail_time_start
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
            urls = "http://www.kuaidaili.com/free/outtr/{}/".format(i)
            urls.append(url)
            url = "http://www.kuaidaili.com/free/outha/{}/".format(i)
            urls.append(url)
        return urls

    @db_session
    def save_to_db(data):
        try:
            for d in data:
                p = get(p for p in Porxy if p.ip == d["ip"] and p.port == d["port"])
                if not p:
                    new_ip = Proxy(ip = d["ip"],port = d["port"],anonymous = d["anonymous"],protocol_type = d["protocol_type"],
                                  support = d["support"],address = d["address"],respond_speed = d["respond_speed"],
                                  last_verification = d["last_verification"],fail_time_start = d["fail_time_start"])
                    commit(new_ip)
        except Exception,e:
            print "KuaidailiSpider save_to_db occure a Exception:{}".format(e)
            return


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "python _spider.py *.conf"
        exit(0)
    conf_file = sys.argv[1]
    conf = ConfigParser.ConfigParser()
    conf.read(conf_file)
    m_host = conf.get("msyql","host")
    m_db = conf.get("mysql","db")
    m_user = conf.get("mysql","user")
    m_password = conf.get("mysql","password")
    db.bind("mysql",host = m_host,passwd = m_password,user = m_user,db = m_db)
    db.generate_mapping(check_tables = True,create_tables = True)

    kuaidaili_spider = KuaidailiSpider()
    kuaidaili_spider.run()
