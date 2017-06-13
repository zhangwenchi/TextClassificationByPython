# BP neural network is apt to 'forget' the data that at the beginning
# so I should shuffle the data ->>>>>> have to
# and the amount of the data should be similar

import os
from scipy.sparse import csr_matrix
import math
import numpy as np
import random

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

trainMatrix = csr_matrix(([1]*len(trainDatar), (trainDatar, trainDatac)), shape=(trainDatar[-1]+1, len(word))).toarray()
testMatrix = csr_matrix(([1]*len(testDataR), (testDataR, testDataC)), shape=(testDataR[-1]+1, len(word))).toarray()

def sigmoid(x):
    vec = []
    for i in x:
        vec.append(1/(1+math.exp(-i)))
    vec = np.array(vec)
    return vec

# print(trainMatrix.shape) (9520, 15046)
# input num is 15046
# invisible layer is inn -> 122
# output num is 9
# study rate = 0.2
# random w1, w2
# initial offset is 0
inn = int(math.sqrt(15046 + 9) + 0)
# inn = 20
numin = trainMatrix.shape[1]
numout = 9
inputRate = 0.2
hidRate = 0.2

def TrainNetwork():
    w1 = 0.2 * np.random.random((numin, inn)) - 0.1
    w2 = 0.2 * np.random.random((inn, numout)) - 0.1
    hidOffset = np.zeros(inn)
    outOffset = np.zeros(numout)
    c = list(zip(trainMatrix,trainLabel))
    random.shuffle(c)
    trainMatrix[:], trainLabel[:] = zip(*c)
    for i in range(len(trainMatrix)):
        print('train the %d data...'%i)
        trainMatrix[i] = np.array(trainMatrix[i])
        t_label = np.zeros(numout)
        t_label[trainLabel[i]] = 1

        hid_value = np.dot(trainMatrix[i],w1) + hidOffset
        hid_act = sigmoid(hid_value)
        out_value = np.dot(hid_act, w2) + outOffset
        out_act = sigmoid(out_value)

        err = t_label - out_act
        out_delta = err * out_act * (1 - out_act)
        hide_delta = hid_act * (1 - hid_act) * np.dot(w2, out_delta)
        for j in range(numout):
            w2[:,j] += hidRate * out_delta[j] * hid_act
        for j in range(inn):
            w1[:,j] += inputRate * hide_delta[j] * trainMatrix[i]
        outOffset += hidRate * out_delta
        hidOffset += inputRate * hide_delta

    print('Finish train...')
    return w1, w2, hidOffset, outOffset

def test():
    w1, w2, hidOffset, outOffset = TrainNetwork()
    print(w1, w2, hidOffset, outOffset)
    right = np.zeros(9)
    numbers = np.zeros(9)
    for i in testLabel:
        numbers[i] += 1
    print(numbers)
    for i in range(len(testLabel)):
        testMatrix[i] = np.array(testMatrix[i])
        hid_value = np.dot(testMatrix[i], w1) + hidOffset
        hid_act = sigmoid(hid_value)
        out_value = np.dot(hid_act, w2) + outOffset
        out_act = sigmoid(out_value)
        if np.argmax(out_act) != testLabel[i]:
            right[testLabel[i]] += 1
    for i in range(9):
        print("error rate in class %d is %f"%(i, float(right[i])/numbers[i]))
    print('error rate is %f'%(right.sum()/len(testLabel)))

test()


# error rate is 0.526427