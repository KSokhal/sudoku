import copy
import time
from math import floor

import pygame

# Set display dimensions
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

# Sets colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Sets constants for display of grid
GRID_START_POS = (50, 50)
CELL_SIZE = 50

def main():
    # Generates grids from text file
    grid = get_unsolved()
    original_grid = copy.deepcopy(grid)

    # Initialises varibles for pygame
    pygame.init()
    global font
    font = pygame.font.SysFont("ubuntumono", 40)
    game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("Sudoku")
    game_display.fill(WHITE)
    clock = pygame.time.Clock()
    draw_grid(game_display, grid)

    end = False
    allow_edit = False
    
    while not end:
        # Quit case
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True

        if button(game_display, (600, 100), (100, 50), (82, 82, 82), (42, 42, 42), "Solve"):
            draw_grid(game_display, original_grid)
            fill_in_grid(game_display, original_grid)

        if check(grid) and get_next_empty_cell(grid) is None:
            print("Complete")
            text = font.render("Level Complete!", True, (0, 255, 0))
            game_display.blit(text, (50, 550))
            pygame.display.update()
            event = pygame.event.wait()
            if event.type == KEYDOWN:
                end = True

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rounding_factor = 50
        cell_pos = (floor(mouse_pos[0] / rounding_factor) * rounding_factor, floor(mouse_pos[1] / rounding_factor) * rounding_factor)
        if cell_pos[0] >= 50 and cell_pos[0] < 500 and cell_pos[1] >= 50 and cell_pos[1] < 500 and click[0] == 1:
            x = int((cell_pos[0] - GRID_START_POS[0]) / CELL_SIZE )
            y = int((cell_pos[1] - GRID_START_POS[1]) / CELL_SIZE )
            number = None
            if original_grid[y][x] == 0:
                allow_edit = True
            else:
                allow_edit = False


        if allow_edit:

            keys = pygame.key.get_pressed()

            if keys[pygame.K_1] or keys[pygame.K_KP1]:
                number = "1"
            elif keys[pygame.K_2] or keys[pygame.K_KP2]:
                number = "2"
            elif keys[pygame.K_3] or keys[pygame.K_KP3]:
                number = "3"
            elif keys[pygame.K_4] or keys[pygame.K_KP4]:
                number = "4"
            elif keys[pygame.K_5] or keys[pygame.K_KP5]:
                number = "5"
            elif keys[pygame.K_6] or keys[pygame.K_KP6]:
                number = "6"
            elif keys[pygame.K_7] or keys[pygame.K_KP7]:
                number = "7"
            elif keys[pygame.K_8] or keys[pygame.K_KP8]:
                number = "8"
            elif keys[pygame.K_9] or keys[pygame.K_KP9]:
                number = "9"
            
            if number is not None:
                grid[y][x] = int(number)
                if check_if_valid(grid, y, x, int(number)):
                    text_colour = BLACK
                else:
                    text_colour = (255, 0, 0)

                pygame.draw.rect(game_display, WHITE, (GRID_START_POS[0] + 10 + (x * CELL_SIZE), GRID_START_POS[1] + 10 + (y * CELL_SIZE), CELL_SIZE - 20, CELL_SIZE - 20), 0)
                text = font.render(number, True, text_colour)
                text_size = font.size(number)
                text_start_pos = (round((CELL_SIZE - text_size[0]) / 2), round((CELL_SIZE - text_size[1]) / 2))
                game_display.blit(text, (GRID_START_POS[0] + text_start_pos[0] + (x * CELL_SIZE), GRID_START_POS[1] + text_start_pos[1] + (y * CELL_SIZE)))
                pygame.display.update()

        clock.tick(60)

    pygame.quit()
    quit()


def draw_grid(display, grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            pygame.draw.rect(display, BLACK, (GRID_START_POS[0] + (row * CELL_SIZE), GRID_START_POS[1] + (col * CELL_SIZE), CELL_SIZE, CELL_SIZE), 1)
            cell_value = str(grid[col][row])
            if cell_value == "0":
                pygame.draw.rect(display, WHITE, (GRID_START_POS[0] + 10 + (row * CELL_SIZE), GRID_START_POS[1] + 10 + (col * CELL_SIZE), CELL_SIZE - 20, CELL_SIZE - 20), 0)
            else:
                text = font.render(cell_value, True, BLACK)
                text_size = font.size(cell_value)
                text_start_pos = (round((CELL_SIZE - text_size[0]) / 2), round((CELL_SIZE - text_size[1]) / 2))
                display.blit(text, (GRID_START_POS[0] + text_start_pos[0] + (row * CELL_SIZE), GRID_START_POS[1] + text_start_pos[1] + (col * CELL_SIZE)))
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(display, BLACK, (GRID_START_POS[0] + (i * CELL_SIZE * 3), GRID_START_POS[1] + (j * CELL_SIZE * 3), CELL_SIZE * 3, CELL_SIZE * 3), 5)

    pygame.display.update()


def button(display, pos, size, active_colour, inactive_colour, display_text):

    pygame.draw.rect(display, inactive_colour, (pos[0], pos[1], size[0], size[1]), 0)
    text = font.render(display_text, True, BLACK)
    text_size = font.size(display_text)
    text_start_pos = (round((size[0] - text_size[0]) / 2), round((size[1] - text_size[1]) / 2))
    display.blit(text, (pos[0] + text_start_pos[0], pos[1] + text_start_pos[1]))
    pygame.display.update()
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    mouse_on_button = mouse[0] > pos[0] and mouse[0] < (pos[0] + size[0]) and mouse[1] > pos[1] and mouse[1] < (pos[1] + size[1])
    if mouse_on_button:
        pygame.draw.rect(display, active_colour, (pos[0], pos[1], size[0], size[1]), 0)
        display.blit(text, (pos[0] + text_start_pos[0], pos[1] + text_start_pos[1]))
        pygame.display.update()
        if click[0] == 1:
            return True
        else:
            return False


def check(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            for number in range(1, 10):
                check_if_valid(grid, row, col, number)





## Checks if a grid is valid
#
# @param grid, nestesd lists that represent a 9x9 grid of intergers
# @param row, the row in the grid
# @param col, the column of the grid
# @param number, the number that has most recently been changed
#
# @return boolean, if the grid is valid return True

def check_if_valid(grid, row, col, number):
    # Checks if all numbers in row occurs only once
    for i in range(len(grid[row])):
        if grid[row][i] == number and col != i:
            return False

    # Checks if all numbers in column occurs only once
    for i in range(len(grid)):
        if grid[i][col] == number and row != i:
            return False

    # Defines the 3x3 grid that needs to be checked
    square = [(row // 3) * 3, (col//3) * 3]
    
    # Checks if all numbers in the 3x3 square occurs only once
    for i in range(square[0] , square[0] + 3):
        for j in range(square[1], square[1] + 3):
            if number == grid[i][j] and i != row and j != col:
                return False
    return True


## Gets the next empty cell in the grid
#
# @param grid, nestesd lists that represent a 9x9 grid of intergers
#
# @return coordinates of empty cell if found, None if no empty cells

def get_next_empty_cell(grid):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                return (row, col)
    return None

# Attempts to solve the grid
#
# @param grid, nestesd lists that represent a 9x9 grid of intergers
#
# @return boolean, if the grid was solved True

def fill_in_grid(display, grid):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                quit()


    # If an empty cell can be found contiue filling in grid, else return True
    if get_next_empty_cell(grid) is not None:
        # Get the next empty cell
        empty_row, empty_col = get_next_empty_cell(grid)
        for i in range(1, 10):
            # If the value of i is a valid option for the empty cell, enter it in
            if check_if_valid(grid, empty_row, empty_col, i):
                grid[empty_row][empty_col] = i
                # If the grid can be solved from this point continue solving, else reset the cell and try next number
                draw_grid(display, grid)
                time.sleep(0.1)
                if fill_in_grid(display, grid):
                    return True
                grid[empty_row][empty_col] = 0
                draw_grid(display, grid)
        return False       
    else:
        return True


# Creats grid from text on notepad
#
# @return grid, nestesd lists that represent a 9x9 grid of intergers

def get_unsolved():
    grid = []
    with open("unsolved.txt") as file:
        for line in file.readlines():
            row = []
            for number in line.strip("\n"):
                row.append(int(number))
            grid.append(row)
    return grid


# Prints grid in easier to see manor
def print_text_grid(grid):
    [print(i) for i in grid]
    print("\n")


if __name__ == "__main__":
    main()
