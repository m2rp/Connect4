import random
import math
import numpy as np

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
    def __init__(self,rows,cols,player):
        self.rows = rows
        self.cols = cols
        self.player = player # 0 is human, 1 is computer
        self.board = np.zeros((rows,cols),dtype=int) #Create board
        if self.player:
            print("Computer playing as player 2")
            self.level = int(input("What difficulty level would you like? (1 or 2)\n"))
        self.display_board()
        self.turn = 1 #Default to player 1 first
        

    def play(self):
        while check_victory(self.board,self.turn) == 0 and self.check_draw() == False:
            if self.player and self.turn == 2: #Comp move
                print("Computer move:")
                self.turn = self.computer_move()
            else: #Human Move
                self.turn = self.player_move()


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

    
    def player_move(self):
        print("Player {} to move".format(self.turn))
        pop = int(input("Do you want to pop the disc? (1 for yes, 0 for no)\n"))
        col = int(input("Enter column of play\n"))
        print(pop,col)
        
        if check_move(self.board,self.turn,col,pop): #Check if valid move
            apply_move(self.board,self.turn,col,pop) #Make the move
            self.display_board()
            return 2 if self.turn == 1 else 1 #Change player to play
        else:
            return self.turn

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

    COLS = 7
    print("Lets play Connect4!")
    ROWS = int(input("How many rows would you like in the board?\n"))
    player = int(input("Enter 0 for human, 1 for computer\n"))
    connect4 = Connect4(ROWS,COLS,player)
    connect4.play()

   
if __name__ == "__main__":
    menu()

