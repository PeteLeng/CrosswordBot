# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 21:45:00 2021

@author: Pete
"""
import random

def get_freq(word_list):
    freq_dict = {}
    for word in word_list:
        unique_letters = []
        for letter in word:
            if letter not in unique_letters:
                unique_letters.append(letter)
        for letter in unique_letters:
            freq_dict[letter] = freq_dict.get(letter, 0) + 1 if letter in freq_dict else 0
    return freq_dict

def freq_score(word, freq_dict):
    return sum([freq_dict[letter] for letter in word])

def freq_sort(word_list, start, end):
    freq_dict = get_freq(word_list)
    if start != end:
        pivot = random.choice(range(start, end+1))
        if pivot != start:
            word_list[start], word_list[pivot] = word_list[pivot], word_list[start]          
        i = start + 1
        for j in range(start+1, end+1):
            if freq_score(word_list[j], freq_dict) > freq_score(word_list[start], freq_dict):
                if i < j:
                    word_list[j], word_list[i] = word_list[i], word_list[j]
                    i += 1
                else:
                    i += 1
        word_list[start], word_list[i-1] = word_list[i-1], word_list[start]
        # print('find index {}'.format(i-1))
        # Bug if there's no check
        if i-1 > start: 
            freq_sort(word_list, start, i-2)
        if i-1 < end:
            freq_sort(word_list, i, end)

def freq_shuffle(word_list, start, end, n):
    freq_dict = get_freq(word_list)
    pivot = random.choice(range(start, end+1))
    word_list[start], word_list[pivot] = word_list[pivot], word_list[start]
    i = start + 1
    for j in range(start + 1, end+1):
        if freq_score(word_list[j], freq_dict) > freq_score(word_list[start], freq_dict):
            if i < j:
                word_list[j], word_list[i] = word_list[i], word_list[j]
                i += 1
            else:
                i += 1
    word_list[start], word_list[i-1] = word_list[i-1], word_list[start]
    if i-1 > n:
        freq_shuffle(word_list, start, i-2, n)
    elif i-1 < n:
        freq_shuffle(word_list, i, end, n)

def _test_get_freq(word_list):
    print(get_freq(word_list))


if __name__ == '__main__':
    l1 = ['car', 'robot', 'cat', 'machine', 'learning']
    l2 = ['CHRISTMAS', 'CHRISTMASEVE', 'COAT', 'LETTER', 'CROSS', 'TREE', 'DECORATIONS', 'PRESENTS', 'FATHER', 'CHAIR']
    l3 = ['CHRISTMAS', 'CHRISTMASEVE', 'COAT', 'LETTER', 'CROSS', 'TREE', 'DECORATIONS', 'PRESENTS', 'FATHER', 'CHAIR']
    _test_get_freq(l2)
    freq = get_freq(l2)
    for w in l2:
        print(w, ':', freq_score(w, freq))
    
    # freq_sort(l1, 0, 4)
    # print(l1)
    
    freq_sort(l2, 0, 9)
    print(l2)
    freq_shuffle(l3, 0, 9, 4)
    print(l3)
    