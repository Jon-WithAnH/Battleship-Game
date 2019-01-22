# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 16:50:39 2018

@author: Main Desktop
"""
try:
    import ChangingBattleship
    import BattleshipShooter
    import tkinter
    from PIL import Image, ImageTk
    import socket
    from threading import Thread
    from pickle import dumps, loads
    from time import sleep
except Exception as ex:
    print(ex)
    input('Import error. Press enter to exit')
    raise 'Do not continue with this'



class myApp(tkinter.Tk):
    def __init__(self, totalBoats, boardSize):
        tkinter.Tk.__init__(self)
        self.totalBoats = totalBoats
        self.boardSize = boardSize
        # object variables
        self.player2= None
        self.player1 = ChangingBattleship.BattleShip(totalBoats,boardSize)
        
        ## NETWORKING STUFF ##
        networking = True
        if networking:
            hoster = input('Press enter if you are not John\n')
            if hoster == 'true':
                self.submitValid = True
                self.playerNum, self.otherPlayerNum = 1 , 2
                self.host = '0.0.0.0'
                self.startConnectionHost()
                self.recvBoard()
                self.sendBoard()
            else:
                self.submitValid = False
                self.playerNum, self.otherPlayerNum = 2, 1
                print("CLIENT NETWORKING OPTION SELECTED\n\n")
                self.host = input("Enter IP Provided by John: ")
                self.startConnectionClient()
                self.sendBoard()
                self.recvBoard()
            print('Initalizing thread...')
            Thread(target=self.recvChat, name='recv').start()
            
        # basic things about the tkinter window        
        self.title('Battleship!')
        # Geometry does (y, x), so y value is first
        self.geometry("800x600")        
        self.playerLabel = tkinter.Label(self, text=("You are player %s!" % self.playerNum))
        self.playerLabel.pack()
        self.entryBox = tkinter.Entry(self)

        self.label = tkinter.Label(self, text="Hit submit to fire!")  
        self.label.place(x=0,y=145)
        self.entryBox2 = tkinter.Entry(self)
        self.entryBox2.place(x=0, y=170)
        self.entryBox.place(x=0,y=125)
        self.l2 = tkinter.Label(self, text="The status of your \nshot will apear here")
        self.l2.place(x=130,y=180)
        self.chatEntryBox = tkinter.Entry(self, width=80)

        self.xChatBase = 105
        self.chatBase = 300
        self.chatEntryBox.place(x=self.xChatBase-5,y=self.chatBase + 210)
        self.chatBackground = tkinter.Label(self, width=68, height=8, background='white')
        self.chatBackground.place(x=self.xChatBase-5,y=self.chatBase+75)
        
        #print(self.otherPlayersBoard, self.otherPersonsBoard)
        self.otherPlayersBoard = self.player2.getBoard()
        self.filledShip = self.player2.shipFilled
        self.currentPlayerShots = BattleshipShooter.shootAt(self.player2)
                
        self.shotHistory = self.currentPlayerShots.shotHistory
        self.showBoardOnGUI(280, 50, self.shotHistory)


        self.prevMessages = []

        self.bind("<Return>", self.sendChat)
        self.createLabels()
        self.createButtons()
        self.showMeMyBoard()
    
    def updateShootingBoard(self):
        # runs when the other player rerolls their board.
        # just updates the shot board
        self.otherPlayersBoard = self.player2.getBoard()
        self.filledShip = self.player2.shipFilled
        self.currentPlayerShots = BattleshipShooter.shootAt(self.player2)
        self.shotHistory = self.currentPlayerShots.shotHistory
        ## TODO: self.shotHistory is what needs to be sent. Find out how to
        # have recv board or whatever accept a placement for it. ty.
        self.showBoardOnGUI(280, 50, self.shotHistory)
    
    def twoSubmitFuncs(self):
        rowOFshot, columnOFshot = int(self.entryBox.get())-1, int(self.entryBox2.get())-1
        y =self.currentPlayerShots.shotHistory[rowOFshot][columnOFshot]
        self.maybeShowUpdatedButton(y)
        #self.currentPlayerShots.displayPrevShots()
        # determines if player can take a shot, and if so, whether they hit or miss
        if self.submitValid:
            if self.otherPlayersBoard[rowOFshot][columnOFshot] == '.':
                self.submitValid = False
                self.currentPlayerShots.attack(int(self.entryBox.get()), int(self.entryBox2.get()))
                self.maybeShowUpdatedButton('You\'ve missed! Other person\'s turn')
                self.c.send(bytes('pass code 546451222', encoding='ascii'))
                self.currentTurnLabelUpdater()
            elif self.otherPlayersBoard[rowOFshot][columnOFshot] == 'X':
                self.currentPlayerShots.attack(int(self.entryBox.get()), int(self.entryBox2.get()))
                self.maybeShowUpdatedButton('You hit them!\nGo again!')
            else:
                        #self.currentPlayerShots.attack(int(self.entryBox.get()), int(self.entryBox2.get()))
                self.maybeShowUpdatedButton('You\'ve already shot here!\nStill your turn!')
            self.showBoardOnGUI(280, 50, self.shotHistory)
            pickledHistory = dumps(self.shotHistory)
            self.c.send(pickledHistory)
        else:
            self.maybeShowUpdatedButton('It\'s not your turn yet')
        
    def currentTurnLabelUpdater(self):
        if self.submitValid == False:
            player = self.otherPlayerNum
        else: player = self.playerNum
        self.currentTurnDisplayer.destroy()
        self.currentTurnDisplayer = tkinter.Label(self, text='Player %s\'s turn' % player)
        self.currentTurnDisplayer.place(x=20, y=15)
        
        
    def sendBoard(self):
        print('Sending board')
        data=dumps(self.player1)
        self.c.send(data)
        print('Successfully sent')
        
    def recvBoard(self):
        print('Attempting to load other players board')
        x = self.c.recv(1024)
        hi = self.player2=loads(x)
        #print(hi, 'revied')
        self.showBoardOnGUI(800, 50, hi.getBoard())
        print('Board recieved')
        
    def getActiveEntryBox(self):
        # TODO I don't know if this is possible or not.
        # when the enter key is pressed, get what entryBox is active
        # and submit the relavent function to the entry field
        pass
    
    ## NETWORKING ##
    def startConnectionHost(self):
        print('ATTEMPTING TO CONNECT TO CLIENT...')
        self.s = socket.socket()
        host = self.host # IP of host machine
        port = 7002
        self.s.bind((host,port))        
        self.s.listen(1) # allows for only 1 active connection
        self.c, addr = self.s.accept()
        print('Got connection from', addr)
        
    def submitBoard(self):
        # destorys tutoritals and enables user to fire
        self.rerollBoard.destroy()
        self.sendBoardButton.destroy()
        self.shotHistoryBoard.destroy()
        self.finalTutorial.destroy()
        self.OwnBoardTutorial.destroy()
        button = tkinter.Button(self, text='Submit', command=self.twoSubmitFuncs)
        button.place(x=130,y=140)
        
    def startConnectionClient(self):
        self.s = socket.socket()
        host = self.host
        port = 7002
        while True:
            try: 
                self.s.connect((host, port))
                break
            except Exception:
                print('Connection failed to host: %s \nFrom port: %s'% (host, port))
                sleep(3)
        # makes it so I don't have to change any variable names between host and client
        self.c = self.s
    
    def recvChat(self):
        while True:
            x = self.c.recv(1024)
            try:
                # pickle rickkkk
                self.player2=loads(x)
                if type(self.player2) == ChangingBattleship.BattleShip:
                    # means that the other player has rerolled their board
                    # so current player has to receive and update their
                    # existing board.
                    self.showBoardOnGUI(800, 50, self.player2.getBoard())
                    self.updateShootingBoard()
                else:
                    # should mean this is a shothistory board
                    # I know this is weird, but in this case
                    # player 2 will = their SHOTHISTORY
                    self.showBoardOnGUI(self.chatBase+90, 200, self.player2)
            except:
                x = x.decode('utf-8')
                if x == 'pass code 546451222':
                    self.submitValid = True
                    self.currentTurnLabelUpdater()
                #self.prevMessages.append(tkinter.Label(self,text=('Them: %s' % self.c.recv(1024).decode('utf-8')), background='white'))
                else:
                    self.prevMessages.append(tkinter.Label(self,text=('Them: %s' % x), background='white'))
                    self.updateChat('do nothing with this')
    
    def sendToOtherPerson(self):
        self.c.send(bytes(self.chatEntryBox.get(), encoding='ascii'))
    
    # the bind function sends some info with it to this function automatically.
    # i don't know what to do with it so i don't think it's important
    def sendChat(self, doNothingWithThis):
        # first we set where the top of the chat appears
        # 225-18
        self.prevMessages.append(tkinter.Label(self,text=('You: %s' % self.chatEntryBox.get()), background='white')) # adds a label to the list for easy looping
        # reset and focus on the chat Entry box so content within are deleted, and you can continue to type
        try:self.sendToOtherPerson()
        except AttributeError: print("No active connection. Chat function disabled")
        self.updateChat(self.chatEntryBox.get())
        self.chatEntryBox.destroy()
        self.chatEntryBox = tkinter.Entry(self, width=80)
        self.chatEntryBox.place(x=self.xChatBase-5,y=self.chatBase + 210)
        self.chatEntryBox.focus()
        
    def updateChat(self, doNothingWithThis):
        self.y = self.chatBase + 75
        if len(self.prevMessages) >= 7: # chat box only comfortables displays 7 lines, so destory old labels and delete them from list
            self.prevMessages[0].destroy()
            del self.prevMessages[0]
        for eachMessage in range(len(self.prevMessages)): # print the suckers
            self.prevMessages[eachMessage].place(x=self.xChatBase, y=self.y)
            self.y += 18 # drops the next label down some so there's no overlap between messages
        
    ## LABELS AND BUTTON ON START ##
        
    def createLabels(self):
        self.shotHistoryBoard = tkinter.Label(self, text='Shows the areas you\'ve shot --->')
        self.shotHistoryBoard.place(x=100,y=100)
        self.OwnBoardTutorial = tkinter.Label(self,text='<-- This is your own board.\nClick the button up top to reroll it')
        self.OwnBoardTutorial.place(x=610,y=100)
        self.finalTutorial = tkinter.Label(self, text='Click here once you\'ve read all stuff and are satisfied with your board-->')
        self.finalTutorial.place(x=250, y=195)
        self.currentTurnDisplayer = tkinter.Label(self, text='Player 1\'s turn')
        self.currentTurnDisplayer.place(x=20, y=15)
        self.otherPersonShotTutorial = tkinter.Label(self, text='Places enemy has shot -->')
        self.otherPersonShotTutorial.place(x=self.chatBase-90, y=260)
        # func to create a bunch of buttons
    def createButtons(self):
        self.rerollBoard = tkinter.Button(self, text='Reroll own board', command=self.rerollPlayersBoard)
        self.rerollBoard.place(x=510, y=30)        
        # fire submit button moved to sendBoard function to prevent firing before
        # board is finalized        
        self.sendBoardButton = tkinter.Button(self, text='Finalize Board', background ='red', command=self.submitBoard)
        self.sendBoardButton.place(x=635,y=190)
        
    # works in tandem with the getInputBoxField method
    def maybeShowUpdatedButton(self,message):
        try: self.l2.destroy() # removes old label so there's no ugly overlap
        except AttributeError: pass
        self.l2 = tkinter.Label(self, text=message)
        self.l2.place(x=130,y=190)
    
    # When a the submit button is pressed, it will activate this function which grabs the entered fields
    # and sends a message to the update label function, which will update the user about their shot.
    def getInputBoxField(self):
        try:
            if self.otherPlayersBoard[int(self.entryBox.get()) -1][int(self.entryBox2.get())-1] == self.filledShip:
                self.currentPlayerShots.attack(int(self.entryBox.get()), int(self.entryBox2.get()))
                self.maybeShowUpdatedButton('Hit!')
            else: 
                self.currentPlayerShots.attack(int(self.entryBox.get()), int(self.entryBox2.get()))
                self.maybeShowUpdatedButton('Miss')
        except ValueError:
            self.maybeShowUpdatedButton('A field is blank.\nShot not sent.')
        
    def showMeMyBoard(self):
        # shows player their own board so they can decide if they
        # reroll it if they desire
        player1Board = self.player1.getBoard()
        self.showBoardOnGUI(500, 50, player1Board)
        
    def rerollPlayersBoard(self):
        # creates a new board and displays it
        self.player1 = ChangingBattleship.BattleShip(self.totalBoats,self.boardSize)
        self.showMeMyBoard()
        self.sendBoard()
            
            
    def showBoardOnGUI(self, xPoint, yPoint, whatBoard):
        #  Simply creates the board on screen with the relavant imagery
        i, j = xPoint, yPoint
        for eachList in whatBoard:
            j +=20
            i= xPoint
            ## WARNING ##
            # if the labels aren't updated in the for loops, it won't update the display
            # of the list for some reasons. they have to be there.
            for eachValue in eachList:
                if eachValue == ".":
                    image = Image.open("sea.png")
                    photo = ImageTk.PhotoImage(image)
                    label2 = tkinter.Label(image=photo)   
                    label2.image = photo # keep a reference!
                    label2.place(x=i,y=j)
                elif eachValue == "|" or eachValue == "X":
                    hitImage = Image.open("hit.png")
                    photoOFhit = ImageTk.PhotoImage(hitImage)
                    labelOFhit = tkinter.Label(image=photoOFhit)
                    labelOFhit.image = photoOFhit # keep a reference!
                    labelOFhit.place(x=i,y=j)
                elif eachValue == "*":
                    imageOFmiss = Image.open("miss.png")
                    photoOFmiss = ImageTk.PhotoImage(imageOFmiss)
                    labelOFmiss = tkinter.Label(image=photoOFmiss)
                    labelOFmiss.image = photoOFmiss # keep a reference!
                    labelOFmiss.place(x=i,y=j)
                else:
                    print('Mystery value found: %s' % eachValue)
                i += 20    
try:      
    app = myApp(5,6)
    app.mainloop()
except Exception as ex:
    print(ex)
    input('\n\n\nError in main loop. Show this to John!')
    
# TODO Label row and column of shot  Entry box
# todo label row and column of grids
    
# TODO flash screen when turn

