# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 11:41:30 2021

@author: Pete
"""
import random
import numpy as np
from word import *

class Crossword(object):
    def __init__(self):
        self.words = []
        # self.allLetters = {}
        # self.openLetters = {}
        self.allLocs = {}
        self.jointLocs = {}
        self.openLocs = {}
        self.xRange = ()
        self.yRange = ()
        
    def getDirection(self, loc):
        """
        Given a location tuple, return the direction of the word on the location.
        The given location has to be an open location.

        Parameters
        ----------
        loc : Tuple, the location tuple of an open location.

        Returns
        -------
        Boolean, 1 for vertical, 0 for horizontal

        """
        return 1 if tuple(np.array(loc) + np.array((0, 1))) in self.allLocs or\
            tuple(np.array(loc) + np.array((0, -1))) in self.allLocs else 0
    
    def checkFit(self, word):
        """
        Given an word object of a particular placement,
        check if the placement fits the crossword.
        
        Parameters
        ----------
        word : Word
        
        Returns
        -------
        Boolean, True if no collision, False otherwise
        
        """
        # Check collison
        idx_list = []
        for i in range(len(word.getWord())):
            loc = word.getLocation(i)
            if loc in self.allLocs:
                if word.getLetter(loc) != self.allLocs[loc]:
                    return False
            else:
                idx_list.append(i)
        
        # Check adjacency
        neighbor_locs = word.getNeighbors(idx_list)
        for neighbor_loc in neighbor_locs:
            if neighbor_loc in self.allLocs:
                return False
        
        # Check friction
        # startLoc = word.getLocation(0)
        # endLoc = word.getLocation(len(word.getWord())-1)
        # if word.getDirection():
        #     startChecks = [(startLoc[0], startLoc[1]-1), (startLoc[0]-1, startLoc[1]), (startLoc[0]+1, startLoc[1])]
        #     endChecks = [(endLoc[0], endLoc[1]+1), (endLoc[0]-1, endLoc[1]), (endLoc[0]+1, endLoc[1])]
        # else:
        #     startChecks = [(startLoc[0]-1, startLoc[1]), (startLoc[0], startLoc[1]-1), (startLoc[0], startLoc[1]+1)] 
        #     endChecks = [(endLoc[0]+1, endLoc[1]), (endLoc[0], endLoc[1]-1), (endLoc[0], endLoc[1]+1)]
        # if startLoc not in self.allLocs:
        #     for loc in startChecks:
        #         if loc in self.allLocs:
        #             return False
        # if endLoc not in self.allLocs:
        #     for loc in endChecks:
        #         if loc in self.allLocs:
        #             return False
        return True
        
    def updateLocs(self, word):
        """
        Given a word that fits in the crossword,
        update locations of the word in the jointLocs, allLocs, openLocs dictionary,
        Go through all jointLocations, update the openLocs inplace.

        Parameters
        ----------
        word : Word, a word object that fits the crossword

        Returns
        -------
        None. updates all locs diction inplace.

        """
        for wLoc in word.getLocations().keys():
            if wLoc in self.allLocs:
                self.jointLocs[wLoc] = word.getLetter(wLoc)
            else:
                self.allLocs[wLoc] = word.getLetter(wLoc)
                self.openLocs[wLoc] = word.getLetter(wLoc)
        for cLoc in self.jointLocs:
            self.updateOpens(cLoc)

    def updateOpens(self, loc):
        """
        Given a location tuple (of a jointLocation),
        update the openLocs dict,
        excluding all openLocations that are 1 unit away from the given location

        Parameters
        ----------
        loc : Tuple, location tuple of a jointLocation.

        Returns
        -------
        None, update the openLocs dictionary inplace

        """
        self.openLocs = {openLoc:cha for openLoc,cha in self.openLocs.items() \
                if abs(openLoc[0]-loc[0])+abs(openLoc[1]-loc[1]) > 1}

    def updateRange(self, word):
        wXRange = word.getXRange()
        wYRange = word.getYRange()
        if not self.xRange or not self.yRange:
            self.xRange = wXRange
            self.yRange = wYRange
        else:
            xHigh = max(self.xRange[1], wXRange[1])
            xLow = min(self.xRange[0], wXRange[0])
            yHigh = max(self.yRange[1], wYRange[1])
            yLow = min(self.yRange[0], wYRange[0])
            self.xRange = (xLow, xHigh)
            self.yRange = (yLow, yHigh)

    def add(self, word):
        self.words.append(word)
        # self.updateLetters(word)
        self.updateLocs(word)
        self.updateRange(word)
        # self.updateOpenLetters()
    
    def refreshLocs(self):
        self.allLocs = {}
        self.jointLocs = {}
        self.openLocs = {}
        for word in self.words:
            for loc in word.getLocations():
                if loc in self.allLocs:
                    self.jointLocs[loc] = word.getLetter(loc)
                else:
                    self.allLocs[loc] = word.getLetter(loc)
        for cLoc in self.jointLocs:
            self.updateOpens(cLoc)
    
    def refreshRange(self):
        self.xRange = ()
        self.yRange = ()
        for word in self.words:
            wXRange = word.getXRange()
            wYRange = word.getYRange()
            if not self.xRange or not self.yRange:
                self.xRange = wXRange
                self.yRange = wYRange
            else:
                xHigh = max(self.xRange[1], wXRange[1])
                xLow = min(self.xRange[0], wXRange[0])
                yHigh = max(self.yRange[1], wYRange[1])
                yLow = min(self.yRange[0], wYRange[0])
                self.xRange = (xLow, xHigh)
                self.yRange = (yLow, yHigh)
        
    def transform(self, del_coordinate):
        [word.transform(del_coordinate) for word in self.words]
        self.refreshLocs()
        self.refreshRange()

    def getWords(self):
        """
        Return a list of word strings in the crossword.

        Returns
        -------
        list, a list of strings

        """
        return [word.getWord() for word in self.words]
    
    def getWord(self, wordString):
        for w in self.words:
            if w.getWord() == wordString:
                return w
    
    # def getLetters(self):
    #     return self.allLetters
    
    # def getOpenLetters(self):
    #     return self.openLetters
    
    def getLocations(self):
        return self.allLocs
    
    def getJoints(self):
        return self.jointLocs
    
    def getOpens(self):
        return self.openLocs
    
    def getDimension(self):
        # xDimen = self.xRange[1] - self.xRange[0] + 1
        # yDimen = self.yRange[1] - self.yRange[0] + 1
        return self.xRange, self.yRange
        
    def __str__(self):
        if not self.words:
            return 'This is an empty crossword!'
        res = ''
        for word in self.words:
            res += 'Location of {}: \n'.format(word.getWord()) +\
                str(word) + '\n'
        return res[:-1]
    
    def __contains__(self, word_or_loc):
        if isinstance(word_or_loc, Word):
            return word_or_loc.getWord() in self.getWords()
        elif isinstance(word_or_loc, tuple):
            return word_or_loc in self.getLocations()
        else:
            return "Incomprehensible type"
    
    def __eq__(self, other):
        for word in self.words:
            if word not in other:
                print("They don't have the same words!")
                return False
            if word != other.getWord(word.getWord()):
                # print("They are not in the same location!")
                return False
        return True


if __name__ == '__main__':
    # wordList = ['CHRISTMAS', 'CHRISTMASEVE', 'COAT', 'LETTER', 'CROSS', \
    #               'TREE', 'DECORATIONS', 'PRESENTS', 'FATHER', 'CHAIR']
    wordList = ['KING', 'XENOMORGPH', 'SIT']
    crossword = Crossword()
    word1 = Word(wordList[0])
    word1.default()
    crossword.add(word1)
    word2 = Word(wordList[1])
    word2.default()
    # for w in wordList:
    #     word = Word(w)
    #     crossword.add(word)
    
    # print(crossword.getWords())
    # print(crossword.getJoints())
    # print(crossword.getLocations())
    
    # place = crossword.placeWord('N', word2)
    # for i in place:
    #     print(i)
    
    print(crossword)
    print("Dimension of {}: {}".format(crossword.getWords(), crossword.getDimension()))
    
    # Test refresh
    # crossword.refreshLocs()
    # print('Refreshed', crossword)
    # print('Refreshed dimension {}: {}'.format(crossword.getWords(), crossword.getDimension()))
    
    # Test transform
    # crossword.transform((5, 5))
    # crossword.refreshLocs()
    # print('Transformed', crossword)
    # print(crossword.getLocations())
    # print('Transformed dimension', crossword.getDimension())
    
    # Test in
    print(word1 in crossword)
    print(word2 in crossword)
    for loc in word1.getLocations().keys():
        print(loc in crossword)


# %%

    # def findCommons(self, word):
    #     """
    #     Given an Word object, go through the openLetters dict,
    #     return a list containting all common letters

    #     Parameters
    #     ----------
    #     word : Word, 

    #     Returns
    #     -------
    #     List, of all common letters between given Word and crossword openLetters.
        
    #     """
    #     # if not self.words:
    #     #     return word.getLetters()
    #     return [cha for cha in word.getLetters() if cha in self.openLetters]
    
    # def findOpens(self, letter):
    #     return [loc for loc,cha in self.openLocs.items() if cha==letter]

    # def placeWord(self, commonLet, word):
    #     """
    #     Given an word object and a selected common letter,
    #     get all open locations of selected letter in the crossword,
    #     place the given word on the crossword according to the chosen open location,
    #     return a generator that generates all possible word placement

    #     Parameters
    #     ----------
    #     commonLet : String, selected from findCommons list
        
    #     word : Word object

    #     Yields
    #     ------
    #     word : Word object, a generator that generates all possible placement,
    #     for all possible openLocations of a given commonLetter
    #     A deterministic process.
        
    #     """
    #     locList = self.openLetters[commonLet].copy()
    #     while locList:
    #         commonLoc = locList.pop(0)
    #         wDirection = not self.getDirection(commonLoc)
    #         word.place(commonLet, commonLoc, wDirection)
    #         yield word
    
    # def add(self, word):
    #     if self.words == None:
    #         # word.place(word.getLetters[0], (0, 0))
    #         word.default()
    #         self.words = [word]
    #         self.updateLetters(word)
    #         self.updateLocs(word)
    #         self.updateOpenLetters()
    #     else:
    #         try:
    #             commonLet = random.choice(self.findCommons(word))
    #         except:
    #             print('No common openletter, skip {}'.format(word.getWord()))
    #         else:
    #             commonLoc = random.choice(self.openLetters[commonLet])
    #             wDirection = not self.getDirection(commonLoc)
    #             word.place(commonLet, commonLoc, wDirection)
    #             if self.checkFit(word):
    #                 self.words.append(word)
    #                 self.updateLetters(word)
    #                 self.updateLocs(word)
    #                 self.updateOpenLetters()
    #             else:
    #                 print('Collision with others, skip {}'.format(word.getWord()))

    # def updateLetters(self, word):
    #     """
    #     Given a word that fits in the crossword,
    #     update the allLetters dictionary.

    #     Parameters
    #     ----------
    #     word : Word

    #     Returns
    #     -------
    #     None, update allLetters dict inplace.

    #     """
    #     # if self.allLetters == None:
    #     #     self.allLetters = {}
    #     wordLocs = word.getLocations()
    #     for cha in word.getLetters():
    #         try:
    #             self.allLetters[cha] + [loc for loc,let in wordLocs.items() if let==cha]
    #         except:
    #             self.allLetters[cha] = [loc for loc,let in wordLocs.items() if let==cha]
    
    # def updateOpenLetters(self):
    #     """
    #     Based on current openLocs dictionary,
    #     recreate the openLetters dictionary.

    #     Returns
    #     -------
    #     None, update the openLetters dict inplace

    #     """
    #     self.openLetters = {}
    #     for cwLoc in self.openLocs:
    #         cwLet = self.openLocs[cwLoc]
    #         try:
    #             self.openLetters[cwLet] + [cwLoc]
    #         except:
    #             self.openLetters[cwLet] = [cwLoc]
