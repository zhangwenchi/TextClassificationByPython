import urllib.request
import threading
import http.cookiejar

inFile = open('CrawlingData/proxy.txt', 'r')
outFile = open('CrawlingData/Avaproxy.txt', 'w')
url = 'http://www.lindenpat.com'
lock = threading.Lock()

def checkTheProxy():
    lock.acquire()
    line = inFile.readline().strip()
    lock.release()
    protocol, proxy = line.split('=')
    try:
        proxy_support = urllib.request.ProxyHandler({protocol.lower():'://'.join(line.split('='))})
        opener = urllib.request.build_opener(proxy_support,urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        request = urllib.request.Request(url)

        #print(urllib.request.urlopen(request,timeout=4).read())
        # cookie
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        r = opener.open(request,timeout=4)
        content = r.read()
        if len(content) >= 1000:
            lock.acquire()
            print('add ' + proxy)
            outFile.write('\"%s\",\n' %proxy)
            lock.release()
        else:
            print('出现验证码或IP被封杀')
    except Exception as e:
        print(e)

allthread = []
for i in range(639):
    t = threading.Thread(target=checkTheProxy)
    allthread.append(t)
    t.start()

for t in allthread:
    t.join()

inFile.close()
outFile.close()
