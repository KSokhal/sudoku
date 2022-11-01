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

    def check_if_valid(self, row, col, number):
        """
        Checks it the grid is valid based of a number entered into a specific cell.
        
        Paramters:
            row, the row in the grid
            col, the column of the grid
            number, the number that has most recently been changed
        """
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

    def get_next_empty_cell(self):
        """
        Gets the position of the next empty cell.
        Returns the cell postition is empty one exists, or None if it does not
        """
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == 0:
                    return (row, col)
        return None

    def solve(self, drawer, display):
        """
        Solves the grid.

        Parameters:
            drawer: helper function used to draw cells on to the pygame display
            display: pygame diaply
        """
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

    def check(self):
        """Checks it the grid as a whole is valid."""
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
