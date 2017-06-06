import os
import json

dataDir = '../Crawling/CrawlingData/NewsContent'
dirList = os.listdir(dataDir)
# typeName = []
# for i in range(len(dirList)):
#     typeName.append(dirList[i].split('.')[0])
data = []
for i in range(len(dirList)):
    file = open('FenciByjieba/%s'%dirList[i], 'r', encoding='utf-8')
    xdata = []
    for line in file.readlines():
        xdata.append(line[:-1].split(' '))
    data.append(xdata)
# print(data)
# data is the cleaned words of every news of every type
dict = {}
for i in range(len(data)):
    for j in range(len(data[i])):
        for k in range(len(data[i][j])):
            if data[i][j][k] in dict.keys():
                dict[data[i][j][k]] += 1
            else:
                dict[data[i][j][k]] = 1

# sorted dict (type is list), and the element from the list is like ('str', frequency)
wordf = sorted(dict.items(), key=lambda d:d[1], reverse=True)

jsObj = json.dumps(wordf)
fileObject = open('dictFile.json', 'w', encoding='utf-8')
fileObject.write(jsObj)
fileObject.close()

words = []
for i in range(len(wordf)):
    words.append(wordf[i][0])

# print(len(words))
# 148693 unique words totally

for i in range(len(data)):
    f = open('VectorOfNews/%s'%dirList[i], 'w', encoding='utf-8')
    st = ""
    for j in range(len(data[i])):
        for k in range(len(data[i][j])):
            st += str(words.index(data[i][j][k])) + " "
        st += '\n'
    f.write(st)
    print('now is file %s'%dirList[i])




