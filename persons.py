class Person:

    def __init__(self, surname, prename = ''):
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
