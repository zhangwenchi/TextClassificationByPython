# -*- coding:utf-8 -*-
import urllib.request
import threading
import http.cookiejar
import os

import time
from bs4 import BeautifulSoup

# https://m.sohu.com/n/495353418/
# http://m.sohu.com/cr/57/?page=1&v=2   (international news)

inFile = open('CrawlingData/Avaproxy.txt', 'r')
url = ['http://m.sohu.com/cr/57/?page=%s&_smuid=1qCppj0Q1MiPQWJ4Q8qOj1&v=2',  # international
       'http://m.sohu.com/cr/32/?page=%s&_smuid=1qCppj0Q1MiPQWJ4Q8qOj1&v=2',  # home
       'http://m.sohu.com/cr/53/?page=%s&_smuid=1qCppj0Q1MiPQWJ4Q8qOj1&v=2',  # social
       'http://m.sohu.com/cr/20/?page=%s&_smuid=1qCppj0Q1MiPQWJ4Q8qOj1&v=2',  # health
       'http://m.sohu.com/cr/15/?page=%s&_smuid=1qCppj0Q1MiPQWJ4Q8qOj1&v=2',  # star
       'http://m.sohu.com/cr/61/?page=%s&_smuid=1qCppj0Q1MiPQWJ4Q8qOj1&v=2',  # tech
       'http://m.sohu.com/cr/70/?page=%s&_smuid=1qCppj0Q1MiPQWJ4Q8qOj1&v=2',  # weapon
       'http://m.sohu.com/cr/80/?page=%s&_smuid=1qCppj0Q1MiPQWJ4Q8qOj1&v=2',  # sports
       'http://m.sohu.com/cr/100/?page=%s&_smuid=1qCppj0Q1MiPQWJ4Q8qOj1&v=2'  # fashion
       ]
feature = ['international', 'home', 'social', 'health', 'star', 'tech', 'weapon', 'sports', 'fashion']
lock = threading.Lock()
proxy = []
for iq in range(10):
    x = inFile.readline().split('"')[1]
    proxy.append(x)

def getNews(url, typex):
    # print(url + " " + typex)
    if not os.path.exists('CrawlingData/NewsLink/%s' % typex):
        os.makedirs('CrawlingData/NewsLink/%s' % typex)
    file1 = open('CrawlingData/NewsLink/%s/link.txt' % typex, 'a')
    file1.write('https://m.sohu.com' + url + '\n')


def crawling(url, proxy, typex):
    for k in range(1, 100):
        time.sleep(0.5)
        print(typex + str(k))
        urlx = url % k
        try:
            proxy_support = urllib.request.ProxyHandler({'http':'://'.join(proxy)})
            opener = urllib.request.build_opener(proxy_support,urllib.request.HTTPHandler)
            urllib.request.install_opener(opener)
            request = urllib.request.Request(urlx)
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; \
                        WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')

            # cookie
            cj = http.cookiejar.CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
            r = opener.open(request,timeout=4)
            content = r.read()
            if len(content) >= 1000:
                lock.acquire()
                bs = BeautifulSoup(content, "lxml")
                tr = bs.findAll("div", {"class": "bd3 pb1"})
                urr = str(tr)
                xiabiao = 0
                while True:
                    qwe = urr.find('n',xiabiao)
                    if(qwe == -1):
                        break
                    else :
                        if(urr[qwe-1:qwe+12][1] != 'n'):
                            continue
                        getNews(urr[qwe-1:qwe+12], typex)
                    xiabiao = qwe + 12
                    #print(urIuse)

                lock.release()
            else:
                print('出现验证码或IP被封杀')
        except Exception as e:
            print(e)

allthread = []
for i in range(9):
    t = threading.Thread(target=crawling, args=(url[i], proxy[i], feature[i],))
    allthread.append(t)
    t.start()
for t in allthread:
    t.join()

inFile.close()




