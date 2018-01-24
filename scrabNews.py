
import json
import requests
import bs4
from newspaper import Newspaper


#numberOfPosts = 20;




#scrap html code

# term for news text in cnn         zn-body__read-all



# CNN test article
urlArticle = "http://us.cnn.com/2017/12/01/politics/michael-flynn-charged/index.html"

# BBC-news test article
#urlArticle = "http://www.bbc.com/news/world-us-canada-42525880"

# Fox-news test article
#urlArticle = "http://www.foxnews.com/opinion/2017/12/31/liz-peek-what-trump-didnt-do-in-2017-presidents-hysteria-prone-critics-must-be-sorely-disappointed.html"

# NBC news test article
#urlArticle = "http://www.nbcnews.com/politics/politics-news/papadopoulos-brag-australian-diplomat-was-key-factor-fbi-s-russia-n833691"

#the guardian test article
#urlArticle = "https://www.theguardian.com/uk-news/2017/dec/31/northern-bell-rochdale-town-hall-put-forward-as-big-ben-stand-in"

# Al-Jazeera test article 
#urlArticle = "http://www.aljazeera.com/news/2017/12/iran-blocks-instagram-telegram-protests-171231133323939.html"

# other news sources 
#urlArticle = "http://www.telegraph.co.uk/science/2017/12/29/british-polar-explorer-ben-saunders-echoes-shackleton-has-abandons/"


#You can copy the API-Key to a file and then read it with the readAPIKey function
#example usage: readAPIKey("APIKey.txt")
def readAPIKey(APIKeyFile):
    APIKey = open(APIKeyFile, "r") 
    APIKey = APIKey.read().splitlines() #splitlines is needed otherwise read would give \n at the end of a line and then the api key is invalid
    return APIKey[0] #APIKey is a list after the usage of splitlines and we just want to return the first entry


def getArticleText(urlArticle, div_id, newsPage = []):
  res = requests.get(urlArticle)
  res.raise_for_status()
  htmlArticle = bs4.BeautifulSoup(res.text, "lxml")

  try:
    elems = htmlArticle.find('div', class_=div_id).findAll('p')
    articleText = ""
    error_flag = False
    for i, divs in enumerate(elems, 0):
      articleText += elems[i].getText() + " "
      return articleText, error_flag
  except AttributeError:
      error_flag = True
      return '', error_flag
    



def getArticlesNewsAPI(relevantNewspaperName, APIKey):
    #request news from news-api
    articlesURL = []
    urlNews = ("https://newsapi.org/v2/top-headlines?sources="+relevantNewspaperName+"&apiKey="+APIKey)
    news = requests.get(urlNews)
    news = news.json() #convert response into a json
    for l, articles in enumerate(news["articles"], 0):
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

#debug json list elements
#i = 0
#for objects in news:
#    print(news["articles"][i]["title"])
#    i = i+1

#names = getHumanNames(getArticleText("http://us.cnn.com/2017/12/01/politics/michael-flynn-charged/index.html"))
#for entries in names:
#    print(entries.getFullName())
#    print(entries.getOccurence())

