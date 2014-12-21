"""
Clone of 2048 game.
http://www.codeskulptor.org/#user34_p5PftdhDXDQkEe0_5.py
"""

import poc_2048_gui        
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    merged_line=[0]*len(line)
    loc=0
    merged=False
    for tmp in line:
        if tmp!=0:
            merged_line[loc]=tmp
            if not merged and loc>0 and merged_line[loc]==merged_line[loc-1]:
                merged_line[loc-1]=2*merged_line[loc-1]
                merged_line[loc]=0
                loc-=1
                merged=True
            else:
                merged=False
            loc+=1
    return merged_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.row = grid_height
        self.col = grid_width
        self.cells = self.reset()
        self.initial_up=[]
        self.initial_down=[]
        self.initial_left=[]
        self.initial_right=[]
        for tmp1 in range(self.col):
            self.initial_up.append([0, tmp1])
            self.initial_down.append([self.row-1, tmp1])
        for tmp2 in range(self.row):
            self.initial_left.append([tmp2, 0])
            self.initial_right.append([tmp2, self.col-1])

    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.cells = [ [ 0 for tmp1 in range(self.col)] for tmp2 in range(self.row)]
        return self.cells
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return self.row, self.col

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.row
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.col
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        self.tile_moved = False
        if direction==UP:
            for tmp1 in self.initial_up:    # iterate through columns
                tmp_list=[]
                for tmp2 in range(self.row):  #iterate through rows and get list merged
                    tmp_list.append(self.get_tile(tmp2,tmp1[1]))
                merged_list=merge(tmp_list)  #merge one column
                for tmp3 in range(self.row):      #Iterate over the column again and store the merged tile values back into the grid
                    self.set_tile(tmp3, tmp1[1], merged_list[tmp3])#iterate through rows and get merged number into grid                        
            self.tile_moved = True

        if direction==DOWN:
            #self.new_tile()
            for tmp1 in self.initial_down:    # iterate through columns
                tmp_list=[]
                for tmp2 in range(self.row):  #iterate through rows and get list merged
                    tmp_list.append(self.get_tile((tmp1[0]-tmp2),tmp1[1]))
                merged_list=merge(tmp_list)  #merge one column
                for tmp3 in range(self.row):      #Iterate over the column again and store the merged tile values back into the grid
                    self.set_tile((tmp1[0]-tmp3), tmp1[1], merged_list[tmp3])#iterate through rows and get merged number into grid
            self.tile_moved = True

        if direction==LEFT:
            #self.new_tile()
            for tmp1 in self.initial_left:    # iterate through rows
                tmp_list=[]
                for tmp2 in range(self.col):  #iterate through col and get list merged
                    tmp_list.append(self.get_tile(tmp1[0], tmp2))
                merged_list=merge(tmp_list)  #merge one row
                for tmp3 in range(self.col):      #Iterate over the row again and store the merged tile values back into the grid
                    self.set_tile(tmp1[0], tmp3, merged_list[tmp3])#iterate through col and get merged number into grid  
            self.tile_moved = True
            
        if direction==RIGHT:
            #self.new_tile()
            for tmp1 in self.initial_right:    # iterate through rows
                tmp_list=[]
                for tmp2 in range(self.col):  #iterate through col and get list merged
                    tmp_list.append(self.get_tile(tmp1[0], tmp1[1]-tmp2))
                merged_list=merge(tmp_list)  #merge one row
                for tmp3 in range(self.col):      #Iterate over the row again and store the merged tile values back into the grid
                    self.set_tile(tmp1[0], tmp1[1]-tmp3, merged_list[tmp3])#iterate through col and get merged number into grid
            self.tile_moved = True
            
        if self.tile_moved:
            self.new_tile()
            
        return self.cells

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        
        number_gen=[4, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        tmp_row=random.randrange(self.row)
        tmp_col=random.randrange(self.col)
        if self.get_tile(tmp_row, tmp_col)==0:
            self.set_tile(tmp_row, tmp_col, random.choice(number_gen))
        return self.cells

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self.cells[row][col] = value
        

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        return self.cells[row][col]
 
    
poc_2048_gui.run_gui(TwentyFortyEight(5, 4))