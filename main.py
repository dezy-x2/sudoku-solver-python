import math as m
import random
puzzle = [
    [9, None, None, 6, 4, None, None, None, 3],
    [2, 7, None, None, 9, None, 5, 8, None],
    [None, 1, None, 5, 8, None, None, None, None],
    [None, 9, None, None, None, None, 7, None, None],
    [None, None, 7, 9, 6, 5, 8, None, None],
    [None, None, 2, None, None, None, None, 4, None],
    [None, None, None, None, 5, 3, None, 6, None],
    [None, 5, 1, None, 7, None, None, 2, 8],
    [4, None, None, None, 1, 6, None, None, 5],
]


def getDimensions(puzzle):
    return len(puzzle), len(puzzle[0])


def makeGrid(puzzle):
    # need to find the dimensions of the puzzle
    rows, cols = getDimensions(puzzle)
    # each grid is an array with the key being its coordinates
    grid = {}
    # iterate through the rows
    for g in range(0, rows, 3):
        # this arr is used to keep arrs of a rows grids
        nums = []
        # iterate through the columns
        for i in range(0, cols, 3):
            # this arr holds one grid and is added to the nums arr
            temp = []
            # these two loops go through each num in the grid
            for j in range(g, g + 3):
                for k in range(i, i + 3):
                    temp.append(puzzle[j][k])
            nums.append(temp)
        # this loop breaks down the nums arr into the grid
        for x in range(len(nums)):
            key = f"{g+x}"
            grid[key] = nums[x]
    return grid


def findCoord(col, row, sudoku=puzzle):
    # we need to know how many rows and columns there are
    rows, cols = getDimensions(sudoku)
    # since each grid is 3x3 dividing the rows and columns by 3 gives us the grid num
    rows /= 3
    cols /= 3
    # this tells us how far over and down the coords are from 0,0
    over = m.floor(col/cols)
    down = m.floor(row/rows)
    # multiplying down by 3 moves us to the correct row and adding over gives us the correct col
    final = down * 3 + over
    return final


def getRowAndCol(col, row, sudoku=puzzle):
    fullRow = sudoku[row]
    fullCol = []
    for i in range(len(sudoku)):
        fullCol.append(sudoku[i][col])
    return fullRow, fullCol


def numPresent(arr, num):
    return num in arr


def legalPlacement(col, row, num, sudoku=puzzle):
    fullRow, fullCol = getRowAndCol(col, row, sudoku)
    grids = makeGrid(sudoku)
    coord = findCoord(col, row)
    grid = grids[str(coord)]
    return not numPresent(fullRow, num) and\
        not numPresent(fullCol, num) and not numPresent(
            grid, num) and sudoku[row][col] == None


def generateEmptyPuzzle(colCount=9, rowCount=9):
    puzzle = []
    for i in range(rowCount):
        row = []
        for j in range(colCount):
            row.append(None)
        puzzle.append(row)
    return puzzle


def randomPlacerOneNumAtATime(depth):
    # this is just to keep track of fails not actually important
    failCount = 0
    # we need this to know whether to break or not
    failed = False
    sudoku = None
    # this loop is here in place of recursion because the recursion would be too deep
    while True:
        # need to make sure that it is false before we start
        failed = False
        # the set makes sure that we don't repeat any numbers
        uniquePairArr = set()
        # creates the puzzle that we will be populating
        sudoku = generateEmptyPuzzle()
        row, col = getDimensions(sudoku)
        count = 0
        # i is the the number that we are trying to place in the sudoku
        for i in range(1, depth+1):
            # keep trying to place i until it has been placed 9 times
            while count < 9:
                # generate a random row and column
                rowToPlace = m.floor(random.random() * row)
                colToPlace = m.floor(random.random() * col)
                # add the row and column to the set
                uniquePairArr.add(makeUniquePair(rowToPlace, colToPlace))
                # we need to check if it is legal to place the number here
                if legalPlacement(colToPlace, rowToPlace, i, sudoku):
                    sudoku[rowToPlace][colToPlace] = i
                    count += 1
                elif isIllegalBoard(uniquePairArr):
                    failCount += 1
                    print(f"FAIL #{failCount}")
                    # since it failed we need to mark it as failed so it exits properly
                    failed = True
                    break
            # resets old values
            uniquePairArr.clear()
            count = 0
            # if it failed we need to completely reset the puzzle
            if failed:
                break
        # if it is here and hasn't failed that means it was completed
        if not failed:
            break
    return sudoku


def randomPlacerOneThroughNine(depth=9):
    failCount = 0
    failed = False
    sudoku = None
    while True:
        failed = False
        uniquePairArr = set()
        sudoku = generateEmptyPuzzle()
        row, col = getDimensions(sudoku)
        for _ in range(0, depth):
            for i in range(1, depth+1):
                placed = False
                while not placed:
                    placed = False
                    rowToPlace = m.floor(random.random() * row)
                    colToPlace = m.floor(random.random() * col)
                    uniquePairArr.add(makeUniquePair(rowToPlace, colToPlace))
                    if legalPlacement(colToPlace, rowToPlace, i, sudoku):
                        sudoku[rowToPlace][colToPlace] = i
                        placed = True
                    elif isIllegalBoard(uniquePairArr):
                        failCount += 1
                        print(f"FAIL #{failCount}")
                        failed = True
                        break
                if failed:
                    break
            if failed:
                print("=================================")
                uniquePairArr.clear()
                break
        if not failed:
            break
    return sudoku


def makeUniquePair(a, b):
    return a + b*10


def isIllegalBoard(arr):
    return len(arr) == 81


def puzzlefy(sudoku, numEliminated=9):
    row, col = getDimensions(sudoku)
    for i in range(row):
        rowToElim = m.floor(random.random() * row)
        colToElim = m.floor(random.random() * col)
        sudoku[rowToElim][colToElim] = None
    return sudoku


def getNumberCount(sudoku):
    countDict = {1: 9, 2: 9, 3: 9, 4: 9, 5: 9, 6: 9, 7: 9, 8: 9, 9: 9}
    for i in range(len(sudoku)):
        for j in range(len(sudoku[i])):
            if sudoku[i][j] != None:
                countDict[sudoku[i][j]] -= 1
    return countDict


def solvePuzzle(sudoku):
    failCount = 0
    failed = False
    sudokuCopy = None
    while True:
        failed = False
        sudokuCopy = [arr.copy() for arr in sudoku]
        numberCount = getNumberCount(sudokuCopy)
        uniquePairArr = set()
        row, col = getDimensions(sudokuCopy)
        count = 0
        for i in range(1, 10):
            while count < numberCount[i]:
                rowToPlace = m.floor(random.random() * row)
                colToPlace = m.floor(random.random() * col)
                uniquePairArr.add(makeUniquePair(rowToPlace, colToPlace))
                if legalPlacement(colToPlace, rowToPlace, i, sudokuCopy):
                    sudokuCopy[rowToPlace][colToPlace] = i
                    count += 1
                elif isIllegalBoard(uniquePairArr):
                    failCount += 1
                    print(f"FAIL #{failCount}")
                    failed = True
                    break
            uniquePairArr.clear()
            count = 0
            if failed:
                break
        if not failed:
            break
    return sudokuCopy


print(randomPlacerOneThroughNine())
