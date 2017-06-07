# For the information gain is not that useful for the classification
# I use TFIDF then I use chi-square, to get the top .... maybe 10000

import numpy as np
from scipy.sparse import csr_matrix
# from gensim import corpora, models, similarities
from sklearn.feature_selection import SelectKBest, chi2
import pandas as pd

# loader = np.load('TFIDF.npz')
# tfidf = csr_matrix((loader['data'], loader['indices'], loader['indptr']), shape=loader['shape'])
#
# print(tfidf.indices)
# ch2 = SelectKBest(chi2, k=10000)

# I can just use the chi-square before the classification
