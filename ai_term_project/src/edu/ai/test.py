'''
Created on Nov 13, 2012

This is the main module for our checkers game.

@author: Derek F, Alex B, Tyler C
'''

import tkinter as tk
import random as rand
from sys import argv
from edu.ai import piece
#from edu.ai import rule

#Global variables
error_messages = 0
is_jump = False

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global error_messages
        error_messages = tk.StringVar()
        error_messages.set("")
        self.canvas = tk.Canvas(self, width="500", height="500", borderwidth="0")
        self.from_entry = tk.Entry(self)
        self.to_entry = tk.Entry(self)
        self.save_button = tk.Button(self, text="Go!", command=self.makeMove, padx=20)
        fromLabel = tk.Label(self, text="From Position:")
        toLabel = tk.Label(self, text="To Position:")
        tk.Label(self, textvariable=error_messages).grid(row=2, column=0, columnspan=5)
        fromLabel.grid(row=1, column=0)
        self.from_entry.grid(row=1, column=1)
        toLabel.grid(row=1, column=2)
        self.to_entry.grid(row=1, column=3)
        self.save_button.grid(row=1, column=4)
        self.canvas.grid(row=0, column=0, columnspan=5)
        """
        Menu Options (For hopefully selecting AI style and what not)
        """
        self.options = tk.OptionMenu(self, "Menu", "Start")
        self.options.grid(row=0, column=0, columnspan=5)
        
        self.cellwidth = 62.5
        self.cellheight = 62.5
        self.rect = {}
        self.circle = {}
        
        self.theBoard = self.createBoard()
        self.computer = ComputerPlayer(self.theBoard)
        self.redrawFullBoard()
        
        
    
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
        return newBoard
    
    """
    This method is the 'mainloop' of the app, when you click the GO button, this method is fired
    """
    def makeMove(self):
        global error_messages
        global is_jump
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
            self.computer.make_random_move()
            self.computer.minimax(0);
            self.theBoard = self.computer.get_board()
        
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
                    self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2,fill="white",tags="rect")
                else:
                    self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2,fill="black",tags="rect")
                column = column + 1
                if (j != 0):
                    if (j.getPlayer() == 1):
                        self.circle[row, column] = self.canvas.create_oval(x1,y1,x2,y2, fill="red",tags="circle")
                    elif (j.getPlayer() == 2):
                        self.circle[row, column] = self.canvas.create_oval(x1,y1,x2,y2, fill="blue",tags="circle")
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
        if ((originPos[0] < 8) & (originPos[1] < 8) & (originPos[1] >= 0) & (newPos[0] < 8) & (newPos[1] <8) & (newPos[1] >= 0)):
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
            if ((newPos[0]-originPos[0] > 1) | (newPos[0]-originPos[0] < -1)):
                error_messages.set("Invalid move range")
                return False
            if ((newPos[1]-originPos[1] > 1) | (newPos[1]-originPos[1] < -1)):
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
    
    def perform_move(self, current_pos, new_pos):
        xOPos = current_pos[0]
        yOPos = current_pos[1]
        xNPos = new_pos[0]
        yNPos = new_pos[1]
        player = self.board[xOPos][yOPos].getPlayer()
        self.board[xOPos][yOPos] = 0
        self.board[xNPos][yNPos] = piece.Piece(player, xNPos, yNPos)
        return self.board
            
    def make_random_move(self):
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
                return self.perform_move(current_pos, new_pos)
            else:
                newY = current_pos[1] + 1
                new_pos = [newX, newY]
                if (self.validateMove(current_pos, new_pos)):
                    return self.perform_move(current_pos, new_pos)
    
    
    #Test comment for test commit!    
    def minimax(self,count):
        if(count > 3): #Return the best move after X number of iterations
            return 0;
        else:
            print("Count" + count);
            
            ++count #Getting ready for some recursion here
            return self(count)
            
        
        
                
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
            check_jump = self.theBoard[newPos[0]+1][newPos[1]+1]
            jPos = [newPos[0]+1, newPos[1]+1]
            if (check_jump == 0):
                return jPos
        elif (newPos[1] < originPos[1]):
            check_jump = self.theBoard[newPos[0]+1][newPos[1]-1]
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
    