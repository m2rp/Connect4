import random
import math
import numpy as np
from tkinter import *
import pathlib
import pygubu

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
    for i in range(4): 
        if check_index(board,row,col+i):
            if board[row][col+i] != who:
                win = False
                break
        else:
            win = False
            break
    if win: 
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
    
    return board

def check_victory(board, who_played):
    board = np_convert(board)
    R,C = board.shape
    p1 = False
    p2 = False
    for row in range(R-1,-1,-1):
        for col in range(C):
            if board[row][col]:
                if p1 == False: #Only check victory condition for player 1 if p1 victory not found yet
                    p1 = check_around(board,row,col,1)
                if p2 == False: #Only check victory condition for player 2 if p2 victory not found yet
                    p2 = check_around(board,row,col,2)
                if p1 and p2: #If both conditions found, other player wins (from rules)
                    if who_played == 1:
                        print("Player 2 has won") 
                        return 2 
                    else:
                        print("Player 1 has won")
                        return 1
    
    if p1: 
        print("Player 1 has won")
        return 1 
    if p2: 
        print("Player 2 has won")
        return 2
    return 0



    
   
 
class Connect4:
    def __init__(self):
        print("Initialising Connect4")
        self.rows = 7 #To be input from user
        self.cols = COLS 
        self.turn = 1 #Default to player 1 first
        self.colour = '#0000ff' #blue
        self.size_of_board = 600
        self.circle_size = self.size_of_board//min(self.rows,self.cols) - 10
        self.whoIsPlaying = None # 0 is human, 1 is computer
        self.builder = self.initBuilder("5")
        self.run()
         
        
    
    #GUI Functions --------------------------------
    def initBuilder(self,windowNumber):
        builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel"+windowNumber)
        builder.connect_callbacks(self)
        return builder

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
        self.level = level

    def playLevel(self):
        if self.level:
            print("Choosing level ",self.level)
            self.mainwindow.destroy()
            self.initBoard()
        else:
           #Display choose message
           pass 
    def initBoard(self):
        #Internal board (np array)
        self.board = np.zeros((self.rows,self.cols),dtype=int) #Create board
        self.display_board()
       #GUI board 
        self.builder = self.initBuilder("3") 
        self.canvas = self.builder.get_object("canvas2")
        
        for i in range(self.rows):
            self.canvas.create_line(0, (i + 1) * self.size_of_board / self.rows, self.size_of_board, (i + 1) * self.size_of_board / self.rows)
        for i in range(self.cols-1):
            self.canvas.create_line((i + 1) * self.size_of_board / self.cols, 0, (i + 1) * self.size_of_board / self.cols, self.size_of_board)
        self.play()

  
        
    def drawCircle(self,row,col): #Draw circle to represent player move
        y,x = row*self.size_of_board//self.rows + 5, col*self.size_of_board//self.cols + 5
        
        self.canvas.create_oval(x,y,x+self.circle_size,y+self.circle_size,outline = "black",fill = self.colour,width = 2)

    def nextPlayer(self): #CHange player turn and colours
        if self.turn == 1:
            self.turn = 2
            self.colour = '#ff0000' #player 2 is red
        else:
            self.turn = 1
            self.colour =  '#0000ff' #player 1 is blue
        self.display = self.builder.get_object("message1")
        self.message = self.builder.get_variable("turn")
        self.display['foreground'] = self.colour
        self.message.set(f"Player {self.turn} to play")

    def convert_grid_to_logical_position(self,grid_position):
        grid_position = np.array(grid_position)
        grid_position[1] = grid_position[1] // (self.size_of_board / self.rows)
        grid_position[0] = grid_position[0] // (self.size_of_board / self.cols)
        return np.array(grid_position, dtype=int)
    
    
    def run(self):
        self.mainwindow.mainloop()
    def boardClick(self, event=None):
        #Click positioning
        grid_position = [event.x, event.y]
        row,col = self.convert_grid_to_logical_position(grid_position)
        print(row,col)
        self.player_move(col,row)
        self.play()
        #self.drawCircle(row,col)
        #self.nextPlayer()

    def play(self):
        #print("Starting play")
        if check_victory(self.board,self.turn) == 0 and self.check_draw() == False:
            if self.whoIsPlaying and self.turn == 2: #Comp move
                print("Computer move:")
                self.turn = self.computer_move()
            else: #Human Move
                #self.turn = self.player_move()
                pass

        else:
            self.mainwindow.destroy()
            print("Thanks for playing Connect4!")
    
    def computer_move(self):
        # implement your function here
        if self.level ==1 :
            self.random_move()
        elif self.level ==2:
            board_future  = self.board.copy()
            for col in range(self.cols): #Check for possible winning moves by computer
                board_future  = self.board.copy() #Create a copy of board to try sample move without pop
                if check_move(board_future,self.turn,col,pop=False,com=1): #Check valid move
                    apply_move(board_future,self.turn,col,pop=False) #Try move
                    if check_victory(board_future,self.turn) == 2: #If computer wins
                        apply_move(self.board,self.turn,col,pop=False) #Do that move to actual board
                        self.display_board()  
                        return 1
                board_future  = self.board.copy() #Create a copy of board to try sample move with pop
                if check_move(board_future,self.turn,col,pop=True,com=1): #Check valid move
                    apply_move(board_future,self.turn,col,pop=True) #Try move
                    if check_victory(board_future,self.turn) == 2: #If won
                        apply_move(self.board,self.turn,col,pop=True) #Do that move
                        self.display_board() 
                        return 1
            for col in range(self.cols): #Check for possible winning moves by opponent(1)
                board_future  = self.board.copy() #Look for adverse move
                if check_move(board_future,1,col,pop=False,com=1): #Check valid move
                    apply_move(board_future,1,col,pop=False) #Try move
                    if check_victory(board_future,1) == 1: #If adverse wins
                        apply_move(self.board,self.turn,col,pop=False) #Do that move
                        self.display_board() 
                        return 1

            self.random_move() #Else do a random move
        self.display_board()     
        return 1

    
    def player_move(self,row,col):
        print("Player {} to move".format(self.turn))
        #pop = int(input("Do you want to pop the disc? (1 for yes, 0 for no)\n"))
        pop = 0
        #col = int(input("Enter column of play\n"))
       # print(pop,col)
        #row,col = self.boardClick()
        if check_move(self.board,self.turn,col,pop): #Check if valid move
            apply_move(self.board,self.turn,col,pop) #Make the move
            self.drawCircle(row,col)
            self.display_board()
            self.nextPlayer()
        else:
            print("Invalid move")
            return 

    def random_move(self):

        col,pop = random.randint(0,6),random.randint(0,9)
        if pop>1:pop=0 #10% chance of popping the disc
        while(check_move(self.board,self.turn,col,pop,com=1)==False): #Make sure to generate a valid random move
            col,pop = random.randint(0,6),random.randint(0,9)
            if pop>1:pop=0 #10% chance of popping the disc
            print("Doing random move") 
        apply_move(self.board,self.turn,col,pop) #Make the move

    def check_draw(self):
        for c in self.board[0]:
            if c ==0: #If there is an avaialble slot game has not ended
                return False
        print("Match drawn")
        return True
    

    def display_board(self):
        print(self.board)

def menu():

    print("Lets play Connect4!")
    connect4 = Connect4()

   
if __name__ == "__main__":
    menu()

