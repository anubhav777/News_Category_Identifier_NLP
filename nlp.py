from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer

df=pd.read_json('News_Category_Dataset_v2.json',lines=True)
data=df.drop(['authors','link','short_description','date'],axis=1)
data.dropna(inplace=True)

news_href=['https://edition.cnn.com/','https://www.bbc.com/','https://www.nytimes.com/','https://www.buzzfeednews.com/','https://www.aljazeera.com/news/','https://news.yahoo.com/','https://timesofindia.indiatimes.com/','https://www.theguardian.com/international','https://www.cnbc.com/world/?region=world','https://www.cbsnews.com/','https://www.abc.net.au/news/','https://www.mirror.co.uk/','https://www.express.co.uk/news','https://www.bbc.com/sport']

# web scrape garera lsit ma halne code
class webscrape:
    def __init__(self,link):
        self.link=link
    def word_filter(self):
        all_news=[]
        for i in range(len(self.link)):
            source=requests.get(news_href[i]).text
            soup=BeautifulSoup(source,'lxml')
            all_link = soup.find_all('a')
            for link in all_link:
                new_text=re.sub("\s+" , " ",link.text)
                if len(new_text) >= 50 and len(new_text) <= 150:
                    if re.search('[a-zA-Z]',new_text) is not None:

                        all_news.append(new_text)
        return all_news 
    
    @staticmethod
    def text_filter(arr):
        stemmed_news=[]    
        for i in range(len(arr)):
            mod_text=re.sub('[^a-zA-Z]',' ',arr[i])
            mod_text=mod_text.lower()
            mod_text=mod_text.split(' ')
            mod_text=filter(None, mod_text)
            news=[ps.lemmatize(sentence) for sentence in mod_text if sentence not in (stopwords.words('english'))]
            news=','.join(news)
            news=news.replace(","," ")
            stemmed_news.append(news)
        return stemmed_news
                
webscrape1=webscrape(news_href)
all_news = webscrape1.word_filter()
all_news=list(set(all_news))
gh=pd.DataFrame(all_news)
