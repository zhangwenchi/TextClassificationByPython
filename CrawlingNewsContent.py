# -*- coding:utf-8 -*-
import urllib.request
import threading
import http.cookiejar
import time
import os
from bs4 import BeautifulSoup


proxyFile = open('CrawlingData/Avaproxy.txt','r')
nproxy = []
for geshu in proxyFile.readlines():
    nproxy.append(geshu.split('"')[1])

lock = threading.Lock()

dict = {'international':0, 'home':0, 'social':0, 'health':0, 'star':0, 'tech':0, 'weapon':0, 'sports':0, 'fashion':0}

def getTheContent(nproxy, ntype, nfile):
    # print(ntype)
    i = 0
    for line in nfile.readlines():
        i += 1
        print(ntype + " " + str(i))
        if(len(line) < 2 or line[-2] != '/'):
            continue
        # else:
        #     print(line)
        proxy_support = urllib.request.ProxyHandler({'http': '://'.join(nproxy)})
        opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        request = urllib.request.Request(line)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; \
                        WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')
        # cookie
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        r = opener.open(request, timeout=4)
        content = r.read()
        if len(content) >= 1000:
            lock.acquire()
            news = ""
            bs = BeautifulSoup(content, "lxml")
            tr = bs.findAll("p", {"class": "para"})
            for trr in tr:
                if trr.string is not None:
                    news += trr.string
            if os.path.exists('CrawlingData/NewsContent/%s'%ntype):
                file = open('CrawlingData/NewsContent/%s'%ntype + '/' + '%s.txt' % dict[ntype], 'w',encoding='utf-8')
                file.write(news)
            else:
                os.makedirs('CrawlingData/NewsContent/%s'%ntype)
                file = open('CrawlingData/NewsContent/%s' % ntype + '/' + '%s.txt' % dict[ntype], 'w',encoding='utf-8')
                file.write(news)
            dict[ntype] += 1
            lock.release()
        else:
            print('出现验证码或IP被封杀')

allthread = []
dirlist = os.listdir('CrawlingData/NewsLink')
file = []
for i in range(10):
    file.append([])
for i in range(9):
    file[i] = open('CrawlingData/NewsLink/%s/link.txt' % dirlist[i], 'r')
    t = threading.Thread(target=getTheContent, args=(nproxy[i], dirlist[i], file[i],))
    allthread.append(t)
    t.start()

for t in allthread:
    t.join()



