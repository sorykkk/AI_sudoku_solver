N = 9
P = print

def format_grid(g):
    for n, l in enumerate(g):
        for m, c in enumerate(l):
            P(str(c).replace("0", "."), end="")
            if(m in {2, 5}):
                P("+", end="")
        P()
        if(n in {2, 5}):
            P("+" * 11)

def verify_init(grid):
    for i in range(N):
        for j in range(N):
            if(grid[i][j]):
                for k in range(N):# verifica linia orizontala
                    if(j != k and grid[i][k] and grid[i][j] == grid[i][k]):
                        #print(f"F{grid[i][j]} {grid[i][k]} {i, j} {i, k}")
                        return False
                for k in range(N):# verifica linia verticala
                    if(i != k and grid[k][j] and grid[i][j] == grid[k][j]):
                        #print(f"S{grid[i][j]} {grid[k][j]} {i, j} {k, j}")
                        return False
                
                start_row = i - i % 3
                start_col = j - j % 3
                for k in range(3):
                    for l in range(3):
                        if(grid[k + start_row][l + start_col] == grid[i][j] and 
                            (k + start_row) != i and (l + start_col) != j):
                            print(grid[i][j])
                            return False
    return True

def is_safe(grid, row, col, num):
    for x in range(N):
        if(grid[row][x] == num):
            return False

    for x in range(N):
        if(grid[x][col] == num):
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if(grid[i + start_row][j + start_col] == num):
                return False
    return True

def solve_sudoku(grid, row, col):
    if(row == N - 1 and col == N):
        return True

    if(col == N):
        row += 1
        col = 0

    if(grid[row][col] > 0):
        return solve_sudoku(grid, row, col + 1)

    for num in range(1, N + 1, 1):
        if is_safe(grid, row, col, num):
            grid[row][col] = num

            if solve_sudoku(grid, row, col + 1):
                return True

        grid[row][col] = 0
    
    return False


def sudoku(grid_init):
    grid = [row[:] for row in grid_init]# deep copy of 2D array
    print("Visualized initial sudoku:")
    format_grid(grid)

    if(not verify_init(grid)):
        P("\nIncorrect initial matrix(sudoku)\n")
        return

    if(solve_sudoku(grid, 0, 0)):
        P("\nVisualized solution:")
        format_grid(grid)

        return (grid)
    else:
        P("\nNo solution exist\n")