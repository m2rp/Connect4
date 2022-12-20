# Author: Prem Manoharan
# Created: Nov 2022
# Email: prem6556@gmail.com

import random
import math
import numpy as np
from tkinter import *
import pathlib
import pygubu
import time

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "gui_1.ui"
COLS = 7

def check_index(board,row,col):
    R,C = board.shape
    if row>=R or row<0: return False
    if col >=C or col<0: return False
    return True

def check_around(board,row,col,who): #Function to check vicotry status of a player at a given r,c
    win = True
    #Check right
    for i in range(4): 
        if check_index(board,row,col+i):
           # print("Checking  ", row, col+i, " with value ", board[row][col+i])
            if board[row][col+i] != who:
                win = False
                break
        else:
            win = False
            break
    if win: 
       # print("Won checking right")
        return win
    else: win = True
    #Check Up
    for i in range(4): 
        if check_index(board,row-i,col):
            if board[row-i][col] != who:
                win = False
                break
        else:
            win = False
            break
    if win: 
       # print("Won checking up")
        return win
    else: win = True

    #Check diag-up-right
    for i in range(4): 
        if check_index(board,row-i,col+i):
            if board[row-i][col+i] != who:
                win = False
                break
        else:
            win = False
            break
    if win: 
        #print("Won checking up right")
        return win
    else: win = True
    #Check diag-up-left
    for i in range(4): 
        if check_index(board,row-i,col-i):  
            if board[row-i][col-i] != who:
                win = False
                break
        else:
            win = False
            break
            
        #print("Won checking up left")       
    return win

 
def find_free_row(board,row,col):
    row -= 1
    while (row >=0):
        if board[row][col] == 0:
            return row
        row -= 1
    print("Error - no available row")
    return -1

def np_convert(board):
    if isinstance(board, np.ndarray): 
        #print("Already numpy")
        return board

    rows = int(len(board)/7)
    board = np.array(board).reshape(rows,7)
    return np.flip(board,0)

def check_move(board, turn, col, pop,com=0):
    board = np_convert(board)
    R,C = board.shape
    if col <0 or col >6: #col is out of range
        print("Invalid column")
        return False   
    if pop:
        if board[R-1][col] == turn:
            return True
        else:
            if com==0: print("Cannot pop disc at selected column")
            return False#Check if bottom row disc in col is same as player       
    else:
        if board[0][col] != 0: #Column is already full -> Cant place a disc here
            if com==0: print("Columns is already full. Please pick a differnt column")
            return False
    return True

def apply_move(board, turn, col, pop):
    board = np_convert(board)
    R,C = board.shape
    row = -1 
    #display_board(board)
    if pop:
        r = R-1
        while r >0:
            board[r][col] = board[r-1][col]
            r -= 1
        board[r][col] = 0 #Add new empty element at the top
    else:
        row = find_free_row(board,R,col)#Find row that disc can be placed at 
        board[row][col] = turn #Place disc
    return 

def check_victory(board, who_played):
    board = np_convert(board)
    R,C = board.shape
    p1 = False
    p2 = False
    for row in range(R-1,-1,-1):
        for col in range(C):
            if board[row][col] == 1 and p1 == False:
                p1 = check_around(board,row,col,1)
            if board[row][col] == 2 and p2 == False: #Only check victory condition for player 2 if p2 victory not found yet
                p2 = check_around(board,row,col,2)
            if p1 and p2: #If both conditions found, other player wins (from rules)
                if who_played == 1:
                    print("Player 2 has won after pop") 
                    return 2 
                else:
                    print("Player 1 has won after pop")
                    return 1
    
    if p1: 
        #print("Player 1 has won")
        return 1 
    if p2: 
        #print("Player 2 has won")
        return 2
    return 0

class Connect4:
    def __init__(self):
        print("Initialising Connect4")
        self.rows = 7 #To be input from user
        self.cols = COLS 
        self.turn = 1 #Default to player 1 first
        self.colour = ['Empty','#0000ff','#ff0000'] #blue,red
        self.size_of_board = 600
        self.circle_size = self.size_of_board//min(self.rows,self.cols) - 10
        self.whoIsPlaying = None # 0 is human, 1 is computer
        self.mainwindow = None
        self.builder = self.initBuilder("5")
        self.run()
 
    #GUI Functions --------------------------------
    def initBuilder(self,windowNumber):
        builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.previous = self.mainwindow #Store previous window for display purposes
        self.mainwindow = builder.get_object("toplevel"+windowNumber)
        builder.connect_callbacks(self)
        return builder
    def initBoard(self):
        #Internal board (np array)
        self.board = np.zeros((self.rows,self.cols),dtype=int) #Create board
       #GUI board 
        self.builder = self.initBuilder("3") 
        self.canvas = self.builder.get_object("canvas2")
        #self.canvas.bind("<1>", self.boardClick)
        self.display_board()

    def rowEnter(self):
        self.rows = self.builder.tkvariables['rows'].get()
        if self.rows >= 1 and self.rows<15:
            self.mainwindow.destroy()
            self.builder = self.initBuilder("1")  
        
    def human_button_click(self):
        print("Human button clicked")
        self.mainwindow.destroy()
        self.whoIsPlaying = 0 #0 for human, 1 for computer
        self.initBoard() 
        
    def comp_button_click(self):  
        print("Computer button clicked")
        self.mainwindow.destroy()
        self.whoIsPlaying = 1 #0 for human, 1 for computer
        self.builder = self.initBuilder("2") 
   
    def inputLevel(self, level):
        self.level = int(level)

    def playLevel(self):
        if self.level:
            print("Choosing level ",self.level)
            self.mainwindow.destroy()
            self.initBoard()
        else:
           #Display choose message
           pass 
  
    def drawLines(self):
        for i in range(self.rows):
            self.canvas.create_line(0, (i + 1) * self.size_of_board / self.rows, self.size_of_board, (i + 1) * self.size_of_board / self.rows)
        for i in range(self.cols-1):
            self.canvas.create_line((i + 1) * self.size_of_board / self.cols, 0, (i + 1) * self.size_of_board / self.cols, self.size_of_board)
  
        
    def drawCircle(self,row,col,colourIndex): #Draw circle to represent player move
        y,x = row*self.size_of_board//self.rows + 5, col*self.size_of_board//self.cols + 5
        self.canvas.create_oval(x,y,x+self.circle_size,y+self.circle_size,outline = "black",fill = self.colour[colourIndex],width = 2)
    
    def run(self):
        self.mainwindow.mainloop()
    
    def boardClick(self, event=None):
        #Click positioning
        grid_position = [event.x, event.y]
        #print(grid_position)
        row,col = self.convert_grid_to_logical_position(grid_position)
        print(row,col)
        self.player_move(col,row)
        
        if self.checkEnd()==False and self.whoIsPlaying and self.turn == 2: #Comp move
                print("Computer move:")
                self.computer_move()

   
    def EndGame(self):
        print(f"Player {self.win} has won")
        print("Thanks for playing Connect4!")
        self.builder = self.initBuilder("6")
        self.label = self.builder.get_variable("whoWon")
        self.label.set(f"Player {self.win} has won")
    def play_again(self):
        self.mainwindow.destroy()
        self.previous.destroy()
        Connect4()
    def no_play_again(self):
        self.mainwindow.destroy()
        self.previous.destroy()
    
    def display_board(self):
        print(self.board)
        self.canvas.delete("all")
        self.drawLines()
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row,col]>0:
                    self.drawCircle(row,col,self.board[row,col])
    #Logical functions------------------------
    def convert_grid_to_logical_position(self,grid_position):
        grid_position = np.array(grid_position)
        grid_position[1] = grid_position[1] // (self.size_of_board / self.rows)
        grid_position[0] = grid_position[0] // (self.size_of_board / self.cols)
        return np.array(grid_position, dtype=int)
    
    def nextPlayer(self): #CHange player turn and colours
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1
        self.display = self.builder.get_object("message1")
        self.message = self.builder.get_variable("turn")
        self.display['foreground'] = self.colour[self.turn]
        self.message.set(f"Player {self.turn} to play")
        return
    def checkEnd(self):
        #print("Starting play")
        self.win = check_victory(self.board,self.turn)
        if self.win != 0 or self.check_draw():
            self.EndGame()
            return True
        return False

    def pop(self,event):
        print("popping")
        pop_col = int(event[-1])
        print(pop_col,type(pop_col))
        if check_move(self.board,self.turn,pop_col,pop=1): #Check if valid move
            apply_move(self.board,self.turn,pop_col,pop=1) #Make the move
            self.display_board()
            self.nextPlayer()
            self.mainwindow.update()
        else:
            self.message = self.builder.get_variable("turn")
            self.message.set(f"Can't pop disc at selected column. Make another move")
        if self.checkEnd()==False and self.whoIsPlaying and self.turn == 2: #Comp move
                print("Computer move:")
                self.computer_move()
        return
    
    def player_move(self,row,col):
        print("Player {} to move".format(self.turn))
        pop = 0
        if check_move(self.board,self.turn,col,pop): #Check if valid move
            apply_move(self.board,self.turn,col,pop) #Make the move
            #self.drawCircle(row,col)
            self.display_board()
            self.nextPlayer()
            self.mainwindow.update()
        else:
            print("Invalid move")
            return 

    def computer_move(self):
        time.sleep(0.5)  
        moved = False      
        if self.level == 1:
            self.random_move()
        elif self.level ==2:
            board_future  = self.board.copy()
            for col in range(self.cols): #Check for possible winning moves by computer
                board_future  = self.board.copy() #Create a copy of board to try sample move without pop
                if check_move(board_future,self.turn,col,pop=False,com=1): #Check valid move
                    apply_move(board_future,self.turn,col,pop=False) #Try move
                    if check_victory(board_future,self.turn) == 2: #If computer wins
                        apply_move(self.board,self.turn,col,pop=False) #Do that move to actual board
                        moved = True
                        #self.drawCircle(row,col) 
                        break 
                
                board_future  = self.board.copy() #Create a copy of board to try sample move with pop
                if check_move(board_future,self.turn,col,pop=True,com=1): #Check valid move
                    apply_move(board_future,self.turn,col,pop=True) #Try move
                    if check_victory(board_future,self.turn) == 2: #If won
                        row,col = apply_move(self.board,self.turn,col,pop=True) #Do that move
                        self.drawCircle(row,col)
                        self.display_board() 
                        return 
            
            for col in range(self.cols): #Check for possible winning moves by opponent(1)
                board_future  = self.board.copy() #Look for adverse move
                if check_move(board_future,1,col,pop=False,com=1): #Check valid move
                    apply_move(board_future,1,col,pop=False) #Try move
                   
                    if check_victory(board_future,1) == 1 and moved == False: #If adverse wins
                        apply_move(self.board,self.turn,col,pop=False) #Do that move to block
                        moved = True
                        #self.drawCircle(row,col)
                        break

            if moved == False:
                self.random_move() #Else do a random move
        self.nextPlayer()
        self.display_board()  
        self.checkEnd() 
        return
    
    def random_move(self):

        col,pop = random.randint(0,6),random.randint(0,9)
        if pop>1:pop=0 #10% chance of popping the disc
        while(check_move(self.board,self.turn,col,pop,com=1)==False): #Make sure to generate a valid random move
            col,pop = random.randint(0,6),random.randint(0,9)
            if pop>1:pop=0 #10% chance of popping the disc
        print("Doing random move") 
        apply_move(self.board,self.turn,col,pop) #Make the move
        #self.drawCircle(row,col)
        
    def check_draw(self):
        for c in self.board[0]:
            if c ==0: #If there is an avaialble slot game has not ended
                return False
        print("Match drawn")
        return True
    
   
def menu():

    print("Lets play Connect4!")
    connect4 = Connect4()

   
if __name__ == "__main__":
    menu()

