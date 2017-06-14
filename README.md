
TextClassificationByPython
==============================================================


1.Crawling
------------------------------------------------------------------
    Using Python to crawl different kinds of news from Sohu.
    (1)Crawl the Proxy
    (2)Check the Proxy available or not
    (3)Crawl the news links
    (4)Crawl the news content
    Using: multi-thread, BeautifulSoup, re, requests, urllib, http.cookiejar
    
2.CleaningData
------------------------------------------------------------------
    Turn all the news to numbers.
    Using jieba to segmentate the news and drop the stopwords by a list,then get the vector of words
    Using sorted dict to count all the words and make every news a vector, 
    the element is the word 's index of the list above
    
3.Feature Selection
----------------------------------------------------------------------
    Using Information Gain & TF-IDF & chi-square.
    IG is not good for classification(ONLY can judge global feature)
    chi-square I may use it just before classification.

4.Normalization & Weight & DataDivision
-------------------------------------------------------------------------
    I think of this part, I think it's not necessary for I do the TF-IDF
    And I can divide data just before classification
    
5.Classification
---------------------------------------------------------------------------
    1.Naive Bayes    -> error rate(DIY): 0.1303894297635605
    2.Random Forest  -> error rate(sklearn): 0.13446088794926003
    3.SVM            -> error rate(sklearn linear, OVO): 0.142495  -> error rate(DIY rbf, OVR): 0.742072
    4.KNN           -> error rate(sklearn): 0.725159
    5.Neural Network
        (1)simple one layer BP  -> error rate(DIY): 0.526427
        (2)MLP                  -> error rate(sklearn, hide_layer(10,30)): 0.128541 (TOP Now)
        (2)RNN                  -> error rate(DIY): 0.365031
    6.Adaboost                  -> error rate(Not do it well) : 0.357717
    
6.Write for me
--------------------------------------------------------------------------
    Finally, I finished my text-classification, it's not perfect, even less than 'cool',
    for I almost 'skip' the RNN and Adaboost part.
    But here is one thing that I am proud of -- I did not use thano or tensorflow or something else.
    I will use then in my next project :)
    Happy ! finished.
