# Maxwell Carmichael 10/17/2020

from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem
import math

class SudokuCSP:
        # len(board) must be a perfect square
    def __init__(self, name, board, MRV = True, DH = False, LCV = True, AC3 = True, print = False):
        self.name = name

        # self.strmap = self.__strmap(neighborgraph) # int -> str
        # self.inverse_strmap = {value: key for key, value in self.strmap.items()} # str -> int
        # self.colormap = self.__colormap() # int -> str
        self.neighbors = self.__genNeighbors(board)

        # construct domain
        domain = self.__domainmap(board)
        # construct constraints
        constraints = self.__constraintmap(board)

        self.CSP = ConstraintSatisfactionProblem(self.neighbors, domain, constraints, MRV, DH, LCV, AC3, print)
        self.solution = self.__find_solution()

    def __find_solution(self):
        print("starting testing")
        return self.CSP.get_assignment()

        # each spot's neighbors are its column, row, and box
    def __genNeighbors(self, board):
        neighbormap = {}

        n = len(board)
        s = int(math.sqrt(len(board)))

        for i in range(0, n, 1):
            for j in range(0, n, 1):
                neighbors = set()

                boxi = i // s * s
                boxj = j // s * s

                # box
                for x in range(boxi, boxi + s, 1):
                    for y in range(boxj, boxj + s, 1):
                        if x != i and y != j:
                            neighbors.add(self.__coordToIndex(x, y, n))

                # column
                for y in range(0, n, 1):
                    if y != j:
                        neighbors.add(self.__coordToIndex(i, y, n))

                # row
                for x in range(0, n, 1):
                    if x != i:
                        neighbors.add(self.__coordToIndex(x, j, n))

                neighbormap[self.__coordToIndex(i, j, n)] = neighbors

        return neighbormap

    def __coordToIndex(self, x, y, n):
        return x + y*n

    def __domainmap(self, board):
        allnums = { 1,2,3,4,5,6,7,8,9 }
        domain = {}

        n = len(board)

        for x in range(0, n, 1):
            for y in range(0, n, 1):
                # domain is all numbers
                if board[y][x] == 0:
                    domain[self.__coordToIndex(x, y, n)] = allnums.copy()
                # domain is one number
                else:
                    domain[self.__coordToIndex(x, y, n)] = { board[y][x] }

        return domain

    def __constraintmap(self, board):
        constraints = {}

        # this will be the set of all possible combinations of numbers
        numsneq = set()
        for i in range(1, len(board) + 1, 1):
            for j in range(1, len(board) + 1, 1):
                if i != j:
                    numsneq.add((i,j))

        # neighbors will have this constraint
        for variable in self.neighbors:
            for neighbor in self.neighbors[variable]:
                if variable < neighbor:
                    constraints[(variable, neighbor)] = numsneq.copy()

        return constraints

    def __str__(self):
        string = "----\n"
        string += "Map Coloring CSP Problem: {:s}\n"
        string += "Heuristics/Inference:  MRV: {:s}. DH: {:s} LCV: {:s}. AC3: {:s}\n"

        if self.solution:
            string += "Number of recursion calls: {:d}\n"
            string += "Solution: {:s}\n"

            string = string.format(self.name, str(self.CSP.MRV_FLAG), str(self.CSP.DH_FLAG), str(self.CSP.LCV_FLAG), str(self.CSP.AC3_FLAG), str(self.__solutionToStr()))
        else:
            string += "No solution found after {:d} recursion calls\n"

            string = string.format(self.name, str(self.CSP.MRV_FLAG), str(self.CSP.DH_FLAG), str(self.CSP.LCV_FLAG), str(self.CSP.AC3_FLAG), self.CSP.nodes_visited)

        return string

    def __solutionToStr(self):
        n = int(math.sqrt(len(self.solution)))
        s = int(math.sqrt(n)) # size of each sub-box

        string = "\n"

        for i in range(0, len(self.solution), 1):
            value = self.solution[i]
            if value < 10:
                value = str(value) + "  "
            else:
                value = str(value) + " "

            if (i + 1) % (n * s) == 0:
                string += value + "\n" + "-"*(3*n+2) + "\n"
            elif (i + 1) % n == 0:
                string += value + "\n"
            elif (i + 1) % s == 0:
                string += str(value) + "|"
            else:
                string += str(value)

        return string


def test1():
    board = [[3, 2, 0, 0, 0, 0, 0, 0, 7],
             [1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 6, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    p = SudokuCSP("Empty", board, True, False, False, False)
    print("")
    print("solving...")
    print(p)

def test2():
    board = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    p = SudokuCSP("sixteen", board, False, False, False, False, True)
    print("")
    print("solving...")
    print(p)
# test1()
test2()
