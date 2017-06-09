from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import os
from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

Vdir = '..\CleanData\VectorOfNews'
fileList = os.listdir(Vdir)
target = []
Labels = []
DataR = []
for i in range(len(fileList)):
    target.append(fileList[i].split('.')[0])
Corpus = []
for i in range(len(fileList)):
    f = open('..\CleanData\FenciByjieba' + '\%s' % fileList[i], 'r', encoding='utf-8')
    y = ""
    for line in f.readlines():
        DataR.append(list(set(line.split(' '))))
        Labels.append(target[i])
        y += line + " "
    Corpus.append(y)

vectorizer = CountVectorizer(vocabulary=None, max_df=50, min_df=5)  # if a word appears more than 50 times or less than 5 times
#
# The most important things is that I can change sparse to array by this Selection!
#
transformer = TfidfTransformer()
vectorizer.fit_transform(Corpus)
word = vectorizer.get_feature_names()  # keywords of all the text
freMatrix = vectorizer.fit_transform(Corpus).toarray()

trainDatar = []
trainDatac = []
trainLabel = []
testDataR = []
testDataC = []
testLabel = []

# trainRow = 0
# testRow = 0
# for i in range(len(DataR)):
#     for j in range(len(DataR[i])):
#         try:
#             index = word.index(DataR[i][j])
#             if i % 100 < 80:
#                 trainDatar.append(trainRow)
#                 trainDatac.append(index)
#             else:
#                 testDataR.append(testRow)
#                 testDataC.append(index)
#         except:
#             continue
#     if i % 100 < 80:
#         trainRow += 1
#         trainLabel.append(Labels[i])
#     else:
#         testRow += 1
#         testLabel.append(Labels[i])
#     if i % 1000 == 0:
#         print("now is :%d" % i)
#
# f = open('RFdata\\trainDatar.txt', 'w')
# for r in trainDatar:
#     f.write(str(r))
#     f.write('\n')
# f.close()
# f = open('RFdata\\testDatar.txt', 'w')
# for r in testDataR:
#     f.write(str(r))
#     f.write('\n')
# f.close()
# f = open('RFdata\\trainDatac.txt', 'w')
# for c in trainDatac:
#     f.write(str(c))
#     f.write('\n')
# f.close()
# f = open('RFdata\\testDataC.txt', 'w')
# for c in testDataC:
#     f.write(str(c))
#     f.write('\n')
# f.close()
# f = open('RFdata\\trainLabel.txt', 'w')
# for l in trainLabel:
#     f.write(str(l))
#     f.write('\n')
# f.close()
# f = open('RFdata\\testLabel.txt', 'w')
# for l in testLabel:
#     f.write(str(l))
#     f.write('\n')
# f.close()

f = open('RFdata\\trainDatar.txt', 'r')
for line in f.readlines():
    trainDatar.append(int(line.split('\n')[0]))
f.close()
f = open('RFdata\\trainDatac.txt', 'r')
for line in f.readlines():
    trainDatac.append(int(line.split('\n')[0]))
f.close()
f = open('RFdata\\trainLabel.txt', 'r')
for line in f.readlines():
    trainLabel.append(line.split('\n')[0])
f.close()
f = open('RFdata\\testDatar.txt', 'r')
for line in f.readlines():
    testDataR.append(int(line.split('\n')[0]))
f.close()
f = open('RFdata\\testDataC.txt', 'r')
for line in f.readlines():
    testDataC.append(int(line.split('\n')[0]))
f.close()
f = open('RFdata\\testLabel.txt', 'r')
for line in f.readlines():
    testLabel.append(line.split('\n')[0])
f.close()

trainMatrix = csr_matrix(([1]*len(trainDatar), (trainDatar, trainDatac)), shape=(trainDatar[-1]+1, len(word)))
testMatrix = csr_matrix(([1]*len(testDataR), (testDataR, testDataC)), shape=(testDataR[-1]+1, len(word)))

clf = RandomForestClassifier(n_estimators=200, n_jobs=10)
clf.fit(trainMatrix, trainLabel)
ans = clf.predict(testMatrix)
error = 0.0
for i in range(len(testLabel)):
    if ans[i] != testLabel[i]:
        error += 1

print('error rate is :' + str(error/len(testLabel)))
joblib.dump(clf, 'RF.pkl')

# error rate is :0.13446088794926003 !!!!



