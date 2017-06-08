# this is from http://blog.csdn.net/panghaomingme/article/details/54428030
# it's much easier and quicker to use sklearn




from sklearn.datasets import fetch_20newsgroups
news = fetch_20newsgroups(subset='all')

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(news.data, news.target, test_size=0.25, random_state=33)

from sklearn.feature_extraction.text import CountVectorizer
count_vec = CountVectorizer()

X_count_train = count_vec.fit_transform(X_train)
X_count_test = count_vec.transform(X_test)

from sklearn.naive_bayes import MultinomialNB
mnb_count = MultinomialNB()
mnb_count.fit(X_count_train, y_train)

print ('The accuracy of classifying 20newsgroups using Naive Bayes (CountVectorizer without filtering stopwords):', mnb_count.score(X_count_test, y_test))
y_count_predict = mnb_count.predict(X_count_test)
from sklearn.metrics import classification_report
print (classification_report(y_test, y_count_predict, target_names = news.target_names))
