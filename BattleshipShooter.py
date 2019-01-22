# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 16:15:54 2018

@author: Main Desktop
"""

class shootAt:
    '''
    needs to accept input to a target locations
    has to check the board at that locations
    if ship is at location, shot a hit
    if not, show a miss
    '''
    def __init__(self, otherPlayer):
        self.otherPlayer = otherPlayer
        self.otherPlayersBoard = otherPlayer.getBoard()
        #  Has to add 1 here because in the main file, I subtract 1 to help with indexing
        self.dimension = self.otherPlayer.dimention+1
        #  TODO this should be change so it can auto adjust somehow. probably through get functions
        self.shotHistory = [[self.otherPlayer.empty]*self.dimension for i in range(self.dimension)]
        
    def attack(self, rowTarget, columnTarget):
        #  for indexing purposes, rowtarget and columntarget need to be reduced by 1 b/c the player will input index + 1
        #  b/c that's how our brains work
        rowTarget -= 1
        columnTarget -= 1
        if self.otherPlayersBoard[rowTarget][columnTarget] == self.otherPlayer.shipFilled and self.otherPlayersBoard[rowTarget][columnTarget] != self.otherPlayer.empty:
            self.shotHistory[rowTarget][columnTarget] = "|"
            self.otherPlayer.changeBoard(rowTarget, columnTarget, 'hit')
            return 'Hit'
        elif self.otherPlayersBoard[rowTarget][columnTarget] == self.otherPlayer.missedShip or self.otherPlayersBoard[rowTarget][columnTarget] == self.otherPlayer.hitShip:
            return 'You\'ve already shot here!' 
        else:
            self.shotHistory[rowTarget][columnTarget] = "*"
            self.otherPlayer.changeBoard(rowTarget, columnTarget, 'miss')
            return 'Miss'
            
    def displayPrevShots(self, **optional):
        print(self.shotHistory, 'shot history')
        for eachLine in self.shotHistory:
            gg = 0
            #print(eachLine, ' each line')
            for eachValue in eachLine:
                gg += 1
                if gg == self.dimension:
                    print(eachValue, "\n")
                else:
                    print(eachValue, '', end='')
        if optional:
            print('Enemy Board below')
            self.otherPlayer.display()
    
    
