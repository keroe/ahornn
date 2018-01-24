from persons import Person
import nltk
from nameparser.parser import HumanName

class PresidentEstimator:
    def __init__(self):
        self.persons_of_interest = []
        self.article_persons = []
    def getPersonsList(self):
        return self.persons_of_interest
    def appendList(self, list, person):
        return list.append(person)
    def sortListDecreasing(self, list):
        sorted_list = sorted(list, key=lambda Person: -1 * Person.getOccurence())
        return sorted_list
    def cropList(self, list, number=3):
        cropped_list = list[0:number]
        return cropped_list
    
    #merge list_2 into list_1
    def mergeLists(self):
        for entries_2 in self.article_persons: #checking all existing objects in the list
            flag = False
            for entries_1 in self.persons_of_interest:
                if entries_1.getSurname() == entries_2.getSurname(): #if the surname is in the list increase occurence
                    flag = True
                    entries_1.addOccurence(entries_2.getOccurence())
                    break
            if not flag:
                    self.persons_of_interest.append(entries_2)#persons.append(Person(person[-1]))
        self.article_persons = []
        self.persons_of_interest = self.sortListDecreasing(self.persons_of_interest)


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
                try:
                    for entries in self.article_persons: #checking all existing objects in the list
                        if person[-1] == entries.getSurname(): #if the surname is in the list increase occurence
                            flag = True
                            entries.increaseOccurence()
                            break
                except TypeError:
                    flag = False
                    #do nothing
                if not flag:
                    if len(person) > 1:
                        self.article_persons.append(Person(person[-1], person[0]))#persons_of_interest.append(Person(person[-1],person[0])) #append new object with prename and surname to the list
                    else:
                        self.article_persons.append(Person(person[-1]))#persons.append(Person(person[-1]))

                name = ''
                flag = False
                person = []
            self.article_persons = self.sortListDecreasing(self.article_persons)
            self.article_persons = self.cropList(self.article_persons)
    

    
#the labels gpe and gsp indicate countriers or capitals
