class Newspaper:
    def __init__(self, name, div_id):
        self.name = name
        self.div_id = div_id
        self.urls = []
    def getName(self):
        return self.name
    def setUrlList(self, list):
        self.urls = list
    def getUrlList(self):
        return self.urls
    def getDivId(self):
        return self.div_id