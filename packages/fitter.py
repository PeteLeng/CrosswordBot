# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 12:50:36 2021

@author: Pete
"""
import copy
import random
from word import *
from crossword import *


def findMatchs(word, crossword):
    """
    Given a word and a crossword, 
    find all combinations of matching letters between the word and the crossword,
    return the index, loc tuples of all matches.
    
    Parameters
    ----------
    word : Word
    crossword : Crossword

    Returns
    -------
    List, a list of 2-tuples.
    First element is the index of the match in the word,
    second element is the key of the match in the crossword openLocs dictionary.

    """
    # return [cha for cha in word.getLetters() \
    #         if cha in crossword.getOpenLetters()]
    return [(i,loc) for i in range(len(word.getLetters())) 
            for loc in crossword.getOpens() 
            if word.getLetters()[i] == crossword.getOpens()[loc]]

def genFits(word, crossword):
    """
    Given a word and crossword, 
    return a generator that generate all possible fits.

    Parameters
    ----------
    word : Word
    
    crossword : Crossword

    Yields
    ------
    Crossword.

    """
    if not crossword.getWords():
        fit = copy.deepcopy(crossword)
        fit.add(copy.deepcopy(word))
        yield fit
    if word not in crossword:
        matchList = findMatchs(word, crossword)
        while matchList:
            wIndex, cwLoc = matchList.pop(0)
            wDirection = not crossword.getDirection(cwLoc)
            word.place(wIndex, cwLoc, wDirection)
            if crossword.checkFit(word):
                fit = copy.deepcopy(crossword)
                fit.add(copy.deepcopy(word))
                yield fit
    else:
        print('Duplicate word')
        yield crossword
    
def makeCrosswords(wordList):
    words = [Word(w) for w in wordList]
    cwSpace = [Crossword()]
    for word in words:
        new = [fit for cw in cwSpace 
               for fit in genFits(word, cw)]
        cwSpace = new if new else cwSpace
    return cwSpace

def dfsCrosswords(wordList, cwList=[Crossword()]):
    """
    Returns
    -------
    List, a list of crosswords that exhausts the wordList, 
    empty list if none is found
    This is so profound! In recursive functions, 
    variable values in the lower layer does not carry back into the higher layer.
    When constructing recursive functions, think about one layer above the base cases.

    """
    if not wordList:
        return cwList
    word = Word(wordList[0])
    result = []
    for crossword in cwList:
        fits = [cw for cw in genFits(word, crossword)]
        if fits:
            result += dfsCrosswords(wordList[1:], fits)
    return result

def genCrosswords(wordList, cwList=[Crossword()]):
    if not wordList:
        for cw in cwList:
            yield cw
    else:
        word = Word(wordList[0])
        find_fit = False
        for crossword in cwList:
            fits = [cw for cw in genFits(word, crossword)]
            if fits:
                yield from genCrosswords(wordList[1:], fits)
                find_fit = True
        if not find_fit:
            for crossword in cwList:
                yield crossword

def randomCrosswords(wordList, cwList=[Crossword()]):
    if not wordList:
        return cwList
    word = Word(wordList[0])
    result = []
    for crossword in cwList:
        fits = [cw for cw in genFits(word, crossword)]
        random.shuffle(fits)
        if fits:
            result += randomCrosswords(wordList[1:], fits)
        if result:
            break
    return result

def printCrosswords(cwList):
    res = ''
    for cw in cwList:
        wordsText = ''
        for word in cw.getWords():
            wordsText += word + ', '
        res += 'The crossword is made up of <{}>\n'.format(wordsText[:-2])
        res += str(cw) + '\n'
    print (res[:-1])
    
# def get_frenquecy(wordList):


if __name__ == '__main__':
    w1 = Word('APPLE')
    w2 = Word('PINEAPPLE')
    w3 = Word('WATERMELLON')
    cw1 = Crossword()
    # cw2 = cw1
    cw3 = copy.deepcopy(cw1)
    cw1.add(w1)
    cw3.add(w3)
    
    # Test findMatches
    # matches = findMatchs(w2, cw1)
    # print(matches)
    
    # Test genFits
    fits = genFits(w2, cw1)
    print(next(fits))
    # cws = [fit for fit in fits]
    # for fit in fits:
    #     cws.append(fit)
    #     print(fit, '\n')
    # print(cws)
    
    # Test makeCrosswords
    # cwList = makeCrosswords(['APPLE', 'PEACH', 'ZZ'])
    # print(cwList[0], cwList[1], sep='\n')
    
    # Test genFits, adding duplicate word to a crossword
    # for cw in genFits(w1, cw1):
    #         print(cw, end='\n')
    # next(genFits(w1, cw1))
    
    # Test dfs
    # fits = dfsCrosswords(['APPLE', 'PEACH', 'STREET'], [Crossword()])
    # print(fits)
    # printCrosswords(fits)
    # dfsFits = dfsCrosswords(['APPLE', 'PEACH', 'DONUT', 'ROBOT'], [Crossword(), cw1])
    # print('\nResult:')
    # for cw in dfsFits:
    #     print(cw, end='\n')
    
    # Test generator
    # genCWs = genCrosswords(['APPLE', 'PEACH', 'ROBOT'], [Crossword()])
    # try:
    #     print(next(genCWs))
    # except StopIteration:
    #     print('No crossword made!')
    # count = 0
    # for cw in genCWs:
    #     # print(cw.xRange)
    #     # print(cw.yRange)
    #     print("Dimension of {}: {}".format(cw.getWords(), cw.getDimension()))
    #     print(cw, '\n')
    #     count += 1
    # print(count)
        
    # Test randomCrosswords
    # randomFits = randomCrosswords(['APPLE', 'PEACH'], [Crossword()])
    # print(randomFits)

    # Test Word equality
    # print(dfsFits[0])
    # testWord = Word('ROBOT')
    # testWord.place(0, (5,3), 0)
    # cwTest = dfsFits[0]
    # print(cwTest.getWord('ROBOT') == testWord)
    
    # Test Crossword equality
    # k = 0
    # for cw in dfsFits:
    #     if cw == cwTest:
    #         k += 1
    # print(k)
        

# %%

# def dfsCrosswords(wordList, cwList, verbose=True):
#     """
#     Given a list of word strings and a list of crosswords,
#     fit the first word into every crossword in the cwList, 
#     for each crossword, generate a new list of crosswords that fits the first word,
#     if the new list is not empty, fit the second word into every crosswords in the list,
#     and so on, until the wordList runs out, and return the cwList.
#     When the first crossword that exhaust the whole wordList is found,
#     break the loop, and return the result

#     Parameters
#     ----------
#     wordList : List, a list of word strings
        
#     cwList : List, a list of Crosswords objects
        
#     verbose : Boolean, optional, whether to print out process, default True

#     Returns
#     -------
#     List, a list of crosswords that exhausts the wordList, 
#     empty list if none is found

#     """
#     if not wordList:
#         print(wordList)
#         return cwList
#     word = Word(wordList[0])
#     # print('Fit', word.getWord())
#     result = []
#     for crossword in cwList:
#         print('Fit {} into {}'.format(word.getWord(), crossword.getWords()) )
#         fits = [cw for cw in genFits(word, crossword)]
#         if verbose:
#             for cw in fits:
#                 print(cw.getWords(), end='\n')
#             print('______')
#         if fits:
#              result = dfsCrosswords(wordList[1:], fits)
#         if result:
#             break
#     # else:
#     #     result = cwList
#     return result

# =============================================================================
# def dfsCrosswords(wordList, cwList, level=1, verbose=False):
#     """
# 
#     Parameters
#     ----------
#     wordList : List, a list of word strings
#         
#     cwList : List, a list of Crosswords objects
#         
#     verbose : Boolean, optional, whether to print out process, default True
# 
#     Returns
#     -------
#     List, a list of crosswords that exhausts the wordList, 
#     empty list if none is found
# 
#     """
#     if not wordList:
#         return cwList
#     word = Word(wordList[0])
#     # print('Fit', word.getWord())
#     collection = []
#     result = []
#     for crossword in cwList:
#         fits = [cw for cw in genFits(word, crossword)]
#         if verbose:
#             print('Fit {} into {}'.format(word.getWord(), crossword.getWords()))
#             for cw in fits:
#                 print(cw.getWords(), end='\n')
#             print('______')
#         if fits:
#             print('{} fits, enter recursion {}'.format(word.getWord(), level))
#             result = dfsCrosswords(wordList[1:], fits, level+1)
#             print('result is {}, out of recursion {}'.format(len(result), level))
#         if result:
#             print('result is {}, at recursion {}, add to collection'.format(len(result),level))
#             collection += result
#     # else:
#     #     result = cwList
#     return collection
# =============================================================================
