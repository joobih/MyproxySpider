#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append("supmodule/CSpider")

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from c_spider import CSpider


class KuaidailiSpider(CSpider):

    def __init__(self):
        CSpider.__init__(self)

    def parser_data(self,html):
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

    def parser_url(self):

        
