"""
Student portion of Zombie Apocalypse mini-project
http://www.codeskulptor.org/#user35_GFHcM3Lio102qXd_67.py
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._human_list = []
        self._zombie_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)     
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zom in self._zombie_list:
            yield zom
        #return []

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)     
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for hum in self._human_list:
            yield hum
        #return []
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        grid_height = self.get_grid_height()
        grid_width = self.get_grid_width()
        #Create a 2D list distance_field of the same size as the grid and initialize each of its entries to be the product of the height times the width of the grid
        distance_field = [[grid_height*grid_width \
                        for dummy_col in range(grid_width)] \
                        for dummy_row in range(grid_height)]
        #obstacle grid, initialize its cells to be empty
        visited = poc_grid.Grid(grid_height, grid_width)
        boundary = poc_queue.Queue()        
        if entity_type == ZOMBIE:
            for zom in self.zombies():
                boundary.enqueue(zom)
        elif entity_type == HUMAN:
            for hum in self.humans():
                boundary.enqueue(hum)
        for grid in boundary:
            visited.set_full(grid[0], grid[1])  # initialize visited to be FULL 
            distance_field[grid[0]][grid[1]] = 0 # initialize distance_field to be zero
        while len(boundary) > 0:
        #while boundary.__len__()>0:
            cell = boundary.dequeue()
            neighbors = visited.four_neighbors(cell[0], cell[1])
            for neighbor in neighbors:
                if (visited.is_empty(neighbor[0], neighbor[1]) )and (self.is_empty(neighbor[0], neighbor[1])):
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)
                    distance_field[neighbor[0]][neighbor[1]] = min(distance_field[neighbor[0]][neighbor[1]], distance_field[cell[0]][cell[1]]+1)
        return distance_field
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        print zombie_distance
        for hum in self._human_list:
            neighbors = self.eight_neighbors(hum[0], hum[1])
            hum_val = zombie_distance[hum[0]][hum[1]]
            hum_max = hum_val
            max_loc = ()
            for cell in neighbors:
                if zombie_distance[cell[0]][cell[1]]>hum_max:
                    hum_max = zombie_distance[cell[0]][cell[1]]
                    max_loc = cell                    
            if (max_loc not in self._human_list) and (max_loc != () ) and (self.is_empty(max_loc[0], max_loc[1])):
                self._human_list[self._human_list.index(hum)] = max_loc
        return self._human_list

    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for zom in self._zombie_list:
            neighbors = self.four_neighbors(zom[0], zom[1])
            zom_val = human_distance[zom[0]][zom[1]]
            zom_min = zom_val
            min_loc = ()
            for cell in neighbors:
                if human_distance[cell[0]][cell[1]]<zom_min:
                    zom_min = human_distance[cell[0]][cell[1]]
                    min_loc = cell
            if (min_loc not in self._zombie_list) and (min_loc != () ) and (self.is_empty(min_loc[0], min_loc[1])):
                self._zombie_list[self._zombie_list.index(zom)] = min_loc
        return self._zombie_list
                
# start up gui for simulation
poc_zombie_gui.run_gui(Zombie(20, 30, [(4, 15), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10)], [(12, 12), (7, 12)], []))
