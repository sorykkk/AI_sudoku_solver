N = 9 #numarul de patrate pe un rand
P = print

def format_grid(g):
    for n, l in enumerate(g):
        for m, c in enumerate(l):
            P(str(c).replace("0", "."), end="")
            if m in {2, 5}:
                P("+", end="")
        P()
        if n in {2, 5}:
            P("+" * 11)

def verify_init(grid):
    for i in range(N):
        for j in range(N):
            if(grid[i][j]):
                for k in range(N):#verifica linia orizontala
                    if(j != k and grid[i][k] and grid[i][j] == grid[i][k]):
                        #print(f"F{grid[i][j]} {grid[i][k]} {i, j} {i, k}")
                        return False
                for k in range(N):#verifica linia verticala
                    if(i != k and grid[k][j] and grid[i][j] == grid[k][j]):
                        #print(f"S{grid[i][j]} {grid[k][j]} {i, j} {k, j}")
                        return False
    return True


# Checks whether it will be
# legal to assign num to the
# given row, col
def is_safe(grid, row, col, num):

    # Check if we find the same num
    # in the similar row , we
    # return false
    for x in range(N):
        if grid[row][x] == num:
            return False

    # Check if we find the same num in
    # the similar column , we
    # return false
    for x in range(N):
        if grid[x][col] == num:
            return False

    # Check if we find the same num in
    # the particular 3*3 matrix,
    # we return false
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    return True

# Takes a partially filled-in grid and attempts
# to assign values to all unassigned locations in
# such a way to meet the requirements for
# Sudoku solution (non-duplication across rows,
# columns, and boxes) */
def solve_sudoku(grid, row, col):

    # Check if we have reached the 8th
    # row and 9th column (0
    # indexed matrix) , we are
    # returning true to avoid
    # further backtracking
    if (row == N - 1 and col == N):
        return True
    
    # Check if column value  becomes 9 ,
    # we move to next row and
    # column start from 0
    if col == N:
        row += 1
        col = 0

    # Check if the current position of
    # the grid already contains
    # value >0, we iterate for next column
    if grid[row][col] > 0:
        return solve_sudoku(grid, row, col + 1)
    for num in range(1, N + 1, 1):
    
        # Check if it is safe to place
        # the num (1-9)  in the
        # given row ,col  ->we
        # move to next column
        if is_safe(grid, row, col, num):
        
            # Assigning the num in
            # the current (row,col)
            # position of the grid
            # and assuming our assigned
            # num in the position
            # is correct
            grid[row][col] = num

            # Checking for next possibility with next
            # column
            if solve_sudoku(grid, row, col + 1):
                return True

        # Removing the assigned num ,
        # since our assumption
        # was wrong , and we go for
        # next assumption with
        # diff num value
        grid[row][col] = 0
    return False


def sudoku(grid_line):
    print("Visualized initial sudoku:")
    format_grid(grid_line)
    #convertim grid in format of matrix
    grid = [None]*len(grid_line)#grid = grid_line.copy()
    for i, v in enumerate(grid_line):
        grid[i] = [int(c) for c in v]

    if(not verify_init(grid)):
        P("\nIncorrect initial matrix(sudoku)\n")
        return

    if(solve_sudoku(grid, 0, 0)):
        #doar stilistica/informativ
        grid_form = grid_line.copy()
        #convertim din grid inapoi in grid_line
        for i, v in enumerate(grid):
            grid_form[i] = "".join([str(c) for c in v])
        P("\nVisualized solution:")
        format_grid(grid_form)

        return (grid)
    else:
        P("\nNo solution exist\n")

