import json
import requests

#request news from news-api at the moment from bild
news = requests.get("https://newsapi.org/v1/articles?source=bild&sortBy=top&apiKey=x")
news = news.json() #convert response into a json


#debug json list elements
i = 0
for objects in news:
    print(news["articles"][i]["description"])
    i = i+1


