#!/usr/bin/python

import sys
import json

class Person(object):
    def __init__(self, person):
        self.name = person['name']
        self.boss = person['boss']
        self.score = person['party-animal-score']
        self.children = []

    def getBest(self, ceo=False):

        if len(self.children) == 0:
            return ([self], self.score, True)

        kidsList = []
        kidsScore = 0 
        kidIncluded = False

        for kid in self.children:
            tlist, tscore, tincl = kid.getBest()
            if tscore > 0:
                kidsList.extend(tlist)
                kidIncluded = kidIncluded or tincl
                kidsScore += tscore


        if not kidIncluded:
            return (kidsList + [self], kidsScore, True)
        elif kidsScore > self.score:
            if ceo:
                for child in self.children:
                    for kid in kidsList:
                        if kid.name == child.name:
                            kidsList.remove(kid)
                kidsList.append(self)
            return (kidsList, kidsScore, False)
        else:
            return ([self], self.score, True)

    def addChild(self, person):
        if person:
            self.children.append(person)

    def getPerson(self):
        return {
            'boss': self.boss,
            'name': self.name,
            'score': self.score,
        }

    def printBest(self, ceo=False):
        tlist, tscore, tincl = self.getBest(ceo)
        for person in tlist:
            print person.name

    def isBoss(self):
        return self.boss == None


def buildGraph(people):
    newpeople = {
        person['name']: Person(person)
        for person in people
    }
    for person in newpeople.itervalues():
        boss = person.getPerson()['boss'] 
        if boss is not None:
            newpeople[boss].addChild(person) 
    return newpeople

def getBoss(people):
    for person in people.itervalues():
        if person.isBoss():
            return person

if __name__ == "__main__":
    peoplefile = sys.argv[1]
    people = None
    with open(peoplefile, 'r') as pf:
        people = json.loads(pf.read())
    people = buildGraph(people)
 
    boss = getBoss(people)
    if boss is not None:
        boss.printBest(ceo=False)
    
    # The list always having the CEO:
    #printList(people, 'even')
