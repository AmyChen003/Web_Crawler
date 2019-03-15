import requests
import bs4
import time
import sys
import ipaddress

# proxyHost = "http-dyn.abuyun.com"
# proxyPort = "9020"
# proxyUser = "HD095H69R92IQ34D"
# proxyPass = "7F8555939DE4200A"
#
# print(proxyUser, proxyPass)
#
# proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
#     "host": proxyHost,
#     "port": proxyPort,
#     "user": proxyUser,
#     "pass": proxyPass,
# }
#
# proxies = {
#     "http": proxyMeta,
#     "https": proxyMeta,
# }

headers = { "Accept":"text/html,application/xhtml+xml,application/xml;9=0.9,*/*;q=0.8",
            "Accept-Encoding":"gzip,deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "X-Forwarded-For": "1.1.1.5",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "Upgrade-Insecure-Requests":"1",
            "Host": "www.66law.cn",
            "Referer": "http://www.66law.cn/",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0"
            }

aa = ipaddress.IPv4Address('88.88.88.88')

requests.encoding='utf-8'


def get_soup(url):
    global aa
    global headers
    soup = None
    page = None
    while soup is None:
        while page is None:
            try:
                headers['X-Forwarded-For'] = str(ipaddress.IPv4Address(aa))
                aa+=1
                page = requests.get(url, timeout=2,headers=headers)
                # print(page.text)
            except Exception:
                page=None
        soup = bs4.BeautifulSoup(page.text, "lxml")
    return soup


