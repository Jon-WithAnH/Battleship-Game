# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 10:55:33 2018

@author: Main Desktop
"""
import random

class BattleShip:

    def __init__(self, shipsTotal,boardDimentions):
        self.totalShipSpaces = 0
        self.noOfShips = shipsTotal
        self.hitShip = "|"
        self.missedShip = "*"
        self.empty = "."
        self.shipFilled = "X"
        self.finalRow = [[self.empty]*boardDimentions for i in range(boardDimentions)]
        self.battleshipLocations = []
        #  used in random num gens
        #  so it doesn't draw a 12 on a 0-11 index board
        self.dimention = boardDimentions - 1
        self.createShips()
        self.makeShipsBigger()
        #  rewrites the board is there are less (or more i guess) ships than there should be
        while not self.checkValidity():
           self.checkValidity()
           self.totalShipSpaces = 0
           self.finalRow = [[self.empty]*boardDimentions for i in range(boardDimentions)]
           self.battleshipLocations = []
           self.createShips()
           self.makeShipsBigger()
        
    def createShips(self):
        for shipToPlace in range(self.noOfShips):
            thisRow, thisColumn = random.randint(0, self.dimention), random.randint(0, self.dimention) 
            while self.finalRow[thisRow][thisColumn] == self.shipFilled:
                #  checks to see is a ship has already been placed at location
                #  and moves it if true
                thisRow, thisColumn = random.randint(0, self.dimention), random.randint(0, self.dimention)
            self.finalRow[thisRow][thisColumn] = self.shipFilled
            #  needs to be added to a pipeline to make the ships bigger
            #  making ships bigger needs to know where to start
            self.battleshipLocations.append([thisRow, thisColumn])
            
    def makeShipsBigger(self):
        for amountToMakeBigger in range(self.noOfShips):
            shipToEnhance = self.battleshipLocations[amountToMakeBigger]
            # Let's do horizontal first
            def goHorizontal():
                if amountToMakeBigger == 0: pass
                #print('%s shouldn\'t grow' % printEnhancment)
                elif shipToEnhance[1] + amountToMakeBigger < self.dimention:
                #  valid
                #print('%s can go right by %s' % (printEnhancment, amountToMakeBigger))
                    for increaseAmount in range(amountToMakeBigger +1):
                        self.finalRow[shipToEnhance[0]][shipToEnhance[1] + increaseAmount] = self.shipFilled
                elif shipToEnhance[1] - amountToMakeBigger > 0: 
                #print('%s can go left by %s' % (printEnhancment, amountToMakeBigger))
                    for increaseAmount in range(amountToMakeBigger +1):
                        self.finalRow[shipToEnhance[0]][shipToEnhance[1] - increaseAmount] = self.shipFilled
                #  valid
            def goVertical():
                if amountToMakeBigger == 0: pass
                #print('%s shouldn\'t grow' % printEnhancment)
                elif shipToEnhance[0] + amountToMakeBigger < self.dimention:
                #  valid
                #print('%s can go right by %s' % (printEnhancment, amountToMakeBigger))
                    for increaseAmount in range(amountToMakeBigger +1):
                        self.finalRow[shipToEnhance[0]  + increaseAmount][shipToEnhance[1]] = self.shipFilled
                elif shipToEnhance[0] - amountToMakeBigger > 0: 
                #print('%s can go left by %s' % (printEnhancment, amountToMakeBigger))
                    for increaseAmount in range(amountToMakeBigger +1):
                        self.finalRow[shipToEnhance[0] - increaseAmount][shipToEnhance[1]] = self.shipFilled
            if random.randint(1,2) == 1:
                goVertical()
            else:
                goHorizontal()
                
    def checkValidity(self):
        for eachList in self.finalRow:
            for eachValueInList in eachList:
                if eachValueInList == self.shipFilled:
                    self.totalShipSpaces += 1
        shouldBeThisManyShips = 0
        for eachShip in range(self.noOfShips):
            shouldBeThisManyShips += (eachShip + 1)
        if self.totalShipSpaces == shouldBeThisManyShips:
            #print('There are the correct amount of ships.')
            return True
        else:
            #print('%s ships on board when there should be %s' % (totalEnlargedShips, shouldBeThisManyShips))
            #print('bad board found...')
            return False
        
    def changeBoard(self, row, column, hitOrMiss):
        #  function only active when attacked
        if hitOrMiss == 'hit':
            self.finalRow[row][column] = self.hitShip
        else:
            self.finalRow[row][column] = self.missedShip

        
    def display(self):
        for eachLine in self.finalRow:
            gg = 0
            for eachValue in eachLine:
                gg += 1
                if gg == self.dimention + 1:
                    print(eachValue, "\n")
                else:
                    print(eachValue, '', end='')
        
    def getBoard(self):
        return self.finalRow
    def getFiller(self):
        return self.shipFilled
    def getTotalShips(self):
        return self.totalShipSpaces

























