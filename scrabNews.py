import json
import requests
import bs4

import nltk
from nameparser.parser import HumanName

#request news from news-api at the moment from bild
#relevantNewspaper = ["Bild", "FAZ"]
#numberOfPosts = 20;

#urlGoogleNews = "https://newsapi.org/v2/top-headlines?sources=" + relevantNewspaper[1] + "&apiKey=" + key;
#urlRedditNews = "https://www.reddit.com/r/worldnews/top/.json?count=" + numberOfPosts;

#news = requests.get(urlGoogleNews)
#news = news.json() #convert response into a json


#scrap html code

# term for news text in cnn         zn-body__read-all



urlArticle = "http://us.cnn.com/2017/12/01/politics/michael-flynn-charged/index.html" #news["articles"][1]["url"]


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
    print("==============TOKENS==============\n")
    print(tokens)
    print("\n")
    print("==============POS============== \n")
    print(pos)
    print("\n")
    print("==============SENTT==============\n")
    print(sentt)
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1: #avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []

    return (person_list)


#debug json list elements
#i = 0
#for objects in news:
#    print(news["articles"][i]["title"])
#    i = i+1

names = getHumanNames(getArticleText("http://us.cnn.com/2017/12/01/politics/michael-flynn-charged/index.html"))
print(names)
