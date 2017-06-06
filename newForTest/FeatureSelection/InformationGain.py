import os
import json
import math
import threading

# This method is sooooooo time consuming...................
# run at 2017/06/06 15:06 to 17:50

# it's a shame that I did not sotre the dict of the whole words
# I store it ! using json
Vdir = '..\CleanData\VectorOfNews'
fileList = os.listdir(Vdir)

# get the list of all the words freq
dictList = []
f = open("..\CleanData\dictFile.json","r")
for line in f:
    dictList.append(json.loads(line))
f.close()

# get the amount of document
numDocument = []
for i in range(len(fileList)):
    f = open('..\Crawling\CrawlingData\\NewsContent' + '\%s'%fileList[i], 'r',encoding='utf-8')
    amount = 0
    numDocument.append(int(f.readlines()[-1].split(':')[0]))
# print(numDocument)
sumDocument = sum(numDocument)
# print(sumDocument)

# IG(T)=H(C) - H(C|T)
# H(C) = sum(p*log(p)) --- same for all
# H(C|T) = -Pt*sum(P(Ci|t)*log(P(Ci|t))) - Ptb*sum(P(Ci|tb)*log(P(Ci|tb)))
# get a 3-D list for all the words
VectorOfWords = []
for i in range(len(fileList)):
    f = open(Vdir + '\%s'%fileList[i], 'r')
    t = []
    for line in f.readlines():
        t.append(line.split(' '))
    VectorOfWords.append(t)

# print(VectorOfWords)

# ig(x) = Pt*sum(P(Ci|t)*log(P(Ci|t))) + Ptb*sum(P(Ci|tb)*log(P(Ci|tb)))
# i want to get top 5000 words
Feature = []
HC = 0
for i in range(len(VectorOfWords)):
    p = numDocument[i] / sumDocument
    HC -= p * math.log2(p)


dictOfFre = {}

def IG(i):

    for j in range(len(VectorOfWords[i])):
        print(str(i) + ' : ' + str(j))
        for k in range(len(VectorOfWords[i][j])):
            x = VectorOfWords[i][j][k]
            if x in dictOfFre.keys():
                continue
            s = 0
            pp = [0] * len(VectorOfWords)
            for iq in range(len(VectorOfWords)):
                for jq in range(len(VectorOfWords[iq])):
                    if x in VectorOfWords[iq][jq]:
                        s += 1
                        pp[iq] += 1
            Pt = s / sumDocument
            Ptb = 1 - Pt
            Pcit = [0] * len(VectorOfWords)
            Pcitb = [0] * len(VectorOfWords)
            for iw in range(len(VectorOfWords)):
                Pcit[iw] = pp[iw] / s

            for iw in range(len(VectorOfWords)):
                Pcitb[iw] = 1 - Pcit[iw]
            ans = 0
            for iw in range(len(VectorOfWords)):
                if(Pcitb[iw] <= 0.0):
                    ans += Pt * (Pcit[iw]*math.log2(Pcit[iw]))
                elif Pcit[iw] <= 0.0:
                    ans += Ptb * (Pcitb[iw] * math.log2(Pcitb[iw]))
                else:
                    ans += (Pt * (Pcit[iw] * math.log2(Pcit[iw])) + Ptb * (Pcitb[iw] * math.log2(Pcitb[iw])))

            dictOfFre[x] = (-ans)
            # print('ans:' + str(dictOfFre[VectorOfWords[i][j][k]]))
    # the last time should be right
    wordf = sorted(dictOfFre.items(), key=lambda d: d[1], reverse=False)
    jsObj = json.dumps(wordf)
    fileObject = open('IG.json', 'w', encoding='utf-8')
    fileObject.write(jsObj)
    fileObject.close()
# I think I need the words that can show the feature ???
# so I need the small IG words ???
## ok, I got it that information gain can only get the words which can represent the whole content,
## it cannot represent one kingd of news @@@@@@@@ so ....???? Maybe try another way.



# here can use a heap to store top 5000
# python heapq - -

# have to use = =
allthread = []
for i in range(9):
    t = threading.Thread(target=IG, args=(i,))
    allthread.append(t)
    t.start()
for t in allthread:
    t.join()




