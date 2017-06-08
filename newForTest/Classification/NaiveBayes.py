# P(B\A) = P(A|B)P(B)/P(A) -- for Bayes
# P((F1*...*Fn)|Ci) * P(Ci)     ----- Naive Bayes for Text Classification( denominator is the same)
# So, if there is a news, I make it to words first, then calculate the frequency of every word in each type,
# So every word sum of frequency is 1
# multiply every possibility to one

# oh, I cannot use CSR matrix in python well...........

import numpy as np
from scipy.sparse import csr_matrix
import os
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import collections


Vdir = '..\CleanData\VectorOfNews'
fileList = os.listdir(Vdir)
Corpus = []
for i in range(len(fileList)):
    f = open('..\CleanData\FenciByjieba' + '\%s' % fileList[i], 'r', encoding='utf-8')
    x = ""
    for line in f.readlines():
        x += " " + line
    Corpus.append(x)

vectorizer = CountVectorizer(vocabulary=None, max_df=50, min_df=5)  # if a word appears more than 50 times or less than 5 times
#
# The most important things is that I can change sparse to array by this Selection!
#
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(vectorizer.fit_transform(Corpus))
word = vectorizer.get_feature_names()  # keywords of all the text
freMatrix = vectorizer.fit_transform(Corpus).toarray()
tfidfMatrix = transformer.fit_transform(vectorizer.fit_transform(Corpus)).toarray()

# is it essential to calculate the TF-IDF for naive Bayes?
target = []
for i in range(len(fileList)):
    target.append(fileList[i].split('.')[0])

# get the train data and test data
# I can only use the freMatrix for the NB
trainData = []  # amount is 1000
trainLabel = []
testData = []
testLabel = []

for i in range(len(fileList)):
    f = open('..\CleanData\FenciByjieba' + '\%s' % fileList[i], 'r', encoding='utf-8')
    trainAmount = 1000
    for line in f.readlines():
        if trainAmount < 0:
            testData.append(line)
            testLabel.append(target[i])
        else:
            trainAmount -= 1
            trainData.append(line)
            trainLabel.append(target[i])

# I get 9000+ train data & 2800+ test data
# I need multinomial model !
# every type I have 5000 keywords !
# I did not use the frequency of the test data ....
amountOfTest = len(testLabel)
error = 0

labels = []
for i in range(amountOfTest):
    pBay = [0] * len(fileList)
    m = collections.Counter(testData[i].split(' ')) # frequency of word
    p = [1.0] * len(fileList)
    for ij in range(len(fileList)):
        for j in range(len(word)):
            if m[word[j]] == 0:
                continue
            tsum = 0.0
            for k in range(len(fileList)):
                tsum += freMatrix[k][j]
            p[ij] *= (freMatrix[ij][j]+1) / tsum
    labels.append(fileList[p.index(max(p))].split('.')[0])
    print("now is " + str(i) + " / " + str(amountOfTest))

print(labels)

for i in range(amountOfTest):
    if labels[i] != testLabel[i]:
        error += 1

print(error / amountOfTest)
print('error rate is :' + str(error / amountOfTest))

#
# error rate is ooooooooooooooooooonly 0.1303894297635605 !!!!
#