
import json
import requests
import bs4

import nltk
from nameparser.parser import HumanName


#numberOfPosts = 20;




#scrap html code

# term for news text in cnn         zn-body__read-all



# CNN test article
# urlArticle = "http://us.cnn.com/2017/12/01/politics/michael-flynn-charged/index.html"

# BBC-news test article
#urlArticle = "http://www.bbc.com/news/world-us-canada-42525880"

# Fox-news test article
#urlArticle = "http://www.foxnews.com/opinion/2017/12/31/liz-peek-what-trump-didnt-do-in-2017-presidents-hysteria-prone-critics-must-be-sorely-disappointed.html"

# NBC news test article
#urlArticle = "http://www.nbcnews.com/politics/politics-news/papadopoulos-brag-australian-diplomat-was-key-factor-fbi-s-russia-n833691"

#the guardian test article
#urlArticle = "https://www.theguardian.com/uk-news/2017/dec/31/northern-bell-rochdale-town-hall-put-forward-as-big-ben-stand-in"

# Al-Jazeera test article 
urlArticle = "http://www.aljazeera.com/news/2017/12/iran-blocks-instagram-telegram-protests-171231133323939.html"

class Person:

    def __init__(self, prename, surname):
        self.occurence = 1
        self.prename = prename
        self.surname = surname

    def increaseOccurence(self):
        self.occurence += 1

    def getSurname(self):
        return self.surname

    def getFullName(self):
        return self.prename + ' ' + self.surname

    def getOccurence(self):
        return self.occurence

#You can copy the API-Key to a file and then read it with the readAPIKey function
#example usage: readAPIKey("APIKey.txt")
def readAPIKey(APIKeyFile):
    APIKey = open(APIKeyFile, "r") 
    APIKey = APIKey.read().splitlines() #splitlines is needed otherwise read would give \n at the end of a line and then the api key is invalid
    return APIKey[0] #APIKey is a list after the usage of splitlines and we just want to return the first entry


def getArticleText(urlArticle, newsPage = []):
  res = requests.get(urlArticle)
  res.raise_for_status()
  htmlArticle = bs4.BeautifulSoup(res.text, "lxml")

  ## CNN
  #elems = htmlArticle.find_all('div', class_="zn-body__paragraph")

  ## BBC news
  #elems = htmlArticle.find('div', class_="story-body__inner").findAll('p')

  ## Fox news
  #elems = htmlArticle.find('div', class_="article-body").findAll('p')

  ## NBC news
  #elems = htmlArticle.find('div', class_= "article-body").findAll('p')

  ## The guardian 
  #elems = htmlArticle.find('div', class_= "content__article-body from-content-api js-article__body").findAll('p')
  
  ## Al-Jazeera
  elems = htmlArticle.find('div', class_="main-article-body").findAll('p')

  i = 0
  articleText = ""
  for divs in elems:
    articleText += elems[i].getText() + " "
    i += 1
  return articleText

def getArticlesNewsAPI(APIKey):
    #request news from news-api
    relevantNewspaper = ["bbc-news", "cnn", "fox-news", "nbc-news", "the-guardian-uk","al-jazeera-english"]
    articlesURL = []
    for i, newspaper in enumerate(relevantNewspaper, 0):
        urlGoogleNews = ("https://newsapi.org/v2/top-headlines?sources="+relevantNewspaper[i]+"&apiKey="+APIKey)
        news = requests.get(urlGoogleNews)
        news = news.json() #convert response into a json
        for l, articles in enumerate(news, 0):
            articlesURL.append(news["articles"][l]["url"])
    return articlesURL

def getArticlesReddit(numberOfPosts = 20):
    articlesURL = []
    urlRedditNews = "https://www.reddit.com/r/worldnews/top/.json?count=" + str(numberOfPosts)
    news = requests.get(urlRedditNews)
    news = news.json()
    for i, news in enumerate(news["data"]["children"], 0):
        articlesURL.append(news["data"]["children"][i]['data']['url'])
    return articlesURL




#the labels gpe and gsp indicate countriers or capitals
def getHumanNames(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    person_list = []
    person = []
    name = ""
    flag = False
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
            for part in person:
                name += part + ' '
            for entries in person_list: #checking all existing objects in the list
              if name[:-1] == entries.getSurname(): #if the surname is in the list increase occurence
                flag = True
                entries.increaseOccurence()
                break
            if not flag:
                person_list.append(Person(name[:0],name[:-1])) #append new object with prename and surname to the list
            name = ''
        flag = False
        person = []

    return (person_list)


#debug json list elements
#i = 0
#for objects in news:
#    print(news["articles"][i]["title"])
#    i = i+1

#names = getHumanNames(getArticleText("http://us.cnn.com/2017/12/01/politics/michael-flynn-charged/index.html"))
#for entries in names:
#    print(entries.getFullName())
#    print(entries.getOccurence())

text = getArticleText(urlArticle)
print(text)