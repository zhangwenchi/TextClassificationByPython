import os
import jieba as ji
import re

dataDir = '../Crawling/CrawlingData/NewsContent'
dirList = os.listdir(dataDir)
# print(dirList)
typeName = []
for i in range(len(dirList)):
    typeName.append(dirList[i].split('.')[0])
# print(typeName)
data = []
for i in range(len(dirList)):
    t = []
    f = open(dataDir + '/' + dirList[i], 'r', encoding='utf-8')
    for line in f.readlines():
        if len(line) < 15:
            continue
        t.append(line[:-1])
    data.append(t)

# jieba.analyse.set_stop_words('D:\\Python27\\stopword.txt')
# tags = jieba.analyse.extract_tags(text,20)

stopwords = open('stopwords', 'r', encoding='utf-8').readlines()
for i in range(len(stopwords)):
    stopwords[i] = stopwords[i][:-1]

for i in range(len(dirList)):
    f = open('FenciByjieba/%s'%dirList[i], 'w', encoding='utf-8')
    for j in range(len(data[i])):
        st = " ".join(ji.cut(data[i][j]))
        st = re.sub(r'([\d]+)', '', st)
        stList = st.split(' ')
        stList = [word for word in stList if word not in stopwords]
        anst = ""
        for k in range(len(stList)):
            anst += stList[k] + " "
        anst += '\n'
        f.write(anst)


