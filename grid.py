import time

import pygame


class Grid:
    def __init__(self):
        self.grid = []
        
    def __str__(self):
        return "\n" + "\n".join([str(x) for x in self.grid]) + "\n"

    def get_unsolved_from_txt(self):
        with open('grid.txt') as file:
            for line in file.readlines():
                row = []
                for number in line.strip("\n"):
                    row.append(int(number))
                self.grid.append(row)

    ## Checks if a grid is valid, based on a number entered into a specific cell
    #
    # @param row, the row in the grid
    # @param col, the column of the grid
    # @param number, the number that has most recently been changed
    #
    # @return boolean, if the grid is valid return True
    def check_if_valid(self, row, col, number):
        # Checks if all numbers in row occurs only once
        for i in range(len(self.grid[row])):
            if self.grid[row][i] == number and col != i:
                return False

        # Checks if all numbers in column occurs only once
        for i in range(len(self.grid)):
            if self.grid[i][col] == number and row != i:
                return False

        # Defines the 3x3 grid that needs to be checked
        square = [(row // 3) * 3, (col//3) * 3]
        
        # Checks if all numbers in the 3x3 square occurs only once
        for i in range(square[0] , square[0] + 3):
            for j in range(square[1], square[1] + 3):
                if number == self.grid[i][j] and i != row and j != col:
                    return False
        return True

    ## Gets the next empty cell in the grid
    #
    # @return coordinates of empty cell if found, None if no empty cells
    def get_next_empty_cell(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == 0:
                    return (row, col)
        return None

    def solve(self, drawer, display):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # If an empty cell can be found contiue filling in grid, else return True
        if self.get_next_empty_cell() is not None:
            # Get the next empty cell
            empty_row, empty_col = self.get_next_empty_cell()
            for i in range(1, 10):
                # If the value of i is a valid option for the empty cell, enter it in
                if self.check_if_valid( empty_row, empty_col, i):
                    self.grid[empty_row][empty_col] = i
                    # If the grid can be solved from this point continue solving, else reset the cell and try next number
                    # drawer(display, self.grid)
                    drawer(display, empty_row, empty_col, i, text_colour = (0, 255, 0))
                    time.sleep(0.1)
                    if self.solve(drawer, display):
                        return True
                    drawer(display, empty_row, empty_col, i, text_colour = (255, 0, 0))
                    time.sleep(0.1)
                    
                    self.grid[empty_row][empty_col] = 0
                    # drawer(display, self.grid)
                    drawer(display, empty_row, empty_col, 0, text_colour = (255, 0, 0))

            return False       
        else:
            return True


    ## Checks if a grid is valid as a whole
    #
    # @param grid, nestesd lists that represent a 9x9 grid of intergers
    #
    # @return boolean, if the grid is valid return True
    def check(self):
        for row in self.grid:
            for i in range(1, 10):
                if row.count(i) != 1:
                    return False

        for col in range(9):
            lst = [row[col] for row in self.grid]
            for i in range(1, 10):
                if lst.count(i) != 1:
                    return False
        
        for i in range(3):
            for j in range(3):
                lst = [row[j* 3:(j*3) + 3] for row in self.grid[i * 3:(i*3) + 3]] 
                flat_list = []
                for k in lst:
                    for number in k:
                        flat_list.append(number)
                
                for check_number in range(1, 10):
                    if flat_list.count(check_number) != 1:
                        return False
        return True
