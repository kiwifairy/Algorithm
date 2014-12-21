"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
http://www.codeskulptor.org/#user37_SFNzf37PYJ_187.py
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        condition1 = False
        condition2 = False
        condition3 = False
        false_times = 0
        assert target_row < self._height , str(target_row) + "out of the height"
        assert target_col < self._width , str(target_col) + "out of the width"   
        if self.get_number(target_row,target_col)==0:   #Tile zero is positioned at (i,j).
            condition1 = True
        if target_row + 1 == self._height:
            condition2 = True
        else:
            for col in range(self._width):
                for row in range(target_row + 1, self._height ):
                    if self.get_number(row,col)!=col + self._width * row :       #All tiles in rows i+1 or below are positioned at their solved location.
                        false_times += 1
        if (target_col + 1) == (self._width ):
            condition3 = True 
        else:
            for col2 in range(target_col + 1, self._width ):
                if self.get_number(target_row,col2)!=col2 + self._width * target_row :  #All tiles in row i to the right of position (i,j) are positioned at their solved location.
                    false_times += 1                  
        if false_times == 0:
            condition2 = True
            condition3 = True
        return condition3 and condition2 and condition1

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col),\
            "Initial invariant check failed\n" + str(self)
        tile_pos = self.current_position(target_row, target_col)
        move_string = ""
        # If it's in the same row, scoot it left
        if tile_pos[0] == target_row:
            move_string += "l" * (abs(target_col - tile_pos[1]))
            move_string += "urrdl" * (abs(target_col - tile_pos[1] )- 1)
        # If the target is only one row above the current spot and directly
        # above, just do a uld cycle.
        
        elif target_row - tile_pos[0] == 1:
            move_string += "u"
            if tile_pos[1] == target_col:
                move_string += "ld"
            # otherwise if it's to the right, we'll have to do a flipped
            # horizontal move left
            elif tile_pos[1] > target_col:
                # move to the immediate left of the target.
                for dummy_square in range(abs(tile_pos[1] - target_col )):
                    move_string += "r"
                # move the tile left until it is over the target.
                for dummy_square in range(abs(tile_pos[1] - target_col)):
                    move_string += "ulldr"
                # move the tile into position, then 
                move_string += "ldruld"
            elif tile_pos[1] < target_col:##?
                # move to the immediate right of the target.
                for dummy_square in range(abs(target_col - tile_pos[1])):
                    move_string += "l"
                # move the tile right until it is over the target.
                for dummy_square in range(abs(tile_pos[1] - target_col)-1):
                    move_string += "urrdl"
                # move the tile into position, then 
                move_string += "druld"
        
        elif target_row - tile_pos[0] >= 1:
            # If it's directly above, just move it down
            if tile_pos[1] == target_col:
                for dummy_square in range(abs(tile_pos[0] - target_row )- 1):
                    move_string += "u"
                for dummy_square in range(abs(tile_pos[0] - target_row )- 1):
                    move_string += "ulddr"
                move_string += "uld"
            # if it's to the right, move it left (with a downward facing loop),
            # then down
            elif tile_pos[1] > target_col:
                for dummy_square in range(abs(target_row - tile_pos[0])):
                    move_string += "u"
                # move to the immediate left of the target.
                for dummy_square in range(abs(tile_pos[1] - target_col )- 1):
                    move_string += "r"
                # move the tile left until it is over the target.
                for dummy_square in range(abs(tile_pos[1] - target_col) - 1):
                    move_string += "rdllu"
                move_string += "rdl"
                for dummy_square in range(abs(tile_pos[0] - target_row )- 1):
                    move_string += "ulddr"
                move_string += "uld"
            elif tile_pos[1] < target_col:
                for dummy_square in range(abs(target_row - tile_pos[0])):
                    move_string += "u"
                # move to the immediate right of the target.
                for dummy_square in range(abs(target_col - tile_pos[1]) - 1):
                    move_string += "l"
                # move the tile right until it is over the target.
                for dummy_square in range(abs(target_col - tile_pos[1] )- 1):
                    move_string += "ldrru"
                move_string += "ldr"
                for dummy_square in range(abs(target_row - tile_pos[0]) - 1):
                    move_string += "ulddr"
                move_string += "uld"
        #print move_string
        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row, target_col - 1),\
            "Final invariant check failed\n" + str(self)
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        tile_pos = self.current_position(target_row, 0)
        move_string = ""
        assert self.lower_row_invariant(target_row, 0),\
            "Initial invariant check failed\n" + str(self)
        # See if the target is directly above you
        if tile_pos[1] == 0:
            # If it's directly above you
            if tile_pos[0] == target_row - 1:
                move_string += "u"
            else:
                # Move underneath it
                move_string += "u" * (abs(target_row - tile_pos[0] )- 1)
                # Move it to column 1
                move_string += "ruldr"
                # Move it down to row i - 1
                move_string += "ulddr" * (abs(target_row - tile_pos[0]) - 2)
                # And move to the left
                move_string += "uld"
                # Then solve
                move_string += "ruldrdlurdluurddlu"
        else:
            # If it's in the row directly above, do upwards facing moves
            if tile_pos[0] == target_row - 1:
                move_string += "u"
                move_string += "r" * (tile_pos[1] - 1)
                move_string += "rulld" * (tile_pos[1] - 2)
                move_string += "ruld"* (tile_pos[1] - 1)
                # Then solve
                move_string += "ruldrdlurdluurddlu"
            # Otherwize use downward
            else:
                move_string += "u" * (abs(target_row - tile_pos[0]))
                move_string += "r" * (tile_pos[1] - 1)
                move_string += "rdllu" * (tile_pos[1] - 2)
                move_string += "rdl"
                move_string += "ulddr" * (abs(target_row - tile_pos[0]) - 2)
                move_string += "uld"
                # Then solve
                move_string += "ruldrdlurdluurddlu"
        # Finish by moving the 0 all the way to the right
        move_string += "r" * (self.get_width() - 1)
        #print tile_pos, move_string
        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1),\
            "Final invariant check failed\n" + str(self)
        return move_string
    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        assert target_col < self._width , str(target_col) + "out of the width"   
        
        if self.get_number(0,target_col)!=0:   #Tile zero is positioned at (0,j).
            return False
        for col in range(self._width):   #row down n-2
            for row in range( 2, self._height ):
                if self.get_number(row,col)!=col + self._width * row :     
                    return False
        for col1 in range(target_col + 1, self._width ):  # row 0,1 right
            for row in range(2):
                if self.get_number(row,col1)!=col1+ self._width * row :  
                    return False
        if self.get_number(1,target_col)!=target_col+ self._width :  # tile (1,j)
            return False      
        return True


    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        assert target_col < self._width , str(target_col) + "out of the width"   
        if not self.lower_row_invariant(1, target_col):
            return False
        else:
            for col in range(target_col + 1, self._width ):
                for row in range(1):
                    if self.get_number(row,col)!=col+ self._width * row :  #All tiles in row i to the right of position (i,j) are positioned at their solved location.
                        return False   
        return True


    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col),\
            "Initial invariant check failed\n" + str(self)
        tile_pos = self.current_position(0, target_col)
        move_string = ""

        # 1. target tile is at (0, target_col -1). The move required is "ld"
        if tile_pos ==  (0, target_col -1):
            move_string += "ld"
        # 2. target tile is already present at (1, target_col - 1). Then do "lld" + the move from #10 of homework.
        elif tile_pos ==  (1, target_col -1):
            move_string += "lld" + "urdlurrdluldrruld"
        # 3. The target tile is in row 0.
        # move to the target tile. Pull it down using "druld" 
        #then shift it to the right  till it reaches (1, target_col - 1). 
        # Then perform the move from #10.   
        elif tile_pos[0]==0 :
            move_string += "l" * (abs(target_col - tile_pos[1])) + "druld" 
            move_string += "urrdl" * (abs(target_col - tile_pos[1]) - 2) + "urdlurrdluldrruld"  
        # 4) If the target tile is in row 1 
        #Go to it and move it to the right using "urrdl" till it reaches (1, target_col - 1)
        #Then perform the move from #10.
        elif tile_pos[0]==1 :
            move_string += "l" * (abs(target_col - tile_pos[1])) + "druldruld"+ "urrdl" * (abs(target_col - tile_pos[1] )- 2) + "urdlurrdluldrruld"  
        self.update_puzzle(move_string)
        assert self.row1_invariant(target_col-1),\
            "Final invariant check failed\n" + str(self)
        return move_string
    
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col),\
            "Initial invariant check failed\n" + str(self)
        tile_pos = self.current_position(1, target_col)
        move_string = ""
        # If it's in row1, scoot it left
        if tile_pos[0] == 1:
            move_string += "l" * (abs(target_col - tile_pos[1]))
            move_string += "urrdl" * (abs(target_col - tile_pos[1]) - 1)   
            move_string += "ur" 
        # in row0
        elif tile_pos[0] == 0:
            move_string += "u"
            if tile_pos[1] < target_col:
                move_string += "l" *(abs(target_col - tile_pos[1] ))
                move_string += "drrul" * (abs(target_col -tile_pos[1]) -1)
                move_string += "dru" 

        self.update_puzzle(move_string)
        assert self.row0_invariant(target_col),\
            "Final invariant check failed\n" + str(self)
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1),\
            "Initial invariant check failed\n" + str(self)    
        move_string = ""
        times = 0
        while True:
            clone = self.clone()
            move_string = "uldr" * times + "ul"
            clone.update_puzzle(move_string)
            if  clone.row0_invariant(0):
                break
            times += 1
        self.update_puzzle(move_string)
        assert self.row0_invariant(0),\
            "Final invariant check failed\n" + str(self)        
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        clone = self.clone()
        target_row = self.get_height()-1
        target_col = self.get_width()-1
        target_pos = self.current_position( 0, 0 )
        # initial target solve
        if not self.lower_row_invariant(target_row, target_col ):
            move_string += "r" * (target_col - target_pos[1]) + "d" * (target_row - target_pos[0])
            clone.update_puzzle(move_string)
            #print str(clone)+"1"+move_string
        # solve lower row 
        while target_row >1:
            if target_col > 0  :
                #print "begin"+str(target_row)+" , "+str(target_col)
                move_string += clone.solve_interior_tile(target_row, target_col)
                #print " "
                #print "2.\n"+str(clone)+str(target_row)+" , "+str(target_col)+" "+move_string
                target_col -= 1
            if target_col == 0 :
                #print " "
                #print str(target_row)+" , "+str(target_col)
                move_string += clone.solve_col0_tile(target_row)
                target_row -= 1
                target_col = self.get_width()-1
                #print "2.1\n"+str(clone)+str(target_row)+" , "+str(target_col)+" "+move_string
        # solve row 1
        while not (target_row == 1 and target_col == 1):
            if target_row ==1 and target_col > 1:
                move_string += clone.solve_row1_tile(target_col)
                target_row = 0
                #print " "
                #print str(clone)+"(3)"+str(target_row)+" , "+str(target_col)+move_string

        # solve row 0    
            if target_row == 0 and target_col > 1:
                move_string += clone.solve_row0_tile(target_col)
                target_row = 1 
                target_col -= 1
                #print " "
                #print str(clone)+"(4)"+str(target_row)+" , "+str(target_col)+move_string

        # solve 2x2
        if target_row == 1 and target_col == 1:
            move_string += clone.solve_2x2()
            #print str(clone)+"5"+move_string
        self.update_puzzle(move_string)
        assert self.row0_invariant(0),\
            "Final invariant check failed\n" + str(self)               
        return move_string

# Start interactive simulation
#obj = Puzzle(4, 4, [[0, 4, 8, 2], [15, 1, 14, 3], [5, 13, 10, 7], [12, 9, 6, 11]])  
#obj = Puzzle(4, 4, [[4, 8, 2, 3], [5, 11, 10, 7], [1, 9, 6, 0], [12, 13, 14, 15]])  
#obj = Puzzle(4, 4, [[4, 8, 2, 3], [5, 6, 9, 7], [1, 0, 10, 11], [12, 13, 14, 15]])  


#poc_fifteen_gui.FifteenGUI(obj)

#print obj.solve_interior_tile(2,1)