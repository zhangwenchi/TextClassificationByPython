import requests
import time
from bs4 import BeautifulSoup

# https://31f.cn/
# https://31f.cn/area/北京市/

def getTheProxy():
    of = open('CrawlingData/proxy.txt','w')
    url = 'https://31f.cn/'
    print("正在采集" + url)
    html = requests.get(url).text
    bs = BeautifulSoup(html,"lxml")
    #print(bs)
    tr = bs.findAll('tr')

    cityList = []

    for i in range(1, 50):
        td = tr[i].findAll('td')
        proxy_ip = td[1].text.strip()
        proxy_port = td[2].text.strip()
        cityList.append(td[3].text.strip())
        of.write('http=%s:%s\n' % (proxy_ip, proxy_port))
        print('http=%s:%s\n' % (proxy_ip, proxy_port))
    time.sleep(5)
    print(cityList)


    cityList = list(set(cityList))
    for i in range(len(cityList)):
        url = "https://31f.cn/area/" + cityList[i] + "/"
        print("正在采集" + url)
        html = requests.get(url).text
        bs = BeautifulSoup(html, "lxml")
        tr = bs.findAll('tr')

        for i in range(1, 50):
            td = tr[i].findAll('td')
            proxy_ip = td[1].text.strip()
            if proxy_ip[0]< '0' or proxy_ip[0] > '9': break
            proxy_port = td[2].text.strip()
            of.write('http=%s:%s\n' % (proxy_ip, proxy_port))
            print('http=%s:%s\n' % (proxy_ip, proxy_port))
        time.sleep(5)

    of.closed

getTheProxy()