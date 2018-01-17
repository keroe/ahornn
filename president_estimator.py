from persons import Person
import nltk
from nameparser.parser import HumanName

class PresidentEstimator:
    def __init__(self):
        self.persons_of_interest = []
    def getPersonsList(self):
        return self.persons_of_interest
    def appendPersonsList(self, person):
        self.persons_of_interest.append(person)
    def sortListDecreasing(self):
        self.persons_of_interest = sorted(self.persons_of_interest, key=lambda Person: -1 * Person.getOccurence())
    def cropList(self, number=3):
        self.persons_of_interest = self.persons_of_interest[0:number]
    def getHumanNames(self, text):
        tokens = nltk.tokenize.word_tokenize(text)
        pos = nltk.pos_tag(tokens)
        sentt = nltk.ne_chunk(pos, binary = False)
        person = []
        name = ""
        flag = False
        for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
            for leaf in subtree.leaves():
                person.append(leaf[0])
            for part in person:
                name += part + ' '
            for entries in self.persons_of_interest: #checking all existing objects in the list
                if person[-1] == entries.getSurname(): #if the surname is in the list increase occurence
                    flag = True
                    entries.increaseOccurence()
                    break
            if not flag:
                if len(person) > 1:
                    self.appendPersonsList(Person(person[-1], person[0]))#persons_of_interest.append(Person(person[-1],person[0])) #append new object with prename and surname to the list
                else:
                    self.appendPersonsList(Person(person[-1]))#persons.append(Person(person[-1]))

            name = ''
            flag = False
            person = []
    

    
#the labels gpe and gsp indicate countriers or capitals
