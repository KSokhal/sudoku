class Grid:
    def __init__(self):
        self.grid = [] 
        

    def get_unsolved_from_txt(self):
        with open('grid.txt') as file:
            for line in file.readlines():
                row = []
                for number in line.strip("\n"):
                    row.append(int(number))
                self.grid.append(row)
    

    def print_txt(self):
        for i in self.grid:
            print(i)
        print("\n")


    def get_next_empty_cell(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == 0:
                    return (row, col)
        return None


if __name__ == "__main__":
    grid = Grid()
    grid.get_unsolved_from_txt()
    grid.print_txt()