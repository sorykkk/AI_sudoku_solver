#grid_line = ['762000004', '080040007', '050028010', '000604030', '906012040', '024050000', '000009000', '070001000', '008473060']


#grid = [None]*len(grid_line)#grid = grid_line.copy()
#for i, v in enumerate(grid_line):
#    grid[i] = [int(c) for c in v]

#print("Splited grid: ", grid)

#for i, v in enumerate(grid):
#    grid_line[i] = "".join([str(c) for c in v])

#print(grid_line)

grid = [[ 0, 0, 5, 0, 0, 0, 0, 0, 0 ],
        [ 8, 0, 0, 0, 0, 0, 0, 2, 0 ],
        [ 0, 7, 0, 0, 1, 0, 5, 0, 0 ],
        [ 4, 0, 0, 0, 0, 5, 3, 0, 0 ],
        [ 0, 1, 0, 0, 7, 0, 0, 0, 6 ],
        [ 0, 0, 3, 2, 0, 7, 0, 8, 0 ],
        [ 0, 6, 0, 5, 0, 0, 0, 0, 9 ],
        [ 0, 0, 4, 0, 0, 0, 0, 3, 0 ],
        [ 0, 0, 0, 0, 7, 9, 7, 0, 0 ] ]


N = 9
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


print(verify_init(grid))