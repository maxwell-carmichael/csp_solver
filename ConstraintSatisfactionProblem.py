# Maxwell Carmichael, 10/11/2020

from collections import deque
import copy
import time

# ASSUMPTION: constraints are binary and nothing more, and all variables need assignment.
class ConstraintSatisfactionProblem:
        # variables: set. domain: map (value -> set). constraints: map (pair -> possible variables)
    def __init__(self, neighbors, domain, constraints, MRV = True, DH = False, LCV = True, AC3 = True, print = True):
        self.neighbors = neighbors
        self.domain = domain
        self.constraints = constraints # (i,j) -> set of possible combos. i<j

        self.MRV_FLAG = MRV # minimum remaining values (when choosing variable)
        self.DH_FLAG = DH
        self.LCV_FLAG = LCV # least constraining value (when choosing value). Very useful in stopping recursion when a var has no more vals left to assign.
        self.AC3_FLAG = AC3 # inference
        self.PRINT_FLAG = print

        self.nodes_visited = 0

        # method which calls recursion
    def get_assignment(self):
        # t = time.time()
        solution = self.backtrack_recursion()
        # print("Time (s): " + str(time.time() - t))
        return solution

        # main method for finding solution
    def backtrack_recursion(self, unassigned_vars = None, assignment = None):
        self.nodes_visited += 1

        if assignment == None:
            self.nodes_visited = 1
            unassigned_vars = list(self.neighbors.keys()) # why is a list so much faster???
            assignment = [None] * len(self.neighbors)

        if self.PRINT_FLAG:
            print("")
            print("Current assignment: " + str(assignment))
            print("Current domain: " + str(self.domain))

        # every variable has an assignment, so check if it's good else stop going deeper.
        if not unassigned_vars:
            if self.is_valid(assignment):
                print("Valid solution found.")
                if self.PRINT_FLAG:
                    print("Nodes visited: " + str(self.nodes_visited))

                return assignment
            return None

        # save current domain to reset forward checking/inference
        # domain_save = copy.deepcopy(self.domain)
        domain_save = self.domain
        # next variable to assign
        variable = self.get_variable(unassigned_vars)
        if self.PRINT_FLAG:
            print("Now handling variable: " + str(variable))

        # values to consider, ordered if LCV is enabled
        values = self.get_values(variable, unassigned_vars)

        for value in values:
            if self.PRINT_FLAG:
                print("Choosing value: " + str(value))
            # assign the value
            assignment[variable] = value

            # constrain domain (forward check)
            self.domain = self.forward_check(variable, value)

            # run inference
            if self.AC3_FLAG and not self.ac3(): # False if our assignment causes failure
                self.domain = domain_save
                continue

            # recurse
            res = self.backtrack_recursion(unassigned_vars, assignment)

            # if not None, we found a solution!
            if res:
                return res

            if self.PRINT_FLAG:
                print("No solution for value " + str(value))

            # remove our forward checking and inference
            self.domain = domain_save

        # if we are here, there was nothing we could validly assign at this stage
        assignment[variable] = None
        unassigned_vars.append(variable)
        return None

        # returns the next variable to look at and removes it from unassigned_vars
    def get_variable(self, unassigned_vars):
        # MRV
        if self.MRV_FLAG:
            min_vars = set() # holds MRV, set in the case of ties
            mrv = None       # our current best MRV integer

            for var in unassigned_vars:
                if mrv is None or len(self.domain[var]) < mrv:
                    min_vars = set() # new best case, empty the set
                    min_vars.add(var)
                    mrv = len(self.domain[var])

                elif len(self.domain[var]) == mrv: # tie case, add it to the set
                    min_vars.add(var)

            # if DH is not enabled, pop a random minimum remaining values var
            if len(min_vars) == 1 or not self.DH_FLAG:
                min_var = min_vars.pop()
            # if DH is enabled, break the tie with it.
            else:
                min_var = self.get_variable_DegreeHeuristic(min_vars)

            unassigned_vars.remove(min_var)
            return min_var

        # Degree Heuristic
        elif self.DH_FLAG:
            return self.get_variable_DegreeHeuristic(unassigned_vars)

        # No heuristic
        else:
            return unassigned_vars.pop()

        # method in which DH operates
    def get_variable_DegreeHeuristic(self, unassigned_vars):
        min_var = None
        min_var_num = 0 # lowest degree found so far


        for var in unassigned_vars:
            num_neighbors = 0

            for neighbor in self.neighbors[var]:
                # if the neighbor is unassigned, increment it
                if neighbor in unassigned_vars and num_neighbors <= min_var_num:
                    if var < neighbor:
                        num_neighbors += 1 # len(self.constraints[(var, neighbor)])
                    else:
                        num_neighbors += 1 # len(self.constraints[(neighbor, var)])

                # we have a new best case, so update
                elif min_var is None or num_neighbors > min_var_num:
                    min_var = var
                    min_var_num = num_neighbors
                    # no need to keep going...
                    break

        unassigned_vars.remove(min_var)
        return min_var

        # returns a (potentially ordered) list of values to check
    def get_values(self, variable, unassigned_vars):
        if self.LCV_FLAG:
            # save some trouble if zero or one choice
            if len(self.domain[variable]) == 0 or len(self.domain[variable]) == 1:
                if self.PRINT_FLAG:
                    print("LCV Map for above variable: " + str(self.domain[variable]))
                return self.domain[variable]

            # obtain a map from variable to the number of constraints
            LCV_map = self.__value_map(variable, unassigned_vars)

            if self.PRINT_FLAG:
                print("LCV Map for above variable: " + str(LCV_map))
            value_list = list(self.domain[variable])
            value_list.sort(key = lambda v : LCV_map[v])

            return value_list

        else:
            return self.domain[variable]

        # helper function which returns the number of allowed combinations of
        # this value with the unassigned variables
    def __value_map(self, variable, unassigned_vars):
        # initialize map from value to number of constraints it is in
        value_map = {key: 0 for key in self.domain[variable]}

        # loop over all possible unassigned neighbors
        for i in unassigned_vars:
            if i < variable:
                var_pair = (i, variable)

                # find value tuples from i to variable
                for value in self.domain[variable]:
                    for ivalue in self.domain[i]:
                        val_pair = (ivalue, value)

                        # if this tuple is not in the constraint, that means value restricts ivalue
                        if var_pair in self.constraints and val_pair not in self.constraints[var_pair]:
                            value_map[value] += 1

            # given that there's no redundancies in constraints, need to check
            # this symmetrical case
            else:
                var_pair = (variable, i)

                # find value tuples from variable to i
                for value in self.domain[variable]:
                    for ivalue in self.domain[i]:
                        val_pair = (value, ivalue)

                        # if this tuple is not in the constraint, that means value restricts ivalue
                        if var_pair in self.constraints and val_pair not in self.constraints[var_pair]:
                            value_map[value] += 1

        return value_map

        # function which returns a domain limited by a variable assignment
    def forward_check(self, variable, value):
        rdomain = copy.deepcopy(self.domain)
        rdomain[variable] = { value }

        # loop over all constraints involving variable
        # I assume worst case, there is a contraint between two variables which are not neighbors
        for i in range(0, len(self.neighbors), 1):
            # identify pair in self.constraints
            if i < variable:
                var_pair = (i, variable)

                # consider each value pair. if it's not in the constraint, remove
                # the value from the domain.
                for ivalue in set(rdomain[i]):
                    val_pair = (ivalue, value)

                    if var_pair in self.constraints and val_pair not in self.constraints[var_pair]:
                        if self.PRINT_FLAG:
                            print("Removing " + str(val_pair) + " from " + str(var_pair))
                        rdomain[i].remove(ivalue)

            elif i == variable:
                continue

            else:
                var_pair = (variable, i)

                # consider each value pair. if it's not in the constraint, remove
                # the value from the domain.
                for ivalue in set(rdomain[i]):
                    val_pair = (value, ivalue)

                    if var_pair in self.constraints and val_pair not in self.constraints[var_pair]:
                        if self.PRINT_FLAG:
                            print("Removing " + str(ivalue) + " from " + str(i))
                        rdomain[i].remove(ivalue)

        return rdomain

    def ac3(self):
        queue = deque()

        for key in self.constraints:
            queue.append(key)
            queue.append((key[1], key[0]))

        while queue:
            arc = queue.popleft()
            vari = arc[0]
            varj = arc[1]

            if self.revise(vari, varj):
                # if no more domain
                if not self.domain[vari]:
                    return False

                for vark in self.neighbors[vari]:
                    queue.append((vark, vari))

        return True

    def revise(self, vari, varj):
        revised = False

        for ivalue in set(self.domain[vari]):
            if not self.__satisfiable(vari, varj, ivalue):
                self.domain[vari].remove(ivalue)
                revised = True

        return revised

    # helper function. if there is a jvalue in domain of varj such that (vari, varj)
    # has a good relation (ivalue, jvalue), then returns true
    def __satisfiable(self, vari, varj, ivalue):
        if vari < varj:
            var_pair = (vari, varj)

            for jvalue in self.domain[varj]:
                val_pair = (ivalue, jvalue)

                # if there exists a jvalue which satisfies constraint...
                if var_pair in self.constraints and val_pair in self.constraints[var_pair]:
                    return True
        else:
            var_pair = (varj, vari)

            for jvalue in self.domain[varj]:
                val_pair = (jvalue, ivalue)

                # if there exists a jvalue which satisfies constraint...
                if var_pair in self.constraints and val_pair in self.constraints[var_pair]:
                    return True
        # no satisfiable found...
        return False

    def is_valid(self, assignment):
        # loop over all variables
        for i in range(0, len(assignment) - 1, 1):
            # loop over all pairs
            for j in range(i + 1, len(assignment), 1):
                pair = (assignment[i], assignment[j])

                if (i, j) in self.constraints and pair not in self.constraints[(i, j)]:
                    return False

        return True

def test1():
    neighbors = { 0 : {2}, 1 : {2}, 2 : {0, 1} }
    colors = { 0, 1 }
    domain = { 0 : colors.copy(), 1 : colors.copy(), 2: colors.copy() }
    colorsneq = { (0,1), (1,0) }
    constraints = { (0,2) : set(colorsneq), (1,2) : set(colorsneq) }

    problem1 = ConstraintSatisfactionProblem(neighbors, domain, constraints, MRV = True, LCV = False, AC3 = False)
    assignment = problem1.get_assignment()
    print(assignment)
    # assignment = problem1.get_assignment()
    # print(assignment)

# australia
def test2():
    variables = [0,1,2,3,4,5,6]
    neighbors = { 0 : {1, 2}, 1 : {0, 2, 3}, 2 : {0, 1, 3, 4, 5}, 3 : {1, 2, 4},
                    4 : {2, 3, 5}, 5 : {2, 4}, 6 : {}}
    colors = { 0, 1, 2 }
    domain = { 0 : colors.copy(), 1 : colors.copy(), 2: colors.copy(), 3: colors.copy(), 4: colors.copy(), 5: colors.copy(), 6: colors.copy() }
    colorsneq = { (0,1), (0,2), (1,0), (1,2), (2,0), (2,1) }
    constraints = { (0,1) : set(colorsneq), (0,2) : set(colorsneq), (1,2) : set(colorsneq), (1,3) : set(colorsneq), (2,3) : set(colorsneq), (2,4) : set(colorsneq), (2,5) : set(colorsneq), (3,4) : set(colorsneq), (4,5) : set(colorsneq) }
    # the following avoids redundancies:
    # 0 WA -> NT, SA
    # 1 NT -> Q, SA
    # 2 SA -> Q, NSW, Victoria
    # 3 Q -> NSW
    # 4 NSW -> Victoria
    # 5 Victoria ->
    # 6 Tasmania ->

    problem2 = ConstraintSatisfactionProblem(neighbors, domain, constraints, MRV = True, LCV = True, AC3 = True)
    assignment = problem2.get_assignment()
    print(assignment)

# test2()
# test2()
