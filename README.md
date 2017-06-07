F

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
    Using sorted dict to count all the words and make every news a vector, the element is the word 's index of the list above
    
3.Feature Selection
----------------------------------------------------------------------
    Using Information Gain & TF-IDF & chi-square.
    IG is not good for classification(ONLY can judge global feature)
    chi-square I may use it just before classification.

4.Normalization & Weight & DataDivision
-------------------------------------------------------------------------
    I think of this part, I think it's not necessary for I do the TF-IDF
    And I can divide data just before classification
