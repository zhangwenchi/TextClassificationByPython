
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
    (1)Using jieba to segmentate the news and drop the stopwords by a list,then get the vector of words
    (2)Using sorted dict to count all the words and make every news a vector, the element is the word 's index of the list above
