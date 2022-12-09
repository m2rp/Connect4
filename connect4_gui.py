# Author: Prem Manoharan
# Created: Nov 2022
# Email: prem6556@gmail.com

import random
import math
import numpy as np
from tkinter import *

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
def check_draw(board):
    for c in board[0]:
        if c ==0: #If there is an avaialble slot game has not ended
            return False
    print("Match drawn")
    return True
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
            if com==0: print("Can't place disc here")
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
def random_move(board,turn):

    col,pop = random.randint(0,6),random.randint(0,4)
    while(check_move(board,turn,col,pop,com=1)==False): #Make sure to generate a valid random move
        col,pop = random.randint(0,6),random.randint(0,9)
        if pop>1:pop=0 #10% chance of popping the disc
        print("Doing random move") 
    apply_move(board,turn,col,pop) #Make the move
    
def computer_move(board, turn, level):
    # implement your function here
    board = np_convert(board) #For test case purposes
    R,C = board.shape
    if level ==1 :
        random_move(board,turn)
    elif level ==2:
        board_future  = board.copy()
        for col in range(C):
            board_future  = board.copy() #Create a copy of board to try sample move WITHOUT pop
            if check_move(board_future,turn,col,pop=False,com=1): #Check valid move
                apply_move(board_future,turn,col,pop=False) #Try move
                if check_victory(board_future,turn) == 2: #If wthat move wins
                    apply_move(board,turn,col,pop=False) #Apply move to actual board
                    display_board(board)  
                    return 1
            board_future  = board.copy() #Create a copy of board to try sample move WITH pop. aka pop every column
            if check_move(board_future,turn,col,pop=True,com=1): #Check valid move
                apply_move(board_future,turn,col,pop=True) #Try move
                if check_victory(board_future,turn) == 2: #If won
                    apply_move(board,turn,col,pop=True) #Do that move
                    display_board(board) 
                    return 1
        for col in range(C):
            board_future  = board.copy() #Look for adverse move
            if check_move(board_future,1,col,pop=False,com=1): #Check valid move
                apply_move(board_future,1,col,pop=False) #Try move
                if check_victory(board_future,1) == 1: #If adverse wins
                    apply_move(board,turn,col,pop=False) #Do that move
                    display_board(board) 
                    return 1

        random_move(board,turn) #Else do a random move
    display_board(board)     
    return 1
    
def display_board(board):
    print(board)  #index [0][0] is top left of board - numpy
    # rows = int(len(board)/7)
    # for row in range(rows-1,-1,-1):
    #     for col in range(row*7,(row+1)*7):
    #         print(board[col],end=' ')
    #     print('\n')
def player_move(board,turn):
    print("Player {} to move".format(turn))
    pop = int(input("Do you want to pop the disc? (1 for yes, 0 for no)\n"))
    col = int(input("Enter column of play\n"))
    print(pop,col)
    
    if check_move(board,turn,col,pop): #Check if valid move
        apply_move(board,turn,col,pop) #Make the move
        turn = 2 if turn == 1 else 1 #Change player to play
        display_board(board) 
    return turn  
def initialize_board(canvas,ROWS,COLS):
    
    for i in range(COLS-1):
        canvas.create_line((i + 1) * size_of_board / COLS, 0, (i + 1) * size_of_board / COLS, size_of_board)

    for i in range(ROWS-1):
        canvas.create_line(0, (i + 1) * size_of_board / ROWS, size_of_board, (i + 1) * size_of_board / ROWS)
def convert_grid_to_logical_position(grid_position):
        global ROWS,COLS
        grid_position = np.array(grid_position)
        grid_position[1] = grid_position[1] // (size_of_board / ROWS)
        grid_position[0] = grid_position[0] // (size_of_board / COLS)
        return np.array(grid_position, dtype=int)

def click(event):
    
    grid_position = [event.x, event.y]
    logical_position = convert_grid_to_logical_position(grid_position)
    print(logical_position)


def menu():
    global ROWS, COLS
    COLS = 7
    print("Lets play Connect4!")
    ROWS = int(input("How many rows would you like in the board?\n"))
   
    board = np.zeros((ROWS,COLS),dtype=int) #Create board
    display_board(board)
    comp = int(input("Enter 0 for human, 1 for computer\n"))
    if comp:
        print("Computer playing as player 2")
        level = int(input("What difficulty level would you like? (1 or 2)\n"))
    #GUI
    window = Tk()
    window.title('Connect4')
    canvas = Canvas(window, width=size_of_board, height=size_of_board)
    canvas.pack()
    initialize_board(canvas,ROWS,COLS)
    window.bind('<Button-1>', click)

    turn = 1 #Default to player 1 first
    while check_victory(board,turn) == 0 and check_draw(board) == False:
        if comp and turn == 2: #Comp move
            print("Computer move:")
            turn = computer_move(board,turn,level)
        else: #Human Move
            turn = player_move(board,turn)


    print("Thanks for playing Connect4!")
global ROWS, COLS
size_of_board = 600
if __name__ == "__main__":
    menu()

