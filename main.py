
from president_estimator import PresidentEstimator
from scrabNews import getArticleText, getArticlesNewsAPI, readAPIKey
from newspaper import Newspaper

pres_es = PresidentEstimator()
APIKEY = readAPIKey("APIKey.txt")
error_counter = 0

#cnn = Newspaper("cnn", "zn-body__paragraph")
bbc = Newspaper("bbc-news", "story-body__inner")
fox = Newspaper("fox-news", "article-body")
nbc = Newspaper("nbc-news", "article-body")
guardian = Newspaper("the-guardian-uk", "content__article-body from-content-api js-article__body")
al_jaz = Newspaper("al-jazeera-english", "main-article-body")

relevantNewspaper = [bbc, fox, nbc, guardian, al_jaz]
for newspaper in relevantNewspaper:
    newspaper.setUrlList(getArticlesNewsAPI(newspaper.getName(), APIKEY))
    for urls in newspaper.getUrlList():
        text, flag = getArticleText(urls, newspaper.getDivId()) 
        if flag:
            error_counter += 1
        pres_es.getHumanNames(text)
        pres_es.mergeLists()


print("Aufgetretene Errors: ", error_counter)
for person in pres_es.getPersonsList(): 
    print(person.getFullName(), " kommt so oft vor: ", person.getOccurence())