N = 9 # numarul de patrate pe un rand
P = print

def format_grid(g):
    # parcurgem randurile extrase din sudoku
    for n, l in enumerate(g):
        for m, c in enumerate(l):
            # in loc de 0 punem puncte sa vizualizam mai usor
            P(str(c).replace("0", "."), end="")
            # formam grila tipica a sudoku
            if(m in {2, 5}):
                P("+", end="")
        P()
        if(n in {2, 5}):
            P("+" * 11)

# verificam daca nu este vreo greseala la citirea grilei
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
    return True

# verifica daca va fi corect de adaugat num
# la randul si coloana data
def is_safe(grid, row, col, num):

    # verifica daca gasim acelasi num
    # in randul acelasi rand, daca da
    # returnam false
    for x in range(N):
        if(grid[row][x] == num):
            return False

    # verifica daca gasim acelasi num
    # in randul aceeasi coloana, daca da
    # returnam false
    for x in range(N):
        if(grid[x][col] == num):
            return False

    # verifica daca gasim acelasi num
    # in patratul 3x3, daca da
    # returnam false
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if(grid[i + start_row][j + start_col] == num):
                return False
    return True

# ia o matrice completata si incearca sa atribuie
# valori locatiei cu cifra 0 in asa mod in cat
# sa corespunda regulilor Sudoku (sa nu fie 2 sau 
# mai multe cifre pe acelasi rand sau coloana sau
# in patratul 3x3)
def solve_sudoku(grid, row, col):

    # verifica daca s-a ajuns la al 8-lea rand
    # si a 9-a coloana, daca da se returneaza 
    # true pentru a preveni urmatoarea iteratie
    # in backtracking
    if(row == N - 1 and col == N):
        return True
    
    # verifica daca valoarea coloanei
    # devine 0, pentru a ne muta pe 
    # urmatorul rand si a incepe 
    # a numara coloana de la 0
    if(col == N):
        row += 1
        col = 0

    # verifica daca pozitia curenta in grila
    # deja contine valoare > 0, iteram pana la
    # urmatoarea coloana
    if(grid[row][col] > 0):
        return solve_sudoku(grid, row, col + 1)

    # iterarea de la 1 pana la 9 pentru a genera 
    # numerele care trebuie inserate in loc de 0
    for num in range(1, N + 1, 1):

        # verifica daca e sigur sa punem
        # num in randul si coloana data
        # daca da noi ne ducem sprea alta coloana
        if is_safe(grid, row, col, num):
        
            # atribuim num la randul si 
            # coloana curenta, asumam
            # ca numarul atribuit e corect
            grid[row][col] = num

            # verifica pentru urmatoarea posibilitate
            # in coloana urmatoare
            if solve_sudoku(grid, row, col + 1):
                return True

        # stergem numarul atribuit
        # caci asuamrea a fost gresita 
        # deci facem urmatoare asumare 
        # cu o valoare diferita a lui num
        grid[row][col] = 0
    
    # daca nu a fost returnat true in bucla cu num
    # rezulta ca nu a fost gasita solutia, deci 
    # returnam false
    return False


def sudoku(grid_line):
    print("Visualized initial sudoku:")
    format_grid(grid_line)
    # convertim grid in format of matrix
    grid = [None]*len(grid_line)#grid = grid_line.copy()
    for i, v in enumerate(grid_line):
        grid[i] = [int(c) for c in v]

    if(not verify_init(grid)):
        P("\nIncorrect initial matrix(sudoku)\n")
        return

    if(solve_sudoku(grid, 0, 0)):
        # doar stilistica/informativ
        grid_form = grid_line.copy()
        # convertim din grid inapoi in grid_line
        for i, v in enumerate(grid):
            grid_form[i] = "".join([str(c) for c in v])
        P("\nVisualized solution:")
        format_grid(grid_form)

        return (grid)
    else:
        P("\nNo solution exist\n")