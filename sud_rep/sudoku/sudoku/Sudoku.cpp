#include "Sudoku.h"

Sudoku::Sudoku()
{
	initGrid();
}

Sudoku::Sudoku(int v[N][N])
{
	setGrid(v);
}

Sudoku::Sudoku(Sudoku& other)
{
	for (int x = 0; x < N; ++x)
	{
		for (int y = 0; y < N; ++y)
		{
			setValue(x, y, other.grid[x][y]);
			grid[x][y] = other.grid[x][y];
		}
	}
}

const void Sudoku::initGrid()
{
	for (int i = 0; i < N; ++i)
	{
		for (int j = 0; j < N; ++j)
		{
			setValue(i, j, 0);
		}
	}
}

const void Sudoku::setGrid(const int v[N][N])
{
	for (int x = 0; x < N; ++x)
	{
		for (int y = 0; y < N; ++y)
		{
			setValue(x, y, v[x][y]);
		}
	}
}

const void Sudoku::getGrid(int v[N][N]) const
{
	for (int x = 0; x < 9; ++x)
	{
		for (int y = 0; y < 9; ++y)
		{
			v[x][y] = getValue(x, y);
		}
	}
}

const int Sudoku::getValue(int x, int y) const
{
	return grid[x][y];
}

const void Sudoku::setValue(int x, int y, int v)
{
	grid[x][y] = v;
}

bool Sudoku:: isSafe(int v[N][N], int row, int col, int num)
{

	// Check if we find the same num
	// in the similar row , we
	// return false
	for (int x = 0; x < N; x++)
		if (v[row][x] == num)
			return false;

	// Check if we find the same num in
	// the similar column , we
	// return false
	for (int x = 0; x < N; x++)
		if (v[x][col] == num)
			return false;

	// Check if we find the same num in
	// the particular 3*3 matrix,
	// we return false
	int startRow = row - row % 3,
		startCol = col - col % 3;

	for (int i = 0; i < 3; i++)
		for (int j = 0; j < 3; j++)
			if (v[i + startRow][j + startCol] == num)
				return false;

	return true;
}

const bool sudokuSolve(Sudoku &su, int row, int col)
{
	// Check if we have reached the 8th
	// row and 9th column (0
	// indexed matrix) , we are
	// returning true to avoid
	// further backtracking
	if (row == N - 1 && col == N)
		return true;

	// Check if column value  becomes 9 ,
	// we move to next row and
	//  column start from 0
	if (col == N) {
		row++;
		col = 0;
	}

	// Check if the current position of
	// the grid already contains
	// value >0, we iterate for next column
	if (su.getValue(row, col) > 0)
		return sudokuSolve(su, row, col + 1);

	for (int num = 1; num <= N; num++)
	{

		// Check if it is safe to place
		// the num (1-9)  in the
		// given row ,col  ->we
		// move to next column
		if (su.isSafe(su.grid, row, col, num))
		{

			/* Assigning the num in
			   the current (row,col)
			   position of the grid
			   and assuming our assigned
			   num in the position
			   is correct     */
			su.setValue(row,col, num);

			//  Checking for next possibility with next
			//  column
			if (sudokuSolve(su, row, col + 1))
				return true;
		}

		// Removing the assigned num ,
		// since our assumption
		// was wrong , and we go for
		// next assumption with
		// diff num value
		su.setValue(row,col, 0);
	}
	return false;
}

const bool Sudoku::checkGrid() const
{
	set<int> squares[3][3];
	set<int> lines[2][9];

	for (int x = 0; x < 9; ++x)
	{
		for (int y = 0; y < 9; ++y)
		{
			int value = getValue(x, y);

			if (value != 0)
			{
				if (squares[x / 3][y / 3].find(value) == squares[x / 3][y / 3].end())
				{
					squares[x / 3][y / 3].insert(value);
				}
				else
				{
					return false;
				}

				if (lines[0][y].find(value) == lines[0][y].end())
				{
					lines[0][y].insert(value);
				}
				else
				{
					return false;
				}

				if (lines[1][x].find(value) == lines[1][x].end())
				{
					lines[1][x].insert(value);
				}
				else
				{
					return false;
				}
			}
		}
	}
	return true;
}

ostream& operator<<(ostream& os, const Sudoku& su)
{
	for (int y = 0; y < 9; ++y)
	{
		for (int x = 0; x < 9; ++x)
		{
			cout << su.grid[x][y] << " ";
		}
		cout << endl;
	}
	return os;
}

