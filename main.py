import pygame

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

    global unsolved_grid
    unsolved_grid = get_unsolved()
    solved_grid = unsolved_grid.copy()
    end = False
    #while True:
    for i in range(10):
        solved_grid = unsolved_grid.copy()
        solved_grid = cycle(solved_grid)
        print(unsolved_grid == solved_grid)
        if unsolved_grid == solved_grid:
            break
        
    print_grid(solved_grid)

def cycle(grid):
    solved_grid = grid.copy()
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 0:
                common = get_valid_options(row, col)
                solved_grid = fill_in_easy(common, solved_grid, row, col)
    return solved_grid

def get_valid_options(row, col):
    valid, missing = get_check_lists(row, col)

    if valid:
        return

    for i in missing:
        if len(i) == 1:
            print(i, row, col)
            return i

    common = set(missing[0])
    for numbers in missing[1:]:
        common.intersection_update(numbers)

    common = list(common)
    return common


def fill_in_easy(common, grid, row, col):
    new_grid = grid.copy()
    if len(common) == 1:
        new_grid[row][col] = common[0]
    return new_grid


def get_check_lists(row, col):
    horizontal_check_list = unsolved_grid[row]
    vertical_check_list = [x[col] for x in unsolved_grid]

    if row in [0, 1, 2]:
        square = unsolved_grid[:3]
    elif row in [3, 4, 5]:
        square = unsolved_grid[3:6]
    elif row in [6, 7, 8]:
        square = unsolved_grid[6:9]

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

    valid = True
    missing_numbers = []

    for each_list in [horizontal_check_list, vertical_check_list, square_check_list]:
        temp_valid, temp_missing = check_list(each_list)
        valid = (valid and temp_valid)
        missing_numbers.append(temp_missing)
    if row == 0 and col == 7:
        print(horizontal_check_list, vertical_check_list, square_check_list)
        print(missing_numbers)
    return valid, missing_numbers



# Check if list is valid and get the numbers that are not present
def check_list(list):
    missing_numbers = []
    valid = True
    for i in range(1, 10):
        count = list.count(i)
        if count > 1:
            valid = False
        elif count == 0:
            valid = False
            missing_numbers.append(i)
    return valid, missing_numbers

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
