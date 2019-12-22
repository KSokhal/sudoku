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
        else:
            print("Still solving...")


    print_grid(grid)


# Checks if a list is valid and get the numbers that are not present
def check_list(list):
    valid = True
    missing_numbers = []
    for number in range(1, 10):
        count = list.count(number)
        if count == 0:
            valid = False
            missing_numbers.append(number)
        if count > 1:
            valid = False
    return valid, missing_numbers


# Checks all the lists; the horizontal, vertical, and square lists
def check_all_lists(grid, row, col):
    horizontal_check_list = grid[row]
    vertical_check_list = [x[col] for x in grid]
    square_check_list = get_square_list(grid, row, col)

    valid = True
    missing_numbers = []

    for each_list in [horizontal_check_list, vertical_check_list, square_check_list]:
        temp_valid, temp_missing_numbers = check_list(each_list)
        valid = (valid and temp_valid)
        missing_numbers.append(temp_missing_numbers)

    return valid, missing_numbers


# Gets the 3x3 square the defined number is in, as a list
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


# Gets the valid options for an empty square
def get_valid_options(grid, row, col):
    missing_numbers = check_all_lists(grid, row, col)[1]

    for i in missing_numbers:
        if len(i) == 1:
            return i

    common = set(missing_numbers[0])
    for numbers in missing_numbers[1:]:
        common.intersection_update(numbers)

    common = list(common)
    return common


# Cycles through ea\ch cell in grid and attempts to solve if empty
def cycle(grid):
    empty_cells = []
    cell_options = []
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 0:
                number_options = get_valid_options(grid, row, col)
                empty_cells.append([row, col])
                cell_options.append(number_options)
                grid = fill_in(grid, empty_cells, cell_options)

    if len(empty_cells) == 0:
        return True
    else:
        return grid


# Logic for filling in empty cells
def fill_in(grid, empty_cells, cell_options):
    for cell in range(len(empty_cells)):
        row = empty_cells[cell][0]
        col = empty_cells[cell][1]
        options = cell_options[cell]

        if len(options) == 1:
            grid[row][col] = options[0]
        else:
            for option in options:
                grid[row][col] = option
                grid = cycle(grid)
                print(type(grid))
                if type(grid) == bool:
                    print("Finshed")
                    return
                else:
                    grid[row][col] = 0
                    print("contniueing")
                    continue

                    
                                




    # if len(number_options) == 1:
    #     grid[row][col] = number_options[0]
    # else:
    #     for option in number_options:
    #         grid[row][col] = option
    #         if check_all_lists(grid, row, col)[0] == True:
    #             break
    #         else:
    #             continue

    return grid


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
