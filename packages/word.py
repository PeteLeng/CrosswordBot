# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 20:02:12 2021

@author: Pete
"""
import random
import numpy as np

class Word(object):
    def __init__(self, word):
        self.word = word
        self.letters = [cha for cha in word]
        self.locations = None
        self.direction = None
        self.xRange = None
        self.yRange = None
        self.default()
    
    def setDirection(self, direction):
        """
        Enter 1 for vertical, 0 for horizontal
        """
        self.direction = direction
        
    def place(self, index, toLoc, direction):
        self.direction = direction
        unit = np.array((0, 1)) if self.direction==1 else np.array((1, 0))
        self.locations = {tuple(np.array(toLoc)+unit*(i-index)):i \
                          for i in range(len(self.letters))}
        self.xRange = (toLoc[0], toLoc[0]) if self.direction==1 \
            else (toLoc[0]-index, toLoc[0]-index+len(self.word)-1)
        self.yRange = (toLoc[1], toLoc[1]) if self.direction==0 \
            else (toLoc[1]-index, toLoc[1]-index+len(self.word)-1)
        
    # def place(self, letter, loc, direction, randm=True):
    #     self.direction = direction
    #     if randm:
    #         index = random.choice([i for i,c in enumerate(self.letters) if c==letter])
    #     else:
    #         index = self.letters.index(letter)
    #     unit = np.array((0, 1)) if self.direction==1 else np.array((1, 0))
    #     self.locations = {tuple(np.array(loc)+unit*(i-index)):self.letters[i] \
    #                       for i in range(len(self.letters))}
    
    def transform(self, del_coordinate):
        newLocs = {tuple(np.array(loc)+np.array(del_coordinate)):idx
                   for loc,idx in self.locations.items()}
        self.locations = newLocs
        del_x, del_y = del_coordinate
        self.xRange = tuple(np.array(self.xRange) + np.array([del_x, del_x]))
        self.yRange = tuple(np.array(self.yRange) + np.array([del_y, del_y]))
    
    def default(self):
        self.place(0, (0, 0), 0)
    
    def getWord(self):
        return self.word
    
    def getLetters(self):
        return self.letters

    def getLetter(self, loc):
        return self.word[self.locations[loc]]
    
    def getDirection(self):
        return self.direction
    
    def getLocations(self):
        return self.locations
    
    def getLocation(self, idx):
        return list(self.locations.keys())[list(self.locations.values()).index(idx)]
    
    def getXRange(self):
        return self.xRange
    
    def getYRange(self):
        return self.yRange
    
    def getNeighbors(self, idx_list):
        """
        Given a list of index, return a list of neighboring locations (tuples) 
        of characters in the index positions of the word.

        Parameters
        ----------
        idx_list : List
        A list of indices
        
        Returns
        -------
        neighbors : List
        A list of neighboring locations of chosen indices

        """
        neighbors = []
        # start = self.getLocation(0)
        # end = self.getLocation(len(self.word)-1)
        if self.getDirection():
            for idx in idx_list:
                idx_loc = self.getLocation(idx)
                if idx == 0:
                    neighbors.append((idx_loc[0], idx_loc[1]-1))
                if idx == len(self.word)-1:
                    neighbors.append((idx_loc[0], idx_loc[1]+1))
                neighbors.append((idx_loc[0]-1, idx_loc[1]))
                neighbors.append((idx_loc[0]+1, idx_loc[1]))
        else:
            for idx in idx_list:
                idx_loc = self.getLocation(idx)
                if idx == 0:
                    neighbors.append((idx_loc[0]-1, idx_loc[1]))
                neighbors.append((idx_loc[0], idx_loc[1]-1))
                neighbors.append((idx_loc[0], idx_loc[1]+1))
                if idx == len(self.word)-1:
                    neighbors.append((idx_loc[0]+1, idx_loc[1]))
        return neighbors
    
    def __str__(self):
        # if self.locations is None:
        #     self.default()
        res = ''
        for loc in self.locations:
            res += '{}: {}'.format(self.getLetter(loc), loc)+'\n'
        return res[:-1]
    
    def __eq__(self, other):
        if self.getWord() != other.getWord():
            print('They are not the same word!')
            return False
        for loc in self.locations:
            if loc not in other.getLocations() or \
                other.getLetter(loc) != self.getLetter(loc):
                    print("They are not in the same location!")
                    return False
        return True
                
    

if __name__ == '__main__':
    apple = Word('APPLE')
    apple.setDirection(0)
    apple.place(0, (0, 1), 0)
    apple2 = Word('APPLE')
    # print(apple == apple2)
    # print(apple.getXRange())
    # print(apple.getYRange())
    # print(apple2.getXRange())
    
    # print(apple.getLetters())
    # print(apple.getDirection())
    # print(apple)
    
    locs = apple.getLocations()
    # print(locs)
    # print((6, 10) in locs)
    
    # Test trasform
    apple.transform((2, 2))
    print(apple.getLocations())
    # print(apple.getLocation(3))
    
    # Test getNeighbor
    print(apple.getDirection())
    print(apple.getNeighbors(range(5)))
    
    # Test getLocation
    
    
    
    