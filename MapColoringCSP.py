# Maxwell Carmichael 10/12/2020

from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem

class MapColoringCSP:
    def __init__(self, name, neighborgraph, MRV = True, DH = False, LCV = True, AC3 = True, print = False):
        self.name = name

        self.strmap = self.__strmap(neighborgraph) # int -> str
        self.inverse_strmap = {value: key for key, value in self.strmap.items()} # str -> int
        self.colormap = self.__colormap() # int -> str
        self.neighbors = self.__neighborgraphToInt(neighborgraph)

        # construct domain
        domain = self.__domainmap()
        # construct constraints
        constraints = self.__constraintmap()

        self.CSP = ConstraintSatisfactionProblem(self.neighbors, domain, constraints, MRV, DH, LCV, AC3, print)
        self.solution = self.__find_solution()

    def __find_solution(self):
        return self.CSP.get_assignment()

    def __strmap(self, neighborgraph):
        strset = list(neighborgraph.keys()) # list for replicability
        # random.shuffle(strset)
        # print(strset)

        strmap = {key: strset.pop() for key in range(0, len(strset), 1)}
        # print(strmap)


        return strmap

    def __colormap(self, numcolors = 3):
        colorset = [ "Blue", "Green", "Red"] # list for replicability

        colormap = {key: colorset.pop() for key in range(0, len(colorset), 1)}

        # print(colormap)
        return colormap

    def __neighborgraphToInt(self, neighborgraph):
        neighbors = {}

        for variable in neighborgraph:
            vneighbors = neighborgraph[variable]

            # if there is an error, it will be here. ensure the neighbor graph is valid.
            intneighbors = set()
            for neighbor in vneighbors:
                if neighbor in self.inverse_strmap:
                    intneighbors.add(self.inverse_strmap[neighbor])
                else:
                    print("Error with neighbors of " + variable)
                    intneighbors.add(self.inverse_strmap[neighbor])

            # { self.inverse_strmap[neighbor] for neighbor in vneighbors }


            neighbors[self.inverse_strmap[variable]] = intneighbors

        # print(neighbors)
        return neighbors


    def __domainmap(self):
        domain = {}

        for variable in self.neighbors:
            domain[variable] = set(self.colormap.keys())


        # print(domain)
        return domain

    def __constraintmap(self):
        colorsneq = set()

        # each relation has the same constraint
        for color1 in self.colormap:
            for color2 in self.colormap:
                if color1 != color2:
                    colorsneq.add((color1, color2))

        constraints = {}
        for i in range(0, len(self.neighbors), 1):
            for j in self.neighbors[i]:
                # neighbors is undirected, so don't add duplicate constraints
                if i < j:
                    constraints[(i,j)] = colorsneq.copy()

        # print(constraints)
        return constraints

    def __str__(self):
        string = "----\n"
        string += "Map Coloring CSP Problem: {:s}\n"
        string += "Heuristics/Inference:  MRV: {:s}. DH: {:s} LCV: {:s}. AC3: {:s}\n"

        if self.solution:
            string += "Number of recursion calls: {:d}\n"
            string += "Solution: {:s}\n"

            string = string.format(self.name, str(self.CSP.MRV_FLAG), str(self.CSP.DH_FLAG), str(self.CSP.LCV_FLAG), str(self.CSP.AC3_FLAG), self.CSP.nodes_visited, str(self.__solutionToStr()))
        else:
            string += "No solution found after {:d} recursion calls\n"

            string = string.format(self.name, str(self.CSP.MRV_FLAG), str(self.CSP.DH_FLAG), str(self.CSP.LCV_FLAG), str(self.CSP.AC3_FLAG), self.CSP.nodes_visited)

        return string

        # returns a dictionary
    def __solutionToStr(self):
        coloredInMap = {}

        # i reverse the map to match the input format
        for i in range(len(self.solution)-1, -1, -1):
            coloredInMap[self.strmap[i]] = self.colormap[self.solution[i]]

        return coloredInMap

def test1():
    neighborhood = { "VT" : {"NH"}, "NH" : {"VT", "ME"}, "ME" : {"NH"} }
    p = MapColoringCSP("Northeast", neighborhood)
    print("")
    print("solving...")
    print(p)

def test2():
    neighborhood = { "WA" : {"NT", "SA"}, "NT" : {"WA", "SA", "Q"}, "SA" : {"WA", "NT", "Q", "NSW", "V"}, "Q" : {"NT", "SA", "NSW"}, "NSW" : {"Q", "SA", "V"}, "V" : {"SA", "NSW"}, "T" : {}}
    p = MapColoringCSP("Australia", neighborhood, MRV = False, LCV = False, AC3 = False, print = False)
    print("")
    print("solving...")
    print(p)

def test3():
    neighborhood = { "YUK" : {"NWT", "BC"}, "NWT" : {"YUK", "BC", "AB", "SK", "NUN"}, "NUN" : {"NWT", "MB"}, "BC" : {"YUK", "NWT", "AB"}, "AB" : {"BC", "NWT", "SK"}, "SK" : {"AB", "NWT", "MB"}, "MB" : {"SK", "NUN", "ON"}, "ON" : {"MB", "QC"}, "QC" : {"ON", "NL", "NB"}, "NL" : {"QC"}, "NB" : {"QC"} }
    p = MapColoringCSP("Canada", neighborhood, MRV = True, DH = True, LCV = True, AC3 = False)
    print("")
    print("solving...")
    print(p)
#
# test2()
test3()
