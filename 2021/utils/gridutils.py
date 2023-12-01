def print_grid(grid, format=None):
    for x in range(len(grid)):
        line = ""
        for y in range(len(grid[x])):
            if format is None:
                line += str(grid[x][y])
            else:
                line += str(format(grid[x][y]))
        print(line)
