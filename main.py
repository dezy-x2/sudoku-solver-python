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
    rows, cols = getDimensions(puzzle)
    grid = {}
    for g in range(0, rows, 3):
        nums = []
        for i in range(0, cols, 3):
            temp = []
            for j in range(g, g + 3):
                for k in range(i, i + 3):
                    temp.append(puzzle[j][k])
            nums.append(temp)

        for x in range(len(nums)):
            key = f"{g+x}"
            grid[key] = nums[x]
    return grid


def findCoord(col, row, sudoku=puzzle):
    rows, cols = getDimensions(sudoku)
    rows /= 3
    cols /= 3
    over = m.floor(col/cols)
    down = m.floor(row/rows)
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
    return not numPresent(fullRow, num) and not numPresent(fullCol, num) and not numPresent(grid, num) and sudoku[row][col] == None


def generateEmptyPuzzle(colCount=9, rowCount=9):
    puzzle = []
    for i in range(rowCount):
        row = []
        for j in range(colCount):
            row.append(None)
        puzzle.append(row)
    return puzzle


def randomPlacer(depth):
    failCount = 0
    failed = False
    sudoku = None
    while True:
        failed = False
        uniquePairArr = set()
        sudoku = generateEmptyPuzzle()
        row, col = getDimensions(sudoku)
        count = 0
        for i in range(1, depth+1):
            # print(i, "*")
            while count < 9:
                # print(count, i)w
                rowToPlace = m.floor(random.random() * row)
                colToPlace = m.floor(random.random() * col)
                uniquePairArr.add(makeUniquePair(rowToPlace, colToPlace))
                if legalPlacement(colToPlace, rowToPlace, i, sudoku):
                    # print("hi")
                    sudoku[rowToPlace][colToPlace] = i
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
    return sudoku


def makeUniquePair(a, b):
    return a + b*10


def isIllegalBoard(arr):
    # print("stupid", len(arr), len(arr) == 81)
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


print(makeGrid(randomPlacer(9)))
