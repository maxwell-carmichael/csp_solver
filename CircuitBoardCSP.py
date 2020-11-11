from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem

class CircuitBoardCSP:
    # piecemap: {char: (width, height))
    def __init__(self, name, piecemap, n, m, MRV = True, DH = False, LCV = True, AC3 = True, print = False):
        self.name = name

        self.n = n
        self.m = m

        self.piecemap = piecemap # char -> (w,h)
        self.charmap = self.__charmap() # int -> char
        self.inverse_charmap = {value: key for key, value in self.charmap.items()} # char -> int

        # self.colormap = self.__colormap() # int -> str
        self.neighbors = self.__genCompleteGraph()

        # construct domain
        domain = self.__domainmap(n, m)
        # construct constraints
        constraints = self.__constraintmap(domain)

        self.CSP = ConstraintSatisfactionProblem(self.neighbors, domain, constraints, MRV, DH, LCV, AC3, print)
        self.solution = self.__find_solution()

    def __find_solution(self):
        return self.CSP.get_assignment()

    def __charmap(self):
        charset = list(self.piecemap.keys()) # list for replicability
        # random.shuffle(strset)
        # print(strset)

        charmap = {key: charset.pop() for key in range(0, len(charset), 1)}

        # print(charmap)
        return charmap

        # everything is a neighbor to everything
    def __genCompleteGraph(self):
        completeGraph = {}

        pieces = self.charmap.keys()

        for piece in self.charmap:
            neighbors = set(pieces)
            neighbors.remove(piece)
            completeGraph[piece] = neighbors

        # print(completeGraph)
        return completeGraph

    def __domainmap(self, n, m):
        domain = {}

        for variable in self.neighbors:
            possibleCoordinates = set()

            length = self.piecemap[self.charmap[variable]][0]
            height = self.piecemap[self.charmap[variable]][1]

            # only possible locations are those which fit in the n x m space
            for x in range(0, n - length + 1, 1):
                for y in range(0, m - height + 1, 1):
                    possibleCoordinates.add((x,y))

            domain[variable] = possibleCoordinates

        # print(domain)
        return domain

    def __constraintmap(self, domain):
        # idea: we set a piece at coordinate (x,y). That means no other piece can be between (x,y) and (x+length,y+height). so, (0,0)
        constraints = {}

        # find out constraints for (i,j) pair in complete graph
        for vari in range(0, len(self.neighbors) - 1, 1):
            for varj in range(vari + 1, len(self.neighbors), 1):
                var_pair = (vari,varj)
                constraints[var_pair] = self.__genCombos(domain, vari, varj)

        # print(constraints)

        return constraints

    def __genCombos(self, domain, vari, varj):
        possibleCombos = set()

        lengthi = self.piecemap[self.charmap[vari]][0]
        heighti = self.piecemap[self.charmap[vari]][1]
        lengthj = self.piecemap[self.charmap[varj]][0]
        heightj = self.piecemap[self.charmap[varj]][1]

        # DEFINITELY MORE EFFICIENT WAY TO IMPLEMENT THIS!!!s

        # loop over the domain of vari and domain of varj and if they do not
        # overlap, add them to possible combos
        for coordi in domain[vari]:
            for coordj in domain[varj]:
                # vari on other side of varj
                if coordi[0] + lengthi - 1 < coordj[0] or coordj[0] + lengthj - 1 < coordi[0]:
                    possibleCombos.add((coordi,coordj))
                # vari on top/below varj
                elif coordi[1] + heighti - 1 < coordj[1] or coordj[1] + heightj - 1 < coordi[1]:
                    possibleCombos.add((coordi,coordj))

        return possibleCombos

    def __str__(self):
        string = "----\n"
        string += "Circuit Board CSP Problem: {:s}\n"
        string += "Heuristics/Inference:  MRV: {:s}. DH {:s}. LCV: {:s}. AC3: {:s}\n"

        if self.solution:
            string += "Number of recursion calls: {:d}\n"
            string += "Solution:\n"
            string += "{:s}\n"

            string = string.format(self.name, str(self.CSP.MRV_FLAG), str(self.CSP.DH_FLAG), str(self.CSP.LCV_FLAG), str(self.CSP.AC3_FLAG), self.CSP.nodes_visited, str(self.__solutionToStr()))
        else:
            string += "No solution found after {:d} recursion calls\n"

            string = string.format(self.name, str(self.CSP.MRV_FLAG), str(self.CSP.DH_FLAG), str(self.CSP.LCV_FLAG), str(self.CSP.AC3_FLAG), self.CSP.nodes_visited)

        return string

        # returns a dictionary
    def __solutionToStr(self):
        labeled = {}

        # i reverse the map to match the input format
        for i in range(len(self.solution)-1, -1, -1):
            labeled[self.charmap[i]] = self.solution[i]

        string = str(labeled) + "\n"

        ASCII = [None]*(self.n*self.m)

        for i in range(0, len(self.solution), 1):
            length = self.piecemap[self.charmap[i]][0]
            height = self.piecemap[self.charmap[i]][1]
            bottom_left = self.solution[i]

            for x in range(bottom_left[0], bottom_left[0] + length, 1):
                for y in range(bottom_left[1], bottom_left[1] + height, 1):
                    ASCII[self.__pointToIndex((x,y))] = self.charmap[i]

        for i in range(0, len(ASCII), 1):
            if i % self.n == 0:
                string += "\n"

            if ASCII[i] is None:
                string += "."
            else:
                string += ASCII[i]

        return string

    def __pointToIndex(self, coord):
        return coord[0] + (self.m - coord[1] - 1) * self.n


# 3x3, with a 1x1 piece and 2x2 piece
def test1():
    piecemap = { 'a' : (1,1), 'b' : (2,2)}
    p = CircuitBoardCSP("3x3 easy", piecemap, 3, 3)

    print("")
    print("solving...")
    print(p)

def test2():
    piecemap = { 'a' : (3,2), 'b' : (5,2), 'c' : (2,3), 'e' : (7,1)}
    p = CircuitBoardCSP("example from assignment", piecemap, 10, 3, False, False, False, False)

    print("")
    print("solving...")
    print(p)

def test3():
    piecemap = { 'a' : (5,5),  'c' : (5,3), 'd' : (1,2), 'e' : (2,2), 'f' : (7,2), 'g' : (1,1), 'h' : (3,1), 'i' : (3,1) }

    p = CircuitBoardCSP("example from assignment", piecemap, 10, 7, False, True, False, True)

    print("")
    print("solving...")
    print(p)

def test4():
    piecemap = { 'a' : (2,3), 'b' : (2,1), 'c' : (1,3), 'd' : (3,1), 'f' : (1,1) }

    p = CircuitBoardCSP("example from assignment", piecemap, 4, 4, False, True, False, True)

    print("")
    print("solving...")
    print(p)

def test4():
    piecemap = { 'a' : (3,6), 'b' : (1,5), 'd' : (3,11), 'e' : (2,5), 'h' : (3,5), 'i' : (1,10), 'j' : (6,6), 'k' : (2,4), 'l' : (1,1), 'm' : (5,4), 'n' : (5,1), 'o' : (1,1), 'p' : (3,1)}

    p = CircuitBoardCSP("15x11", piecemap, 15, 11, True, False, False, False, False)

    print("")
    print("solving...")
    print(p)

# test2()
# test3()
test4()
