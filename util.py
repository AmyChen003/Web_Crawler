import requests
import bs4
import time
import sys
import ipaddress

proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
proxyUser = "H4SWG38D0B862X4D"
proxyPass = "28A0E3887023FCA7"

print(proxyUser, proxyPass)

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

headers = { "Accept":"text/html,application/xhtml+xml,application/xml;9=0.9,*/*;q=0.8",
            "Accept-Encoding":"gzip,deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "X-Forwarded-For": "2.1.1.6",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "Upgrade-Insecure-Requests":"1",
            "Host" : "china.findlaw.cn",
            "Referer":"http://china.findlaw.cn/",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0"
            }

headers_post = { "Accept":"text/html,application/xhtml+xml,application/xml;9=0.9,*/*;q=0.8",
            "Accept-Encoding":"gzip,deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "X-Forwarded-For": "2.1.1.6",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "Upgrade-Insecure-Requests":"1",
            "Host" : "china.findlaw.cn",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer":"http://china.findlaw.cn/",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0"
            }

aa = ipaddress.IPv4Address('88.88.98.88')
aaa = ipaddress.IPv4Address('88.88.98.88')

requests.encoding='utf-8'


def get_soup(url):
    global aa
    global aaa
    global headers
    soup = None
    page = None
    while soup is None:
        while page is None:
            try:
                headers['X-Forwarded-For'] = str(ipaddress.IPv4Address(aa))
                headers_post['X-Forwarded-For'] = str(ipaddress.IPv4Address(aaa))
                aa+=1
                aaa+=1
                page = requests.get(url, timeout=2,headers=headers)
                # print(page.text)
            except Exception:
                page=None
        soup = bs4.BeautifulSoup(page.text, "lxml")
    return soup


def get_dynamic_content (qid,aid_list):
    payload = "qid="+str(qid)
    for item in aid_list:
        payload+="&aids%5B%5D="+str(item)
    response = None
    while response is None:
        try:
            response = requests.post('http://china.findlaw.cn/ask_front/?m=ask&c=ajax&a=updateQuesClicks',timeout=2,
                                     data=payload, headers=headers_post)
        except Exception:
            response = None
    return response.json()
