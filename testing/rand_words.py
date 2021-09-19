# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 21:58:25 2021

@author: Pete
"""
import random

def load_words(file_name):
    with open(file_name) as f:
        words = []
        for line in f:
            words.append(f.readline().strip('\n'))
    return words

def rand_words(words, num):
    if num > len(words):
        return 'Not enough words'
    return [words[random.choice(range(len(words)))] for i in range(num)]

def write_words(words):
    with open('C:\\Pete\\Project\\Crossword\\test_words.txt', 'w') as f:
        for word in words:
            f.write(word + '\n')

if __name__ == '__main__':
    words = load_words('sports.txt')
    test_words = rand_words(words, 10)
    print(test_words)
    write_words(test_words)