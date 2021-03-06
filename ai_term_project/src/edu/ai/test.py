'''
Created on Nov 13, 2012

This is the main module for our checkers game.

@author: Derek F, Alex B, Tyler C
'''

import tkinter as tk
import random as rand
import sys as system
from sys import argv
from edu.ai import piece

#Global variables
option_str = ''
error_messages = 0
move_messages = 0
is_jump = False

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global error_messages
        global move_messages
        global option_str
        error_messages = tk.StringVar()
        error_messages.set("")
        move_messages = tk.StringVar()
        move_messages.set("")
        self.canvas = tk.Canvas(self, width="500", height="500", borderwidth="0")
        self.from_entry = tk.Entry(self)
        self.to_entry = tk.Entry(self)
        self.save_button = tk.Button(self, text="Go!", command=self.makeMove, padx=20)
        fromLabel = tk.Label(self, text="From Position:")
        toLabel = tk.Label(self, text="To Position:")
        tk.Label(self, textvariable=error_messages).grid(row=3, column=0, columnspan=5)
        tk.Label(self, textvariable=move_messages).grid(row=4, column=0, columnspan=5)
        fromLabel.grid(row=2, column=0)
        self.from_entry.grid(row=2, column=1)
        toLabel.grid(row=2, column=2)
        self.to_entry.grid(row=2, column=3)
        self.save_button.grid(row=2, column=4)
        self.canvas.grid(row=1, column=0, columnspan=5)
        """
        Menu Options (For hopefully selecting AI style and what not)
        """
        ai_label = tk.Label(self, text="AI Type:")
        ai_label.grid(row=0,column=0)
        optionlist = ('Random', 'Rule-Based')
        option_str = tk.StringVar();
        option_str.set(optionlist[0])
        self.options = tk.OptionMenu(self, option_str, *optionlist)
        self.options.grid(row=0, column=1)
        #Restart button
        self.restart_button = tk.Button(self, text="Restart",command=self.restart_game,padx=20)
        self.restart_button.grid(row=0, column=2)
        #Exit button
        self.exit_button = tk.Button(self, text="Exit",command=self.exit_game,padx=20)
        self.exit_button.grid(row=0,column=3)
        
        self.cellwidth = 62.5
        self.cellheight = 62.5
        self.rect = {}
        self.circle = {}
        
        self.theBoard = self.createBoard()
        self.computer = ComputerPlayer(self.theBoard)
        self.redrawFullBoard()
        
        """
        def optionCallBack(self, *args):
            if (option_str.get() == 'Exit'):
                system.exit(0)                
        option_str.trace('w', optionCallBack)
        """       
    
    """
    Generates the initial gamestate, each piece is its own class called Piece.
    A piece has 3 parameters:
        - The player number (can be 1 for computer, 2 for player)
        - The row number in the grid (between 0 and 7)
        - The column number (between 0 and 7)
    A piece must have knowledge of its initial position or it cannot do anything else
    """        
    def createBoard(self):
        
        newBoard = [[0,piece.Piece(1,0,1),0,piece.Piece(1,0,3),0,piece.Piece(1,0,5),0,piece.Piece(1,0,7)],
                    [piece.Piece(1,1,0),0,piece.Piece(1,1,2),0,piece.Piece(1,1,4),0,piece.Piece(1,1,6),0],
                    [0,piece.Piece(1,2,1),0,piece.Piece(1,2,3),0,piece.Piece(1,2,5),0,piece.Piece(1,2,7)],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [piece.Piece(2,5,0),0,piece.Piece(2,5,2),0,piece.Piece(2,5,4),0,piece.Piece(2,5,6),0],
                    [0,piece.Piece(2,6,1),0,piece.Piece(2,6,3),0,piece.Piece(2,6,5),0,piece.Piece(2,6,7)],
                    [piece.Piece(2,7,0),0,piece.Piece(2,7,2),0,piece.Piece(2,7,4),0,piece.Piece(2,7,6),0]]
        """
        newBoard = [[0,0,0,0,0,0,0,0],
                    [piece.Piece(1,1,0),0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,piece.Piece(2,3,2),0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0.0,0],
                    [0,0,0,0,0,piece.Piece(1,6,5),0,0],
                    [0,0,0,0,0,0,0,0]]
        """
        return newBoard
    
    def restart_game(self):
        self.theBoard = self.createBoard()
        self.redrawFullBoard()
        
    def exit_game(self):
        system.exit(0)
    
    def check_if_new_king(self):
        row = self.theBoard[0]
        for n in row:
            if (n != 0):
                if ((n.getPlayer() == 2) & (n.getIsKing()==False)):
                    n.set_is_king()
        return False
    
    """
    This method is the 'mainloop' of the app, when you click the GO button, this method is fired
    """
    def makeMove(self):
        global error_messages
        global is_jump
        global option_str
        
        if (self.is_game_over() == False):
            originLoc = self.from_entry.get()
            newLoc = self.to_entry.get()
            error_messages.set("Move = " + originLoc + " -> " + newLoc)
        
            originPos = [int(n) for n in originLoc.split(",")]
            newPos = [int(n) for n in newLoc.split(",")]
            """
            If the move is valid, makes the player's move is successful, and the computer goes
            """
            if (self.validateMove(originPos, newPos)):
                self.playerMove(originPos, newPos)
                self.redrawFullBoard()
        
                #Controls computer move    
                self.computer.update_board(self.theBoard)
                if (option_str.get() == "Random"):
                    self.computer.make_random_move() 
                elif (option_str.get() == "Rule-Based"):
                    self.computer.make_rule_based_move() #Not actually performing moves yet, I have this called for debugging purposes!
                
                self.theBoard = self.computer.get_board()
        
            self.check_if_new_king()
            self.computer.check_if_new_king()
            self.redrawFullBoard()
    
    """
    This is the logic for determining a players move, whether it's valid, and whether it is a jump or not
    """    
    def playerMove(self, originPos, newPos):        
        if (self.validateMove(originPos, newPos)):
            xOPos = originPos[0]
            yOPos = originPos[1]
            xNPos = newPos[0]
            yNPos = newPos[1]
            
            if ((is_jump == True) & (self.check_if_jump(originPos, newPos) != False)):
                player = self.theBoard[xOPos][yOPos].getPlayer()
                
                jumpPos = self.check_if_jump(originPos, newPos)
                xJPos = jumpPos[0]
                yJPos = jumpPos[1]
                self.theBoard[xOPos][yOPos] = 0
                self.theBoard[xNPos][yNPos] = 0
                self.theBoard[xJPos][yJPos] = piece.Piece(player, xJPos, yJPos)
            else:    
                player = self.theBoard[xOPos][yOPos].getPlayer()
                self.theBoard[xOPos][yOPos] = 0
                self.theBoard[xNPos][yNPos] = piece.Piece(player, xNPos, yNPos)
        
            self.redrawFullBoard()
            return True
        return False
    
    def is_game_over(self):
        comp_pieces = 0
        player_pieces = 0
        for rows in self.theBoard:
            for square in rows:
                if (square != 0):
                    if (square.getPlayer() == 1):
                        comp_pieces += 1
                    else:
                        player_pieces += 1
        if ((player_pieces<=0)|(comp_pieces<=0)):
            return True
        
        return False
    """
    Function to redraw the checkers board whenever a change is made
    """        
    def redrawFullBoard(self):              
        row = 0
        column = 0
        for i in self.theBoard:
            column = 0;
            for j in i:
                x1 = column*self.cellwidth
                y1 = row*self.cellheight
                x2 = x1+self.cellwidth
                y2 = y1+self.cellheight
                if ((column % 2 == 0) ^ (row % 2 == 0)):
                    self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2,fill="black",tags="rect")
                else:
                    self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2,fill="gray",tags="rect")
                column = column + 1
                if (j != 0):
                    if (j.getPlayer() == 1):
                        self.circle[row, column] = self.canvas.create_oval(x1,y1,x2,y2, fill="red",tags="circle")
                        if (j.getIsKing() == True):
                            self.canvas.create_text(x1+30, y1+30, text="K")
                    elif (j.getPlayer() == 2):
                        self.circle[row, column] = self.canvas.create_oval(x1,y1,x2,y2, fill="blue",tags="circle")
                        if (j.getIsKing() == True):
                            self.canvas.create_text(x1+30, y1+30, text="K")
            row = row + 1
        self.from_entry.delete(0, tk.END)
        self.to_entry.delete(0, tk.END)
    
    """
    Validates a player's move entry to check if they have entered incorrect positions, incorrect
    directions, or if it's a jump move
    """        
    def validateMove(self, originPos, newPos):
        global error_messages
        global is_jump
        is_jump = False
        if ((originPos[0] < 8) and (originPos[1] < 8) and (originPos[1] >= 0) and (newPos[0] < 8) and (newPos[1] <8) and (newPos[1] >= 0)):
            posValue = self.theBoard[originPos[0]][originPos[1]]
            newValue = self.theBoard[newPos[0]][newPos[1]]
            if (posValue == 0):
                error_messages.set("No valid piece at position")
                return False
            if (posValue.getPlayer() == 1):
                error_messages.set("Invalid piece selected")
                return False
            if (posValue.getIsKing() == False):
                if (newPos[0]-originPos[0] >= 0):
                    error_messages.set("Invalid Move Direction")
                    return False
                if (newPos[1] == originPos[1]):
                    error_messages.set("Invalid Move Direction")
                    return False
            if ((newPos[0]-originPos[0] > 1) or (newPos[0]-originPos[0] < -1)):
                error_messages.set("Invalid move range")
                return False
            if ((newPos[1]-originPos[1] > 1) or (newPos[1]-originPos[1] < -1)):
                error_messages.set("Invalid move range")
                return False
            if (newValue != 0):
                if (newValue.getPlayer() == 1):
                    error_messages.set("Jump")
                    is_jump = True            
                    return True
                else:
                    error_messages.set("Occupied")
                    return False
            return True
    
    """
    Called whenever the game need to check if a move is a jump. If it is this function
    returns the location of where the piece will land, otherwise returns false
    """
    def check_if_jump(self, originPos, newPos):
        global error_messages
        global is_jump
        
        if (is_jump == False):
            return False
        
        check_jump = {}
        if (newPos[1] > originPos[1]):
            check_jump = self.theBoard[newPos[0]-1][newPos[1]+1]
            jPos = [newPos[0]-1, newPos[1]+1]
            if (check_jump == 0):
                return jPos
        elif (newPos[1] < originPos[1]):
            check_jump = self.theBoard[newPos[0]-1][newPos[1]-1]
            jPos = [newPos[0]-1, newPos[1]-1]
            if (check_jump == 0):
                return jPos
        return False      

"""
This class contains the functionality of the computer opponent, since it has
different validation and logic that it needs
"""    
class ComputerPlayer():
    def __init__(self, initBoard):
        self.board = initBoard
    
    def update_board(self, newBoard):
        self.board = newBoard
        
    def get_board(self):
        return self.board
    
    def check_if_new_king(self):
        row = self.board[7]
        for n in row:
                if (n != 0):
                    if ((n.getPlayer() == 1) & (n.getIsKing()==False)):
                        n.set_is_king()
        return False
    
    def perform_move(self, current_pos, new_pos):
        global is_jump
        xOPos = current_pos[0]
        yOPos = current_pos[1]
        
        if (is_jump == False):
            xNPos = new_pos[0]
            yNPos = new_pos[1]
            player = self.board[xOPos][yOPos].getPlayer()
            self.board[xOPos][yOPos] = 0
            self.board[xNPos][yNPos] = piece.Piece(player, xNPos, yNPos)
            return self.board
        else:
            xNPos = new_pos[0][0]
            yNPos = new_pos[0][1]
            xJPos = new_pos[1][0]
            yJPos = new_pos[1][1]
            player = self.board[xOPos][yOPos].getPlayer()
            self.board[xOPos][yOPos] = 0
            self.board[xNPos][yNPos] = 0
            self.board[xJPos][yJPos] = piece.Piece(player, xJPos, yJPos)
            return self.board
            
    def make_random_move(self):
        global move_messages
        validMove = False
        for p in self.board:
            for check in p:
                if (check != 0):
                    check.set_looked_at(False)
                    
        while (validMove == False):
            current_piece = self.find_piece()
            current_pos = current_piece.get_current_pos()
            newX = current_pos[0] + 1
            newY = current_pos[1] - 1
            new_pos = [newX, newY]
            if (self.validateMove(current_pos, new_pos)):
                move_messages.set("Random Move!")
                return self.perform_move(current_pos, new_pos)
            else:
                newY = current_pos[1] + 1
                new_pos = [newX, newY]
                if (self.validateMove(current_pos, new_pos)):
                    move_messages.set("Random Move!")
                    return self.perform_move(current_pos, new_pos)
    
    
    def make_rule_based_move(self):
        global move_messages
        
        #First Rule
        for p in self.board:
            for check in p:
                if((check != 0) and (check.player == 1)):
                    #This will look through all of the computer's pieces
                    if(self.rule1(check) != False):
                        move_messages.set("Jump Rule Used")
                        return self.perform_move(check.get_current_pos(), self.rule1(check))
        
        #Second Rule
        for p in self.board:
            for check in p:
                if((check != 0) and (check.player == 1)):
                    #This will look through all of the computer's pieces
                    if(self.rule3(check) != False):
                        move_messages.set("King Rule Used")
                        return self.perform_move(check.get_current_pos(), self.rule3(check))
                    
        #Third Rule
        for p in self.board:
            for check in p:
                if((check != 0) and (check.player == 1)):
                    #This will look through all of the computer's pieces
                    if(self.rule2(check) != False):
                        move_messages.set("Protective Random Used")
                        return self.perform_move(check.get_current_pos(), self.rule2(check))
        
        
        #If no rules were matched the game will make a random move
        return self.make_random_move()
                        
                    
    
    #Rule 1 is just a template for making more rule methods!
    #Iterates over all the possible moves a computer piece can make
    def ruleTemplate(self,piece):
        original_pos = piece.get_current_pos();
        
        #Looking at the board:
        #Down and to the right
        newX = original_pos[0]+1
        newY = original_pos[1]+1
        new_pos = [newX,newY]
        if(self.validateMove(original_pos,new_pos)):
            return True
        
        #Down and to the left
        newX = original_pos[0]+1
        newY = original_pos[1]-1
        new_pos = [newX,newY]
        if(self.validateMove(original_pos,new_pos)):
            return True
                                                    
        #King's only
        if(piece.getIsKing == True):
            
            #Up and to the right
            newX = original_pos[0]-1
            newY = original_pos[1]+1
            new_pos = [newX,newY]
            if(self.validateMove(original_pos,new_pos)):
                return True
            
            #Up and to the left
            newX = original_pos[0]-1
            newY = original_pos[1]-1
            new_pos = [newX,newY]
            if(self.validateMove(original_pos,new_pos)):
                return True
            
        return False #None of these triggered the rule
        
    #Rule 2 checks for a player piece to jump on!
    def rule1(self,piece):
        original_pos = piece.get_current_pos();
        
        #Looking at the board:
        #Down and to the right
        newX = original_pos[0]+1
        newY = original_pos[1]+1
        new_pos = [newX,newY]
        if(self.validateMove(original_pos,new_pos)):
            lookingAt = self.get_board()[new_pos[0]][new_pos[1]]
            if(lookingAt != 0):
                if(lookingAt.getPlayer() == 2):
                    return [new_pos, self.check_if_jump(original_pos, new_pos)]
        
        #Down and to the left
        newX = original_pos[0]+1
        newY = original_pos[1]-1
        new_pos = [newX,newY]
        if(self.validateMove(original_pos,new_pos)):
            lookingAt = self.get_board()[new_pos[0]][new_pos[1]]
            if(lookingAt != 0):
                if(lookingAt.getPlayer() == 2):
                    return [new_pos, self.check_if_jump(original_pos, new_pos)]
                                                    
        #King's only
        if(piece.getIsKing == True):
            
            #Up and to the right
            newX = original_pos[0]-1
            newY = original_pos[1]+1
            new_pos = [newX,newY]
            if(self.validateMove(original_pos,new_pos)):
                lookingAt = self.get_board()[new_pos[0]][new_pos[1]]
                if(lookingAt != 0):
                    if(lookingAt.getPlayer() == 2):
                        return [new_pos, self.check_if_jump(original_pos, new_pos)]
            
            #Up and to the left
            newX = original_pos[0]-1
            newY = original_pos[1]-1
            new_pos = [newX,newY]
            if(self.validateMove(original_pos,new_pos)):
                lookingAt = self.get_board()[new_pos[0]][new_pos[1]]
                if(lookingAt != 0):
                    if(lookingAt.getPlayer() == 2):
                        return [new_pos, self.check_if_jump(original_pos, new_pos)]
            
        return False #None of these triggered the rule
    
    #First move that doesn't endanger the piece (essentially an improved random move) Should be used last in the rule list in most cases
    def rule2(self,piece):
        original_pos = piece.get_current_pos();
        
        #Looking at the board:
        #Down and to the right
        newX = original_pos[0]+1
        newY = original_pos[1]+1
        new_pos = [newX,newY]
        if(self.validateMove(original_pos,new_pos)):
            #Start Here
            safe = True
            lookingAt = self.get_board()[new_pos[0]][new_pos[1]]
            #Down and to the right
            newX2 = newX + 1
            newY2 = newY + 1
            new_pos2 = [newX2,newY2]
            if((newX2 < 8) and (newX2 >= 0) and (newY2 < 8) and (newY2 >= 0)):
                lookingAt2 = self.get_board()[new_pos2[0]][new_pos2[1]]
                if(lookingAt2 != 0):
                    if(lookingAt2.getPlayer() == 2):
                        safe = False
            #Down and to the left
            newX2 = newX + 1
            newY2 = newY - 1
            new_pos2 = [newX2,newY2]
            if((newX2 < 8) and (newX2 >= 0) and (newY2 < 8) and (newY2 >= 0)):
                lookingAt2 = self.get_board()[new_pos2[0]][new_pos2[1]]
                if(lookingAt2 != 0):
                    if(lookingAt2.getPlayer() == 2):
                        safe = False
            if(piece.getIsKing == True):
                #Up and to the right
                newX2 = newX - 1
                newY2 = newY + 1
                new_pos2 = [newX2,newY2]
                if((newX2 < 8) and (newX2 >= 0) and (newY2 < 8) and (newY2 >= 0)):
                    lookingAt2 = self.get_board()[new_pos2[0]][new_pos2[1]]
                    if(lookingAt2 != 0):
                        if(lookingAt2.getPlayer() == 2):
                            safe = False
                #Up and to the left
                newX2 = newX - 1
                newY2 = newY - 1
                new_pos2 = [newX2,newY2]
                if((newX2 < 8) and (newX2 >= 0) and (newY2 < 8) and (newY2 >= 0)):
                    lookingAt2 = self.get_board()[new_pos2[0]][new_pos2[1]]
                    if(lookingAt2 != 0):
                        if(lookingAt2.getPlayer() == 2):
                            safe = False
            #End Here
            if(safe == True):
                return new_pos
        
        #Down and to the left
        newX = original_pos[0]+1
        newY = original_pos[1]-1
        new_pos = [newX,newY]
        if(self.validateMove(original_pos,new_pos)):
            #Start Here
            safe = True
            lookingAt = self.get_board()[new_pos[0]][new_pos[1]]
            #Down and to the right
            newX2 = newX + 1
            newY2 = newY + 1
            new_pos2 = [newX2,newY2]
            if((newX2 < 8) and (newX2 >= 0) and (newY2 < 8) and (newY2 >= 0)):
                lookingAt2 = self.get_board()[new_pos2[0]][new_pos2[1]]
                if(lookingAt2 != 0):
                    if(lookingAt2.getPlayer() == 2):
                        safe = False
            #Down and to the left
            newX2 = newX + 1
            newY2 = newY - 1
            new_pos2 = [newX2,newY2]
            if((newX2 < 8) and (newX2 >= 0) and (newY2 < 8) and (newY2 >= 0)):
                lookingAt2 = self.get_board()[new_pos2[0]][new_pos2[1]]
                if(lookingAt2 != 0):
                    if(lookingAt2.getPlayer() == 2):
                        safe = False
            if(piece.getIsKing == True):
                #Up and to the right
                newX2 = newX - 1
                newY2 = newY + 1
                new_pos2 = [newX2,newY2]
                if((newX2 < 8) and (newX2 >= 0) and (newY2 < 8) and (newY2 >= 0)):
                    lookingAt2 = self.get_board()[new_pos2[0]][new_pos2[1]]
                    if(lookingAt2 != 0):
                        if(lookingAt2.getPlayer() == 2):
                            safe = False
                #Up and to the left
                newX2 = newX - 1
                newY2 = newY - 1
                new_pos2 = [newX2,newY2]
                if((newX2 < 8) and (newX2 >= 0) and (newY2 < 8) and (newY2 >= 0)):
                    lookingAt2 = self.get_board()[new_pos2[0]][new_pos2[1]]
                    if(lookingAt2 != 0):
                        if(lookingAt2.getPlayer() == 2):
                            safe = False
            #End Here
            if(safe == True):
                return new_pos
                                                    
        #King's only
        if(piece.getIsKing == True):
            
            #Up and to the right
            newX = original_pos[0]-1
            newY = original_pos[1]+1
            new_pos = [newX,newY]
            if(self.validateMove(original_pos,new_pos)):
                #Start Here
                safe = True
                lookingAt = self.get_board()[new_pos[0]][new_pos[1]]
                #Down and to the right
                newX2 = newX + 1
                newY2 = newY + 1
                new_pos2 = [newX2,newY2]
                if((newX2 < 8) and (newX2 >= 0) and (newY2 < 8) and (newY2 >= 0)):
                    lookingAt2 = self.get_board()[new_pos2[0]][new_pos2[1]]
                    if(lookingAt2 != 0):
                        if(lookingAt2.getPlayer() == 2):
                            safe = False
                #Down and to the left
                newX2 = newX + 1
                newY2 = newY - 1
                new_pos2 = [newX2,newY2]
                if((newX2 < 8) and (newX2 >= 0) and (newY2 < 8) and (newY2 >= 0)):
                    lookingAt2 = self.get_board()[new_pos2[0]][new_pos2[1]]
                    if(lookingAt2 != 0):
                        if(lookingAt2.getPlayer() == 2):
                            safe = False
                if(piece.getIsKing == True):
                    #Up and to the right
                    newX2 = newX - 1
                    newY2 = newY + 1
                    new_pos2 = [newX2,newY2]
                    if((newX2 < 8) and (newX2 >= 0) and (newY2 < 8) and (newY2 >= 0)):
                        lookingAt2 = self.get_board()[new_pos2[0]][new_pos2[1]]
                        if(lookingAt2 != 0):
                            if(lookingAt2.getPlayer() == 2):
                                safe = False
                    #Up and to the left
                    newX2 = newX - 1
                    newY2 = newY - 1
                    new_pos2 = [newX2,newY2]
                    if((newX2 < 8) and (newX2 >= 0) and (newY2 < 8) and (newY2 >= 0)):
                        lookingAt2 = self.get_board()[new_pos2[0]][new_pos2[1]]
                        if(lookingAt2 != 0):
                            if(lookingAt2.getPlayer() == 2):
                                safe = False
                #End Here
                if(safe == True):
                    return new_pos
            
            #Up and to the left
            newX = original_pos[0]-1
            newY = original_pos[1]-1
            new_pos = [newX,newY]
            if(self.validateMove(original_pos,new_pos)):
                #Start Here
                safe = True
                lookingAt = self.get_board()[new_pos[0]][new_pos[1]]
                #Down and to the right
                newX2 = newX + 1
                newY2 = newY + 1
                new_pos2 = [newX2,newY2]
                if((newX2 < 8) and (newX2 >= 0) and (newY2 < 8) and (newY2 >= 0)):
                    lookingAt2 = self.get_board()[new_pos2[0]][new_pos2[1]]
                    if(lookingAt2 != 0):
                        if(lookingAt2.getPlayer() == 2):
                            safe = False
                #Down and to the left
                newX2 = newX + 1
                newY2 = newY - 1
                new_pos2 = [newX2,newY2]
                if((newX2 < 8) and (newX2 >= 0) and (newY2 < 8) and (newY2 >= 0)):
                    lookingAt2 = self.get_board()[new_pos2[0]][new_pos2[1]]
                    if(lookingAt2 != 0):
                        if(lookingAt2.getPlayer() == 2):
                            safe = False
                if(piece.getIsKing == True):
                    #Up and to the right
                    newX2 = newX - 1
                    newY2 = newY + 1
                    new_pos2 = [newX2,newY2]
                    if((newX2 < 8) and (newX2 >= 0) and (newY2 < 8) and (newY2 >= 0)):
                        lookingAt2 = self.get_board()[new_pos2[0]][new_pos2[1]]
                        if(lookingAt2 != 0):
                            if(lookingAt2.getPlayer() == 2):
                                safe = False
                    #Up and to the left
                    newX2 = newX - 1
                    newY2 = newY - 1
                    new_pos2 = [newX2,newY2]
                    if((newX2 < 8) and (newX2 >= 0) and (newY2 < 8) and (newY2 >= 0)):
                        lookingAt2 = self.get_board()[new_pos2[0]][new_pos2[1]]
                        if(lookingAt2 != 0):
                            if(lookingAt2.getPlayer() == 2):
                                safe = False
                #End Here
                if(safe == True):
                    return new_pos
                
        return False #None of these triggered the rule
            
        #Can it make a king?
    def rule3(self,piece):
        original_pos = piece.get_current_pos();
        
        #Looking at the board:
        #Down and to the right
        newX = original_pos[0]+1
        newY = original_pos[1]+1
        new_pos = [newX,newY]
        if(self.validateMove(original_pos,new_pos)):
            if(newX == 7):
                return new_pos
        
        #Down and to the left
        newX = original_pos[0]+1
        newY = original_pos[1]-1
        new_pos = [newX,newY]
        if(self.validateMove(original_pos,new_pos)):
            if(newX == 7):
                return new_pos
                                                    
        #King's only - not required here!
            
        return False #None of these triggered the rule
        
                
    def find_piece(self):
        foundPiece = False        
        while (foundPiece == False):
            guess = rand.randint(0, 12)
            count = 0
            for i in self.board:
                for j in i:
                    if (j != 0):
                        if ((j.getPlayer() == 1) & (j.getLookedAt() == False) & (guess <= count)):
                            j.set_looked_at(True)
                            return j
                    count += 1
    
    def check_if_jump(self, originPos, newPos):
        global error_messages
        global is_jump
        
        if (is_jump == False):
            return False
        
        check_jump = {}
        if (newPos[1] > originPos[1]):
            check_jump = self.board[newPos[0]+1][newPos[1]+1]
            jPos = [newPos[0]+1, newPos[1]+1]
            if (check_jump == 0):
                return jPos
        elif (newPos[1] < originPos[1]):
            check_jump = self.board[newPos[0]+1][newPos[1]-1]
            jPos = [newPos[0]+1, newPos[1]-1]
            if (check_jump == 0):
                return jPos
        return False   
                    
    def validateMove(self, originPos, newPos):
        global error_messages
        global is_jump
        is_jump = False
        if ((originPos[0] < 8) & (originPos[1] < 8) & (originPos[1] >= 0) & (newPos[0] < 8) & (newPos[1] <8) & (newPos[1] >= 0)):
            posValue = self.board[originPos[0]][originPos[1]]
            newValue = self.board[newPos[0]][newPos[1]]
            if (posValue == 0):
                return False
            if (posValue.getPlayer() == 2):
                return False
            if (posValue.getIsKing() == False):
                if (newPos[0]-originPos[0] <= 0):
                    return False
                if (newPos[1] == originPos[1]):
                    return False
            if (newValue != 0):
                if (newValue.getPlayer() == 2):
                    error_messages.set("Jump")
                    is_jump = True            
                    return True
                else:
                    error_messages.set("Occupied")
                    return False
            return True
        
if __name__ == "__main__":
    app = App()
    app.resizable(0, 0)
    app.mainloop()
    