#!/usr/bin/python3
import numpy as np
import pathlib
import pygubu
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "gui_1.ui"


class Gui1App:
    def __init__(self, master=None):
        self.rows = 7 
        self.cols = 7
        self.turn = 1
        self.colour = '#0000ff' #blue
        self.size_of_board = 600
        self.circle_size = self.size_of_board//min(self.rows,self.cols) - 10
        self.builder = self.initBuilder("5")
        #self.initBoard()

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

    def run(self):
        self.mainwindow.mainloop()

    def human_button_click(self):
        print("Human button clicked")
        self.mainwindow.destroy()
        self.initBoard()
        
    def comp_button_click(self):
        print("Computer button clicked")
        self.mainwindow.destroy()
        self.builder = self.initBuilder("2") 
   
    def initBoard(self):
        self.builder = self.initBuilder("3") 
        self.canvas = self.builder.get_object("canvas2")
        
        for i in range(self.rows):
            self.canvas.create_line(0, (i + 1) * self.size_of_board / self.rows, self.size_of_board, (i + 1) * self.size_of_board / self.rows)
        for i in range(self.cols-1):
            self.canvas.create_line((i + 1) * self.size_of_board / self.cols, 0, (i + 1) * self.size_of_board / self.cols, self.size_of_board)

    def boardClick(self, event=None):
        #Click positioning
        grid_position = [event.x, event.y]
        row,col = self.convert_grid_to_logical_position(grid_position)
        print(row,col)
        self.drawCircle(row,col)
        self.nextPlayer()
        
    def drawCircle(self,row,col): #Draw circle to represent player move
        x,y = row*self.size_of_board//self.rows + 5, col*self.size_of_board//self.cols + 5
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
        

if __name__ == "__main__":
    app = Gui1App()
    app.run()
