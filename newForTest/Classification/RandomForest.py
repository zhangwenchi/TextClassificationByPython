# this code is sooooooooooooooo slooooooooooooooow
# begin at 2017/06/10 10:44 ,and I make only 5 trees (have to - )
# 12:27 not finish even one tree
# i give up

from scipy.sparse import csr_matrix
import random
import numpy as np
import os

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

trainDD = [1]*len(trainDatar)
for i in range(trainDatar[-1]+1):
    trainDatar.append(i)
    trainDatac.append(len(word))
    trainDD.append(trainLabel[i])

testDD = [1]*len(testDataR)
for i in range(testDataR[-1]+1):
    testDataR.append(i)
    testDataC.append(len(word))
    testDD.append(testLabel[i])

# after feature selection I do not need sparse ~~~~~~~~~
trainMatrix = csr_matrix((trainDD, (trainDatar, trainDatac)), shape=(trainDatar[-1]+1, len(word)+1)).toarray()
# print(trainMatrix)
testMatrix = csr_matrix((testDD, (testDataR, testDataC)), shape=(testDataR[-1]+1, len(word)+1)).toarray()
# print(testMatrix)

class randomforest():
    def __init__(self,train_data,n_estimators=10):
        self.data = train_data
        self.n_estimators = n_estimators
        self.decision_trees = []
        self.labels = np.unique(self.data[:,-1])
    def cal_entropy(self,y):
        elements={}
        total=len(y)
        for ele in y:
            elements[ele]=elements.get(ele,0)+1
        entropy=0
        for ele in elements:
            p=elements.get(ele)*1.0/total
            entropy-=p*np.log2(p)
        return entropy
    def split_data(self,data,i,value):
        "split data x in the dimension i with value "
        split_data=[]
        for row in data:
            if row[i]==value:
                split_data.append(row[:i].tolist()+row[i+1:].tolist())
        return np.array(split_data)
    def select_feature(self,data):
        x=data[:,:-1]
        y=data[:,-1]
        base_entropy=self.cal_entropy(y)
        max=-1
        select_feature=-1
        row_num,col_num=x.shape
        for col in range(col_num):
            elements=np.unique(x[:,col])
            entropy=0
            for ele in elements:
                split_data=self.split_data(data,col,ele)
                entropy+=split_data.shape[0]*1.0/row_num*self.cal_entropy(split_data[:,-1])
            info_gain=base_entropy-entropy
            #print "featurn %d increase is %f"%(col,info_gain)
            if max<info_gain:
                select_feature=col
                max=info_gain
        return select_feature
    def build_decision_tree(self,data,features_list):
        "train the data and build an decision tree"
        x=data[:,:-1]
        y=data[:,-1]
        #conditions for the termination of the recursive function
        #condition one:when all lables is the
        if len(np.unique(y))==1:
            return y[0]
        #condition two :when there are no feature to split
        if data.shape[1]==1:
            dic={}
            for i in y:
                dic[i]=dic.get(i,0)+1
            l=sorted(dic.iteritems(),key=lambda xx:xx[1],reverse=True)
            return l[0][0]
        select_feature=self.select_feature(data)
        values=np.unique(data[:,select_feature])
        raw_feature=features_list[select_feature]
        features_list.remove(raw_feature)
        myTree={raw_feature:{}}
        for value in values:
            myTree[raw_feature][value]=self.build_decision_tree(self.split_data(data,select_feature,value),features_list[:])
        return myTree
    def fit(self):
        row,col=self.data.shape
        for i in range(self.n_estimators):
            #sample data
            samples=np.random.randint(0,row,int((row+1)/2))
            samples=np.unique(samples)
            samples_data=self.data[samples.tolist()]
            #sample feature
            features=np.random.randint(0,col-1,int(col/2))
            features=np.unique(features)
            features_list=features.tolist()
            features_list.append(-1)
            sample_feature_data=samples_data[:,features_list]
            #print sample_feature_data
            decision_tree=self.build_decision_tree(sample_feature_data,features_list)
            print(decision_tree)
            print("Finish %d trees" % i)
            self.decision_trees.append(decision_tree)
    def classify(self,decision_tree,test_x):
        first_feature=decision_tree.keys()[0]
        secondDict=decision_tree[first_feature]
        key=test_x[first_feature]
        value=secondDict.get(key,"false")
        #if we can not find the key ,the we will return a label randomly
        if value=="false":
            return "cannot calssify"
        if isinstance(value,dict):
            classLabel=self.classify(value,test_x)
        else:classLabel=value
        return classLabel
    def predict(self,test_data):
        predict_labels=[]
        for test_x in test_data:
            dic={}
            for decision_tree in self.decision_trees:
                predict_label=self.classify(decision_tree,test_x)
                if predict_label=="cannot calssify":
                    continue
                #print predict_label
                dic[predict_label]=dic.get(predict_label,0)+1

            l=sorted(dic.iteritems(),key=lambda x:x[1],reverse=True)
            if len(l)==0:
                r=np.random.randint(0,self.labels.shape[0])
                label=self.labels[r]
                predict_labels.append(label)
            else:
                predict_labels.append(l[0][0])
        return np.array(predict_labels)
    def accuracy(self,test_data):
        predict_labels=RF.predict(test_data[:,:-1])
        length=test_data.shape[0]
        num=0
        for i in range(length):
            if predict_labels[i]==test_data[i,-1]:
                num+=1
        print("test data accuracy is %f"%(num*1.0/length))

RF = randomforest(trainMatrix,5)
RF.fit()
RF.accuracy(testMatrix)
