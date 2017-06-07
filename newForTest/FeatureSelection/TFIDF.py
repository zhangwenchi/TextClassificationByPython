# TF - IDF
# TF is the term frequency, the appearance in a news
# IDF is inverse document frequency, it means it is not that common in news
# so, if a word is not common but appears a lot in a news, its keyword !!!!!
# TF = (the appearing times of a word in a new) / (the amount of words in that news OR the max frequency in this news)
# IDF = log(the amount of news / (the amount of news that contains this word + 1))
# do not need to + 1 cause I use the all the words from news to be the Corpus
# tf-idf = TF * IDF
from scipy.sparse import csr_matrix
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import os
import numpy as np

Vdir = '..\CleanData\VectorOfNews'
fileList = os.listdir(Vdir)
Corpus = []
for i in range(len(fileList)):
    f = open('..\CleanData\FenciByjieba' + '\%s' % fileList[i], 'r', encoding='utf-8')
    for line in f.readlines():
        Corpus.append(line)

# print(Corpus) ## the news Content
vectorizer = CountVectorizer()
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(vectorizer.fit_transform(Corpus))

# print(type(tfidf))
word = vectorizer.get_feature_names()  # 所有文本的关键字
#  how to store a sparse matrix!
np.savez('TFIDF.npz', data=tfidf.data, indices=tfidf.indices,
         indptr=tfidf.indptr, shape=tfidf.shape)
loader = np.load('TFIDF.npz')
print(csr_matrix((loader['data'], loader['indices'], loader['indptr']), shape=loader['shape']))
