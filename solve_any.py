
def check_if_valid(grid, row, col, number):

    for i in range(len(grid)):
        if grid[row][i] == number and col != i:
            return False

    # Check Col
    for i in range(len(grid)):
        if grid[i][col] == number and col != i:
            return False

    square = [(row // 3) * 3, (col//3) * 3]
    
    for i in range(square[0] , square[0] + 3):
        for j in range(square[1], square[1] + 3):
            if number == grid[i][j] and i != row and j != col:
                return False

    return True

def get_next_empty_cell(grid):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                return (row, col)
    return None

def fill_in_grid(grid):
    #print(get_next_empty_cell(grid))
    
    find = get_next_empty_cell(grid)
    if find:
        empty_row, empty_col = find
    else:
        return True

    for i in range(1,10):
        if check_if_valid(grid, empty_row, empty_col, i):
            grid[empty_row][empty_col] = i
            
            if fill_in_grid(grid):
                return True

            grid[empty_row][empty_col] = 0


    return False
    # if get_next_empty_cell(grid) is not None:
    #     empty_row, empty_col = get_next_empty_cell(grid)

    #     for i in range(1, 10):
    #         if check_if_valid(grid, empty_row, empty_col, i):
    #             grid[empty_row][empty_col] = i
            
    #             if fill_in_grid(grid):
    #                 return True

    #             grid[empty_row][empty_col] = 0

    #     return False
                
    # else:
    #     print_grid(grid)
    #     return True

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


def main():
    grid = get_unsolved()
    fill_in_grid(grid)
    print_grid(grid)


main()