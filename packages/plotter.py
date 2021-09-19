# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 17:29:11 2021

@author: Pete
"""
from word import *
from crossword import *
from fitter import *

def plot(crossword, display_size):
    x_range, y_range = crossword.getDimension()
    x_del = round(display_size/2 - (x_range[0] + x_range[1])/2)
    y_del = round(display_size/2 - (y_range[0] + y_range[1])/2)
    crossword.transform((x_del, y_del))
    return crossword

def rand_testcase(word_list):
    return randomCrosswords(word_list)

def gen_testcase(word_list):
    return genCrosswords(word_list)

if __name__ == "__main__":
    # Build test cases
    wordList = ['CHRISTMAS', 'CHRISTMASEVE', 'COAT', 'LETTER', 'CROSS', \
                  'TREE', 'DECORATIONS', 'PRESENTS', 'FATHER', 'CHAIR']
    rand_test = ran_testcase(wordList)
    gen_test = gen_testcase(wordList)

    # Test transformer
    # print('Before transformation', ran_test[0].getDimension())
    print(plot(ran_test[0], 15))
    # plot(ran_test[0], 18)
    # print('After transformation', ran_test[0].getDimension())
    # print(ran_test[0].getLocations())
    # print(next(gen_test))
    
    
    
    
    
    
    
    
    
    