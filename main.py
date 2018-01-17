
from president_estimator import PresidentEstimator
from scrabNews import getArticleText

pres_es = PresidentEstimator()

urlArticle = "http://us.cnn.com/2018/01/15/politics/congress-week-ahead/index.html"



text = getArticleText(urlArticle) 

pres_es.getHumanNames(text)
pres_es.sortListDecreasing()
pres_es.cropList()

#for person in pres_es.getPersonsList():
#    print(person.ge)

urlArticle = "http://us.cnn.com/2017/12/01/politics/michael-flynn-charged/index.html"
text = getArticleText(urlArticle) 
pres_es.getHumanNames(text)
pres_es.sortListDecreasing()
pres_es.cropList()

for person in pres_es.getPersonsList(): 
    print(person.getFullName(), " kommt so oft vor: ", person.getOccurence())