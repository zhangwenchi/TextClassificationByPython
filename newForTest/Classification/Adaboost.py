import os
import random
from sklearn.ensemble import AdaBoostClassifier
from scipy.sparse import csr_matrix

Vdir = '..\CleanData\VectorOfNews'
fileList = os.listdir(Vdir)
target = []
for i in range(len(fileList)):
    target.append(fileList[i].split('.')[0])

trainDatar = []
trainDatac = []
trainLabel = []
testDataR = []
testDataC = []
testLabel = []

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
word = []
f = open('RFdata\\word.txt', 'r')
for line in f.readlines():
    word.append(line.split('\n')[0])
f.close()

for i in range(len(trainLabel)):
    trainLabel[i] = target.index(trainLabel[i])

for i in range(len(testLabel)):
    testLabel[i] = target.index(testLabel[i])

trainMatrix = csr_matrix(([1]*len(trainDatar), (trainDatar, trainDatac)), shape=(trainDatar[-1]+1, len(word)))
testMatrix = csr_matrix(([1]*len(testDataR), (testDataR, testDataC)), shape=(testDataR[-1]+1, len(word)))

clf = AdaBoostClassifier(n_estimators=200, learning_rate=0.5)
clf.fit(trainMatrix, trainLabel)
ans = clf.predict(testMatrix)
error = 0.0
for i in range(len(ans)):
    if ans[i] != testLabel[i]:
        error += 1

print("error rate is %f" % (error/len(ans)))

# error rate is 0.357717