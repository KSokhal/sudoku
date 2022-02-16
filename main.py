import copy
import time
from math import floor
from grid import Grid

import pygame

# Set display dimensions
DISPLAY_WIDTH = 700
DISPLAY_HEIGHT = 600

# Sets colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREY = (100, 100, 100)
DARK_GREY = (65, 65, 65)


# Sets constants for display of grid
GRID_START_POS = (50, 50)
CELL_SIZE = 50

def main():
    # Generates grids from text file
    grid = Grid()
    grid.get_unsolved_from_txt()
    original_grid = copy.deepcopy(grid.grid)

    # Initialises varibles for pygame
    pygame.init()
    global font, small_font
    font = pygame.font.SysFont("ubuntumono", 40)
    small_font = pygame.font.SysFont("ubuntumono", 30)
    game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("Sudoku")
    game_display.fill(WHITE)
    clock = pygame.time.Clock()
    draw_grid(game_display, grid.grid)

    end = False
    allow_edit = False
    
    while not end:
        # Quit case
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
        
        # Draws 'sovle' button and wait for it to be pressed
        btn = button(game_display, (GRID_START_POS[0] + (10 * CELL_SIZE), GRID_START_POS[1] + CELL_SIZE), ((2 * CELL_SIZE), CELL_SIZE), LIGHT_GREY, DARK_GREY, "Solve")
        if btn:
            # If button is pressed, display original grid and solve
            draw_grid(game_display, grid.grid)
            grid.solve(draw_cell, game_display)

        # Checks if the grid has been manually completed
        if grid.check():
            text = font.render("Level Complete!", True, GREEN)
            exit_str = "Press any key to quit..."
            small_text = small_font.render(exit_str , True, BLACK)
            win_text_start = (50, 525)

            game_display.blit(text, win_text_start)
            game_display.blit(small_text, (win_text_start[0], win_text_start[1] + small_font.size(exit_str)[1] + 20))
            pygame.display.update()

            ev = pygame.event.wait()
            if ev.type == pygame.KEYDOWN or ev.type == pygame.QUIT:
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
            elif keys[pygame.K_BACKSPACE]:
                number = "0"
                
            if number is not None:
                grid[y][x] = int(number)
                pygame.draw.rect(game_display, WHITE, (GRID_START_POS[0] + 10 + (x * CELL_SIZE), GRID_START_POS[1] + 10 + (y * CELL_SIZE), CELL_SIZE - 20, CELL_SIZE - 20), 0)
                
                if number != "0":
                    if grid.check_if_valid(y, x, int(number)):
                        text_colour = BLACK
                    else:
                        text_colour = RED

                    text = font.render(number, True, text_colour)
                    text_size = font.size(number)
                    text_start_pos = (round((CELL_SIZE - text_size[0]) / 2), round((CELL_SIZE - text_size[1]) / 2))
                    game_display.blit(text, (GRID_START_POS[0] + text_start_pos[0] + (x * CELL_SIZE), GRID_START_POS[1] + text_start_pos[1] + (y * CELL_SIZE)))
            
                pygame.display.update()

        clock.tick(60)

    pygame.quit()
    quit()



def draw_cell(display, col, row , value, text_colour = BLACK, update=True):
    pygame.draw.rect(display, BLACK, (GRID_START_POS[0] + (row * CELL_SIZE), GRID_START_POS[1] + (col * CELL_SIZE), CELL_SIZE, CELL_SIZE), 1)
    value = str(value)
    if value == "0":
        pygame.draw.rect(display, WHITE, (GRID_START_POS[0] + 10 + (row * CELL_SIZE), GRID_START_POS[1] + 10 + (col * CELL_SIZE), CELL_SIZE - 20, CELL_SIZE - 20), 0)
    else:
        text = font.render(value, True, text_colour)
        text_size = font.size(value)
        text_start_pos = (round((CELL_SIZE - text_size[0]) / 2), round((CELL_SIZE - text_size[1]) / 2))
        display.blit(text, (GRID_START_POS[0] + text_start_pos[0] + (row * CELL_SIZE), GRID_START_POS[1] + text_start_pos[1] + (col * CELL_SIZE)))
    if update:
        pygame.display.update()


# ## Draws a grid
# #
# # @param display, the pygame display
# # @param grid, nestesd lists that represent a 9x9 grid of intergers

def draw_grid(display, grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            cell_value = str(grid[col][row])
            draw_cell(display, col, row , cell_value, update=False)
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(display, BLACK, (GRID_START_POS[0] + (i * CELL_SIZE * 3), GRID_START_POS[1] + (j * CELL_SIZE * 3), CELL_SIZE * 3, CELL_SIZE * 3), 5)
    pygame.display.update()


## Displays a button on the screen, and check if clicked 
#
# @param display, the pygame display
# @param pos, the position of the button
# @param size, the size of the button
# @param active_colour, the backgroud colour of the button when the mouse is hovering over it
# @param inactive_colour, the backgroud colour of the button when the mouse is not hovering over it
# @param display_text, the text that is displayed on the button
#
# @return boolean, if the button is clicked return True

def button(display, pos, size, active_colour, inactive_colour, display_text):

    text = font.render(display_text, True, BLACK)
    text_size = font.size(display_text)
    text_start_pos = (round((size[0] - text_size[0]) / 2), round((size[1] - text_size[1]) / 2))
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    mouse_on_button = mouse[0] > pos[0] and mouse[0] < (pos[0] + size[0]) and mouse[1] > pos[1] and mouse[1] < (pos[1] + size[1])

    if mouse_on_button:
        pygame.draw.rect(display, active_colour, (pos[0], pos[1], size[0], size[1]), 0)
    else:
        pygame.draw.rect(display, inactive_colour, (pos[0], pos[1], size[0], size[1]), 0)
    
    display.blit(text, (pos[0] + text_start_pos[0], pos[1] + text_start_pos[1]))
    pygame.display.update()

    if mouse_on_button and click[0] == 1:
        return True
    else:
        return False


if __name__ == "__main__":
    main()
