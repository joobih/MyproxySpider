#!/usr/bin/env python
# coding=utf-8

import requests

#url = "https://www.baidu.com"
url = "http://httpbin.org/ip"
headers = { 'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)' }
timeout = 10
proxy = {
#    "http":"http://121.232.146.13:9001",
#    "https":"https://110.73.1.114:8123",
#    "http":"http://110.73.1.114:8123"
#    "http":"http://58.46.153.245:8118",
#    "http":"http://27.46.22.43:8888"
#    "http":"http://58.99.43.1"
#    "http":"http://218.62.227.131:8998"
#    "http":"http://183.159.9.10:8998"
#    'http':'http://183.154.215.85:9000'
#    'http':'http://183.31.251.29:9797'
#    'http':'http://111.76.133.177:808'
#    'http':'http://27.206.212.23:9999'
    "http":"http://118.123.245.154:3128"
}
#s = requests.Session()
#r = s.get(url,proxies = proxy,headers = headers,timeout = timeout)
html=requests.get('http://httpbin.org/ip',proxies=proxy,timeout=10)
print html.content
