import json
import requests

#request news from news-api at the moment from bild
news = requests.get("https://newsapi.org/v2/top-headlines?sources=bild&apiKey=x")
news = news.json() #convert response into a json


#debug json list elements
i = 0
for objects in news:
    print(news["articles"][i]["title"])
    i = i+1


