import pygame

# Set display dimensions
DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 900

# Sets colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def main():
    grid = get_unsolved()

    pygame.init()

    game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("Sudoku")
    game_display.fill(WHITE)
    clock = pygame.time.Clock()

    end = False

    while not end:
        # Quit case
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True

        
        draw_grid(game_display, grid)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        fill_in_grid(grid)
        draw_grid(game_display, grid)
        clock.tick(60)
    pygame.quit()
    #quit()



def draw_grid(display, grid):
    grid_start_pos = (100, 100)
    cell_size = 50
    font = pygame.font.SysFont("ubuntumono", 40)

    for row in range(len(grid)):
        for col in range(len(grid[col])):
            pygame.draw.rect(display, BLACK, (grid_start_pos[0] + (col * cell_size), grid_start_pos[1] + (col * cell_size), cell_size, cell_size), 1)
            if grid[row][col] != 0:
                cell_value = str(grid[col][row])
                text = font.render(cell_value, 1, BLACK)
                text_size = font.size(cell_value)
                text_start_pos = (round((cell_size - text_size[0]) / 2), round((cell_size - text_size[1]) / 2))
                display.blit(text, (grid_start_pos[0] + text_start_pos[0] + (col * cell_size), grid_start_pos[1] + text_start_pos[1] + (col * cell_size)))

    for i in range(3):
        for j in range(3):
            pygame.draw.rect(display, BLACK, (grid_start_pos[0] + (col * cell_size * 3), grid_start_pos[1] + (col * cell_size * 3), cell_size * 3, cell_size * 3), 5)

    pygame.display.update()


def button(display, pos, size, active_colour, inactive_colour, text):









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
    for i in range(len(grid)):
        if grid[row][i] == number and col != i:
            return False

    # Checks if all numbers in column occurs only once
    for i in range(len(grid)):
        if grid[i][col] == number and col != i:
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

def fill_in_grid(grid):
    # If an empty cell can be found contiue filling in grid, else return True
    if get_next_empty_cell(grid) is not None:
        # Get the next empty cell
        empty_row, empty_col = get_next_empty_cell(grid)
        for i in range(1, 10):
            # If the value of i is a valid option for the empty cell, enter it in
            if check_if_valid(grid, empty_row, empty_col, i):
                grid[empty_row][empty_col] = i
                # If the grid can be solved from this point continue solving, else reset the cell and try next number
                if fill_in_grid(grid):
                    return True
                grid[empty_row][empty_col] = 0
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