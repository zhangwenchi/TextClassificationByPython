# simple RNN -> have a context of the hidden layer to store the forward data
# Bidirectional RNN -> two RNN together decide (forward and next data together with the data)
# Deep RNN -> more than two Bidirectional RNN
# Echo State Network  -> random reservoir
# LSTM -> solve for long list dependency -> main and most important , I choose this

# It cannot change the position of every word for the RNN is memory!
# it's so huge for I need a matrix for input, so only small dataSet is used!
# if a news is not long enough, using the word used before

# input data is a vector in every joint
# so in hidden_layer we should create a 3D matrix , 2D matrix and every element is a (20*1) vector, and the number is randomly

import os
import random

from gensim.models import Word2Vec, KeyedVectors
from gensim.models.word2vec import LineSentence
import numpy as np
import copy

Vdir = '..\CleanData\FenciByjieba'
fileList = os.listdir(Vdir)
target = []
trainData = []
for i in range(len(fileList)):
    target.append(fileList[i].split('.')[0])
    f = open(Vdir + '\\' + fileList[i],'r',encoding='utf-8')
    trainData.append(f.readlines())
f.close()
# trainData.size: 9 * 1000+ * 3000+
trainMatrix = []
trainLabel = []
testMatrix = []
testLabel = []
for i in range(len(trainData)):
    for j in range(len(trainData[i])):
        if j % 29 == 0:
            trainMatrix.append(trainData[i][j])
            trainLabel.append(i)
        elif j % 71 ==0:
            testMatrix.append(trainData[i][j])
            testLabel.append(i)

# get the vector of words by using all the words -> but train only use some of them
# f = open('Word2Vec\sentence.txt','w',encoding='utf-8')
# for i in range(len(trainData)):
#     f.write("".join(trainData[i]))
# f.close()
# model = Word2Vec(LineSentence('Word2Vec\sentence.txt'), size=20, min_count=3, workers=4)
# model.wv.save_word2vec_format('Word2Vec\Vector', binary=False)
# print(model.most_similar('中国'))
model = KeyedVectors.load_word2vec_format('Word2Vec\Vector')
trainV = []
for i in range(len(trainMatrix)):
    temp = []
    w = trainMatrix[i].split(' ')
    for j in range(len(w)):
        try:
            temp.append(model[w[j]])
        except:
            continue
    trainV.append(temp)
testV = []
for i in range(len(testMatrix)):
    temp = []
    w = testMatrix[i].split(' ')
    for j in range(len(w)):
        try:
            temp.append(model[w[j]])
        except:
            continue
    testV.append(temp)

# trainV is 415 * hundreds * 20
# testV is 163 * hundreds * 20
random.shuffle(trainV)
random.shuffle(testV)

# if less than 500 words, use the front, if more, just drop
input_dim = 500
hidden_dim = 10
output_dim = 9
alpha = 0.1


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_ouput_to_derivative(output):
    return output * (1 - output)

synapse_0 = 2 * np.random.random((input_dim, hidden_dim)) - 1
# print(synapse_0)
synapse_1 = 2 * np.random.random((hidden_dim, output_dim)) - 1
synapse_h = 2 * np.random.random((hidden_dim, hidden_dim)) - 1
synapse_0_update = np.zeros_like(synapse_0)
synapse_1_update = np.zeros_like(synapse_1)
synapse_h_update = np.zeros_like(synapse_h)

# train
for i in range(len(trainV)):
    pre = -1
    overallError = 0
    layer_2_deltas = list()
    layer_1_values = list()
    layer_1_values.append(np.zeros(hidden_dim))

    tt = 0
    a = np.zeros((500,20))
    # a is one train data
    # c is the right answer
    c = np.zeros(9)
    c[trainLabel[i]] = 1

    for position in range(input_dim):
        a[position] = np.array(trainV[i][tt])
        tt += 1
        if tt == len(trainV[i]):
            tt = 0
    a = np.array(a)

    for position in range(20): # 20 is length of one word vector
        X = np.array([a[t][position] for t in range(500)])
        layer_1 = sigmoid(np.dot(X,synapse_0) + np.dot(layer_1_values[-1],synapse_h))
        layer_2 = sigmoid(np.dot(layer_1, synapse_1))

        layer_2_error = c - layer_2
        layer_2_deltas.append(layer_2_error * sigmoid_ouput_to_derivative(layer_2))
        overallError += np.abs(layer_2_error[0])

        layer_1_values.append(copy.deepcopy(layer_1))
    future_layer_1_delta = np.zeros(hidden_dim)

    for position in range(20):
        X = np.array([a[t][position] for t in range(500)])
        layer_1 = layer_1_values[position]
        pre_layer_1 = layer_1_values[position-1]

        layer_2_delta = layer_2_deltas[position]
        layer_1_delta = (future_layer_1_delta.dot(synapse_h.T) +
                layer_2_delta.dot(synapse_1.T)) * sigmoid_ouput_to_derivative(layer_1)

        xt = np.matrix(layer_2_delta)
        xt2 = np.matrix(layer_1_delta)
        xt3 = np.matrix(layer_1_delta)
        X = np.matrix(X)
        synapse_1_update += np.atleast_2d(layer_1).T.dot(xt)
        synapse_h_update += np.atleast_2d(pre_layer_1).T.dot(xt2)
        synapse_0_update += X.T.dot(xt3)

        future_layer_1_delta = layer_1_delta

errorCount = 0.0
for i in range(len(testV)):
    pre = -1
    at = np.zeros((500,20))
    tt = 0
    for position in range(input_dim):
        at[position] = np.array(testV[i][tt])
        tt += 1
        if tt == len(testV[i]):
            tt = 0
    at = np.array(at)
    finalAns = np.matrix(np.zeros(9))
    for position in range(20):
        X = np.matrix(np.array([at[t][position] for t in range(500)]))
        ans = X * synapse_0 * synapse_h * synapse_1
        finalAns += ans[0]
    if int(np.where(finalAns == np.max(finalAns))[1]) == testLabel[i]:
        print('test %d is right!' % i)
    else:
        errorCount += 1

print('error rate is :%f'%(errorCount/len(testV)))
