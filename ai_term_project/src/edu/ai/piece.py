'''
Created on Nov 23, 2012

This module contains the Piece class
Test Commit
@author: Derek F
'''

class Piece:
    '''
    Class representing a checkers piece.  Needs to have knowledge of it's initial position
    as well as which player controls it.
    
    @param playerType: 1 for Computer, 2 for Player
    @param row: Row number of piece (0 to 7)
    @param column: Column number of piece (0 to 7)
    @var looked_at: For the computer to decide if it's already tried moving this piece
    @var is_king: Describes whether a piece is a king or not    
    '''
    def __init__(self, playerType, row, column):
        self.is_king = False
        self.player = playerType #If this is 1 - computer if 2 - player
        self.position = [row, column]
        self.looked_at = False
        
    def getPlayer(self):
        return self.player     
        
    def getIsKing(self):
        return self.is_king
    
    def getLookedAt(self):
        return self.looked_at
    
    def set_looked_at(self, val):
        self.looked_at = val
        
    def get_current_pos(self):
        return self.position
    
    def set_new_pos(self, val):
        self.position = val
        
    def set_is_king(self):
        self.is_king = True
        