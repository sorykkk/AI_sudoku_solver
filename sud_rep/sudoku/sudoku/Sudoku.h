/*
 * Sudoku.h
 *
 *  Created on: 10 Oct 2015
 *      Author: guillaume
 */

#ifndef SUDOKU_H_
#define SUDOKU_H_

#include <iostream>
#include <string>
#include <cstdlib>
#include <set>

using namespace std;

const int N = 9;

class Sudoku
{

private:
	int grid[N][N];

public:
	
	Sudoku();
	Sudoku(int v[N][N]);
	Sudoku(Sudoku& other);

	virtual ~Sudoku() {};

	const void setGrid(const int v[N][N]);
	const void getGrid(int v[N][N]) const;
	const bool checkGrid() const;


private:
	const void initGrid();
	const void setValue(int x, int y, int v);
	const int getValue(int x, int y) const;

	friend ostream& operator<<(ostream& os, const Sudoku& su);

	friend const bool sudokuSolve(Sudoku& su, int row, int col);
	bool isSafe(int grid[N][N], int row, int col, int num);
};

#endif /* SUDOKU_H_ */
