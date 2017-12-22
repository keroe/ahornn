import json
import requests
import bs4

import nltk
from nameparser.parser import HumanName

#request news from news-api
relevantNewspaper = ["al-jazeera-english", "bbc-news", "cnn", "fox-news", "nbc-news", "the-guardian-uk", "the-guardian-uk"]
#numberOfPosts = 20;

#urlGoogleNews = "https://newsapi.org/v2/top-headlines?sources=" + relevantNewspaper[1] + "&apiKey=" + key;
#urlRedditNews = "https://www.reddit.com/r/worldnews/top/.json?count=" + numberOfPosts;

#news = requests.get(urlGoogleNews)
#news = news.json() #convert response into a json


#scrap html code

# term for news text in cnn         zn-body__read-all



urlArticle = "http://us.cnn.com/2017/12/01/politics/michael-flynn-charged/index.html" #news["articles"][1]["url"]

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
    APIKey = APIKey.read()
    return APIKey


def getArticleText(urlArticle, newsPage = []):
  res = requests.get(urlArticle)
  res.raise_for_status()
  htmlArticle = bs4.BeautifulSoup(res.text)

  ## CNN
  elems = htmlArticle.find_all('div', class_="zn-body__paragraph")

  i = 0
  articleText = ""
  for divs in elems:
    articleText += elems[i].getText() + " "
    i += 1
  return articleText


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


