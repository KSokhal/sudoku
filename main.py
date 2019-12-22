import pygame
import copy

# Set display dimensions
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

# Sets colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def main():
    
    # pygame.init()

    # game_display = pygame.display.set_mode((display_width, display_height))
    # pygame.display.set_caption("Sudoku")
    
    # clock = pygame.time.Clock()

    grid = get_unsolved()

    end = False

    while end == False:
        before = copy.deepcopy(grid)
        grid = cycle(grid)
        if before == grid:
            end = True

    print_grid(grid)

def cycle(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 0:
                common = get_valid_options(grid, row, col)
                grid = fill_in_easy(grid, row, col, common)
    return grid

def get_valid_options(grid, row, col):
    missing_numbers = get_check_lists(grid, row, col)

    for i in missing_numbers:
        if len(i) == 1:
            return i

    common = set(missing_numbers[0])
    for numbers in missing_numbers[1:]:
        common.intersection_update(numbers)

    common = list(common)
    return common


def fill_in(grid, row, col, number_options):
    if len(number_options) == 1:
        grid[row][col] = number_options[0]
    else:
        for option in number_options:
            grid[row][col] = option
            

    return grid


def get_check_lists(grid, row, col):
    horizontal_check_list = grid[row]
    vertical_check_list = [x[col] for x in grid]
    square_check_list = get_square_list(grid, row, col)

    missing_numbers = []
    for each_list in [horizontal_check_list, vertical_check_list, square_check_list]:
        missing_numbers.append(check_list(each_list))

    return missing_numbers

def get_square_list(grid, row, col):
    if row in [0, 1, 2]:
        square = grid[:3]
    elif row in [3, 4, 5]:
        square = grid[3:6]
    elif row in [6, 7, 8]:
        square = grid[6:9]

    if col in [0, 1, 2]:
        square = [x[:3] for x in square]
    elif col in [3, 4, 5]:
        square = [x[3:6] for x in square]
    elif col in [6, 7, 8]:
        square = [x[6:9] for x in square]
    
    square_check_list = []

    for i in square:
        for j in i:
            square_check_list.append(j)

    return square_check_list



# Check if list is valid and get the numbers that are not present
def check_list(list):
    missing_numbers = []
    for number in range(1, 10):
        count = list.count(number)
        if count == 0:
            missing_numbers.append(number)
        if count > 1:
            pass
    return missing_numbers

# Fills in the list with the missing numbers
def fill_in_list(list, missing_numbers):
    for missing in missing_numbers:
        for i in range(len(list)):
            if list[i] == 0:
                list[i] = missing
                break
    return list

# Creats grid from text on notepad
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
def print_grid(grid):
    [print(i) for i in grid]
    print("\n")


if __name__ == "__main__":
    main()
