# its multi-classification question
# can use OVR SVM, every time compares one against 1/n * rest
# I think it will be ..... ok?
# the certainty factor is the distance of one predict to the plane
# So its useful to let the Last prediction to be the class that will most far away from the plane
# use SMO


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

trainMatrix = csr_matrix(([1]*len(trainDatar), (trainDatar, trainDatac)), shape=(trainDatar[-1]+1, len(word))).toarray()
testMatrix = csr_matrix(([1]*len(testDataR), (testDataR, testDataC)), shape=(testDataR[-1]+1, len(word))).toarray()

# below is the SVM (label is +1 & -1, using SMO)

def selectJrand(i, m):
    j = i
    while j == i:
        j = int(random.uniform(0,m))
    return j

def clipAlpha(aj, H, L):
    if aj > H:
        aj = H
    if aj < L:
        aj = L
    return aj

def kernelTrans(X, A, kTup):
    m, n = np.shape(X)
    K = np.mat(np.zeros((m,1)))
    if kTup[0] == 'lin':
        K = K * A.T
    elif kTup[0] == 'rbf':
        for j in range(m):
            deltaRow = X[j,:] - A
            K[j] = deltaRow * deltaRow.T
        K = np.exp(K / (-1*kTup[1]**2))
    else:
        raise NameError('No this Kernel')
    return K

class optStruct:
    def __init__(self, dataMatIn, classLabels, C, toler, kTup):
        self.X = dataMatIn
        self.C = C
        self.labelMat = classLabels
        self.tol = toler
        self.m = np.shape(dataMatIn)[0]
        self.alphas = np.mat(np.zeros((self.m,1)))
        self.b = 0
        self.eCache = np.mat(np.zeros((self.m,2)))
        self.K = np.mat(np.zeros((self.m,self.m)))
        for i in range(self.m):
            self.K[:,i] = kernelTrans(self.X, self.X[i,:], kTup)

def calcEk(oS, k):
    fxk = float(np.multiply(oS.alphas,oS.labelMat).T*oS.K[:,k] + oS.b)
    Ek = fxk - float(oS.labelMat[k])
    return Ek

def selectJ(i, oS, Ei):
    maxK = -1
    maxDeltaE = 0
    Ej = 0
    oS.eCache[i] = [1, Ei]
    validEcacheList = np.nonzero(oS.eCache[:,0].A)[0]
    if(len(validEcacheList)) > 1:
        for k in validEcacheList:
            if k == i:
                continue
            Ek = calcEk(oS, k)
            deltaE = abs(Ei-Ek)
            if deltaE > maxDeltaE:
                maxK = k
                maxDeltaE = deltaE
                Ej = Ek
        return maxK, Ej
    else:
        j = selectJrand(i, oS.m)
        Ej = calcEk(oS, j)
        return j, Ej

def updateEk(oS, k):
    Ek = calcEk(oS, k)
    oS.eCache[k] = [1, Ek]

def innerL(i, oS):
    Ei = calcEk(oS, i)
    if (not(oS.labelMat[i]*Ei<-oS.tol and oS.alphas[i]<oS.C)) and \
            (not (oS.labelMat[i]*Ei>oS.tol and oS.alphas[i]>0)):
        return 0
    j, Ej = selectJ(i, oS, Ei)
    alphaIold = oS.alphas[i].copy()
    alphaJold = oS.alphas[j].copy()
    if oS.labelMat[i] != oS.labelMat[j]:
        L = max(0, oS.alphas[j]-oS.alphas[i])
        H = min(oS.C, oS.C+oS.alphas[j]-oS.alphas[i])
    else:
        L = max(0, oS.alphas[j]+oS.alphas[i]-oS.C)
        H = min(oS.C, oS.alphas[j]+oS.alphas[i])
    if L == H:
        return 0
    eta = 2.0 * oS.K[i,j] - oS.K[i,i] - oS.K[j,j]
    if eta >= 0:
        return 0
    oS.alphas[j] -= oS.labelMat[j] * (Ei - Ej) / eta
    oS.alphas[j] = clipAlpha(oS.alphas[j], H, L)
    updateEk(oS, j)
    if abs(oS.alphas[j]-alphaJold) < 0.00001:
        return 0
    oS.alphas[i] += oS.labelMat[j] * oS.labelMat[i] * (alphaJold-oS.alphas[j])
    updateEk(oS, i)
    b1 = oS.b - Ei - oS.labelMat[i] * (oS.alphas[i] - alphaIold) * oS.K[i, i] - oS.labelMat[j] \
            * (oS.alphas[j] - alphaJold) * oS.K[i, j]
    b2 = oS.b - Ej - oS.labelMat[i] * (oS.alphas[i] - alphaIold) * oS.K[i, j] - oS.labelMat[j] \
            * (oS.alphas[j] - alphaJold) * oS.K[j, j]
    if (0 < oS.alphas[i]) and (oS.C > oS.alphas[i]):
        oS.b = b1
    elif (0 < oS.alphas[j]) and (oS.C > oS.alphas[j]):
        oS.b = b2
    else:
        oS.b = (b1 + b2) / 2.0
    return 1

def smoP(dataMatIn, classLabels, C, toler, maxIter, kTup=('lin',0)):
    oS = optStruct(np.mat(dataMatIn),np.mat(classLabels).transpose(),C,toler,kTup)
    print('finish Init...')
    iter = 0
    entireSet = True
    alphaPairsChanged = 0
    while (iter<maxIter) and ((alphaPairsChanged>0) or entireSet):
        print('iter = %d' % iter)
        alphaPairsChanged = 0
        if entireSet:
            for i in range(oS.m):
                alphaPairsChanged += innerL(i, oS)
            iter += 1
        else:
            nonBoundIs = np.nonzero((oS.alphas.A>0) * (oS.alphas.A<C))[0]
            for i in nonBoundIs:
                alphaPairsChanged += innerL(i, oS)
            iter += 1
        if entireSet:
            entireSet = False
        elif alphaPairsChanged == 0:
            entireSet = True
    return oS.b, oS.alphas

def calcWs(alphas, dataArr, classLabels):
    X = np.mat(dataArr)
    labelMat = np.mat(classLabels).transpose()
    m, n = np.shape(X)
    w =np.zeros((n,1))
    for i in range(m):
        w += np.multiply(alphas[i]*labelMat[i], X[i,:].T)
    return w


LastPredict = np.zeros(len(testLabel))
oldpredict = np.zeros(len(testLabel))
# for huge feature, linear is better than rbf
def test(trainddd, case, kTup=('rbf', 2)):
    b, alphas = smoP(trainddd,trainLabelS[case],200,0.0001,10000,kTup)
    dataMat = np.mat(trainddd)
    labelMat = np.mat(trainLabelS[case]).transpose()
    svInd = np.nonzero(alphas.A>0)[0]
    sVs = dataMat[svInd]
    labelSV = labelMat[svInd]
    m, n = np.shape(dataMat)
    errorCount = 0
    for i in range(m):
        kernelEval = kernelTrans(sVs, trainddd[i,:], kTup)
        predict = kernelEval.T * np.multiply(labelSV, alphas[svInd]) + b
        if np.sign(predict) != np.sign(trainLabelS[case][i]): errorCount += 1
    print("the training error rate : %f" % (float(errorCount) / m))

    rightCount = 0.0
    dataMat = np.mat(testMatrix)
    m, n = np.shape(dataMat)
    for i in range(m):
        kernelEval = kernelTrans(sVs, dataMat[i,:], kTup)
        predict = kernelEval.T * np.multiply(labelSV,alphas[svInd]) + b
        predicta = np.ndarray.flatten(np.array(predict))
        if np.sign(predict) > 0:
            if predicta[0] > oldpredict[i]:
                LastPredict[i] = case
                oldpredict[i] = predicta[0]
        if oldpredict[i] != 0 and testLabel[i] == LastPredict[i]:
            rightCount += 1
    print("the right rate : %f" % (float(rightCount) / m))
    print("(every time the right rate plus 10+% if perfectly...)")



trainMatrixS = []
trainLabelS = []
indext = []
for ind in range(len(target)):
    tempd = []
    templ = []
    x = 0
    for i in range(len(trainMatrix)):
        if trainLabel[i] == ind:
            tempd.append(trainMatrix[i])
            templ.append(1)
        else:
            if(x > float(len(trainMatrix))/len(target)):
                continue
            w = random.randint(0,6)
            if w != 5:
                continue
            x += 1
            tempd.append(trainMatrix[i])
            templ.append(-1)
    trainMatrixS.append(tempd)
    trainLabelS.append(templ)

trainMatrixS = np.array(trainMatrixS)
trainLabelS = np.array(trainLabelS)
testMatrix = np.array(testMatrix)
testLabel = np.array(testLabel)
for i in range(len(trainMatrixS)):
    w = np.array(trainMatrixS[i]) # too large to make all in a array
    test(w, i)

allError = 0.0
for i in range(len(testLabel)):
    if testLabel[i] != LastPredict[i]:
        allError += 1
print("the  final OVR error rate : %f" % (float(allError) / len(testLabel)))
print(LastPredict)
