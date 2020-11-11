Maxwell Carmichael

### Introduction
In this project, I created a general-purpose constraint satisfaction problem solver as well as three specific constraint satisfaction problems: Map coloring, circuit board, and sudoku.

### General-Purpose CSP
I began this assignment by creating a ConstraintSatisfactionProblem class, which, given a graph of integer variables, domains, and constraints, could return a list of values, with indices being the variables. The bulk of the backtracking algorithm is in backtrack_recursion, which assigns a value to an unassigned variable with each level of recursion. It chooses the variable to assign by calling get_variable, and determines the order of values to assign by calling get_values. I decided that my algorithm would always forward check, so that any value chosen from any domain would always be consistent. The other option would be to check if a value is consistent as it's chosen, but this yields the same result as - and in much slower time than - forward checking. The forward_check method does this by returning a new domain - I save the old domain in a variable "domain_save" so that any modifications to the domain (in either forward_check or AC3) can be quickly undoed. Another implementation decision I made was that my constraint map, which maps tuples of variables in the form (i,j) to a set of allowed value-pairs, would always have i<j. This saves space in the constraint map.

When initializing, you have the option of which heuristics to use. If you initialize with Minimum Remaining Values (MRV) or Degree Heuristic (DH) (if both are selected, the algorithm will use DH as a tie-breaker), the get_variable method will employ the heuristic to choose the next variable. Otherwise, it will choose effectively a random variable from the unassigned variables. If you initialize with Least Constraining Value (LCV), the get_values method will find which values eliminate the least number of values from its variable's neighbors and return a list of values ordered in such a way. Otherwise (no heuristic), it will just return the variable's domain as it is already ordered.

Lastly, you have the option to using inference by employing AC3, which I implemented according to textbook pseudocode. The __satisfiable helper method takes a variable, its neighbor, and a value for the variable, and checks if the neighbor has any values which could be consistent with the variable's value.

### MapColoringCSP
Implementing MapColoringCSP was relatively straightforward. The goal here was, given a map from region names to a set of adjacent regions, generate an undirected graph, domains, and constraints which the general-purpose CSP class can solve (and also be able to print the solution in a digestible way). To do so, first I generated maps from integer (0 to len(map)) to string and the inverse map of that. Then, using this inverse map, essentially converted the graph of region names to a graph of integers representing each region. The domain was easy - each variable in the integer graph has a domain of three colors. Likewise, the constraints were straightforward - each edge in the graph could take six possible color combinations: (r,g), (r,b), (g,r), (g,b), (b,r), (b,g). We can then find a solution (or return no solution) by passing this information into the general-purpose CSP class. I use the maps from integer to string to convert the solution in a readable way.

To print a solution, just print the MapColoringCSP object. The constructor finds the solution.

### CircuitBoardCSP
Implementing CircuitBoardCSP was slightly more of a challenge than MapColoringCSP. The parameter of this problem is a map from piece name (a character) to a tuple representing its length and height. You also need to specify the nxm dimensions of the board. Like MapColoringCSP, I first generated maps from integer to character and the inverse map of that. Generating the undirected graph was easy - every piece is a neighbor to every other piece (in that the locations of any one piece limit the locations of any other piece). Generating the domain was also not difficult - for any piece, its possible values (values are the bottom-left corner of the piece) is the set of all coordinates of the nxm board, minus the coordinates that would cause the piece to be over the top or right edge of the board. The constraints, on the other hand, are a little less straightforward. First, we need to loop over all the variable pairs. Then we have to look at the domain of each variable in the pair and find which pairs of values are valid. For a pair of values to be invalid, it must cause the squares to overlap. Thus, only add the value pairs to the constraint between two variables if the values do not cause the pieces to overlap. Now that we have all our information, we can find a solution (or return no solution) by passing this information into the general-purpose CSP class. I use the maps from integer to character to convert the solution in a readable way (ASCII art).

##### CircuitBoardCSP Discussion
Given a component of width w and height h, on a circuit board of width n and height m, and given that the value of the component is its lower left corner, the domain would be all coordinate pairs within the rectangle: (0, 0), (0, m-h), (n-w, m-h), (n-w, 0). Anything on the board and not within this rectangle would cause the piece to overlap the top and/or the right edges.

Below the solution board to the assignment's example problem is the set of tuple pairs, the left representing piece 'b' and the right representing piece 'a', such that the two pieces do not overlap on a 10x3 board. In my solution, I have 'b' at (3,0) and 'a' at (0,0), and you can find this pair in the constraints.

```
.eeeeeeecc
aaabbbbbcc
aaabbbbbcc
```

{((5, 1), (0, 1)), ((0, 1), (7, 1)), ((0, 1), (7, 0)), ((1, 0), (6, 1)), ((5, 0), (2, 1)), ((5, 1), (2, 0)), ((4, 0), (1, 0)), ((2, 1), (7, 0)), ((4, 1), (1, 1)), ((0, 0), (5, 1)), ((0, 0), (6, 0)), ((4, 0), (1, 1)), ((2, 0), (7, 0)), ((5, 0), (1, 1)), ((0, 0), (7, 1)), ((5, 1), (0, 0)), ((1, 1), (6, 1)), ((3, 0), (0, 1)), ((0, 1), (6, 1)), ((0, 1), (6, 0)), ((4, 0), (0, 0)), ((1, 0), (7, 1)), ((0, 1), (5, 0)), ((1, 0), (7, 0)), ((4, 0), (0, 1)), ((5, 0), (0, 1)), ((4, 1), (1, 0)), ((2, 1), (7, 1)), ((5, 0), (1, 0)), ((0, 0), (6, 1)), ((2, 0), (7, 1)), ((5, 0), (2, 0)), **((3, 0), (0, 0))**, ((0, 1), (5, 1)), ((5, 1), (2, 1)), ((0, 0), (5, 0)), ((5, 1), (1, 0)), ((1, 1), (7, 1)), ((1, 1), (7, 0)), ((3, 1), (0, 0)), ((5, 1), (1, 1)), ((1, 0), (6, 0)), ((4, 1), (0, 0)), ((3, 1), (0, 1)), ((5, 0), (0, 0)), ((4, 1), (0, 1)), ((0, 0), (7, 0)), ((1, 1), (6, 0))}

My code converts the piece names to integer values and likewise finds the domains for all these integer values based on the passed-in size of the piece and the constraints for all pairs of these integer values. I do not actually convert the coordinate pairs into integers here, as these are purely used in the constraint and domain. Tuples are as efficient as using integers, as both are immutable. Only variables, not values, necessarily need to be converted to integers for ConstraintSatisfactionProblem to work properly.


### SudokuCSP
This extra-credit class can solve 4x4 and 9x9 sudoku problems. The input is a 2d nxn array with integer values between 0 and n (0 indicates that the spot is empty/unassigned). The undirect graph has the neighbors to each variable be other variables which share a row, column, and subsquare with the variable. The domain for each variable is all numbers 1-n, unless the spot already has an assigned number, in which the domain for that spot is just the inputted value. Any two variables which are neighbors share a constraint, which is all pairwise combinations of values 1-n besides duplicates. With this information, we can find a solution (or return no solution) by passing this information into the general-purpose CSP class. I convert the resulting list into an easily readable sudoku board (ASCII art).

### Analysis
```
Map Coloring CSP Problem: Australia
Heuristics/Inference:  MRV: False. DH: False LCV: False. AC3: False
Number of recursion calls: 8
Solution: {'WA': 'Red', 'NT': 'Green', 'SA': 'Blue', 'Q': 'Red',
'NSW': 'Green', 'V': 'Red', 'T': 'Red'}
```
My MapColoringCSP algorithm, even with all heuristics turned off, performs the same amount of recursion calls as with all heuristics on. I am sure there are more constrained cases where heuristics would be of more benefit, but there is no improvement seen when running the algorithm on either of my Australia and Canada test cases.

However, for testing purposes, I limited the domain to only include two colors - a problem with no solution in many cases. The following table represents how many recursion calls on the Canada problem before it terminates, having found no solution.

| MRV   | DH    | LCV   | AC3   | Visited |
|-------|-------|-------|-------|---------|
| False | False | False | False | 21      |
| False | False | False | True  | 1       |
| False | False | True  | False | 21      |
| False | False | True  | True  | 1       |
| False | True  | False | False | 38      |
| False | True  | False | True  | 1       |
| False | True  | True  | False | 38      |
| False | True  | True  | True  | 1       |
| True  | False | False | False | 17      |
| True  | False | False | True  | 1       |
| True  | False | True  | False | 17      |
| True  | False | True  | True  | 1       |
| True  | True  | False | False | 5       |
| True  | True  | False | True  | 1       |
| True  | True  | True  | False | 5       |
| True  | True  | True  | True  | 1       |

**Table 1.** Number of recursion calls for various combinations of heuristics.

This table is as expected. Whenever AC-3 is run, the algorithm detects the early failure relatively quickly - since there are three regions (pairwise) adjacent to one another (more broadly, there exists an odd cycle), AC-3 will see immediately that at least one variable will have an empty domain upon the first assignment, so we will terminate without having even entered recursion. As Figure 1 shows, LCV has no impact on how quickly the program will find no solution. This makes sense as this only impacts the order of values chosen, and we will still recurse through all the values anyway. I think it makes sense that Degree Heuristic alone slows down the algorithm. Degree Heuristic will effectively pick variables with the most unassigned neighbors, and so it increases the chance of picking variables that have no assigned neighbors. This reduces pruning since it increases the odds we choose a variable that has a domain greater than zero (when AC-3 is off, we stop recursion only upon selecting a variable with no consistent remaining domain values). By the same logic, it makes sense that MRV increases pruning, as it guarantees we choose a variable with no consistent remaining values. There is also a significant improvement when combining MRV and Degree Heuristic. Degree Heuristic guarantees we choose Northwest Territory first, thus limiting the domains of its many neighbors through forward checking. Then, MRV selects one of the neighbors, which has a decent likelihood of making the domain of another unassigned province empty, enabling MRV to prune in the next recursion call.

```
Circuit Board CSP Problem: example from assignment
Heuristics/Inference:  MRV: False. DH False. LCV: False. AC3: False
Number of recursion calls: 12
Solution:
{'a': (0, 0), 'b': (3, 0), 'c': (8, 0), 'e': (1, 2)}

.eeeeeeecc
aaabbbbbcc
aaabbbbbcc
```

Let's now look at CircuitBoardCSP's performance solving the following puzzle under various heuristics:
```
ffffjjjjjjaaaee
ffffjjjjjjaaaee
ffffjjjjjjaaaee
ccccjjjjjjaaaee
dddljjjjjjaaaee
dddojjjjjjaaabi
dddqqqqqqqqkkbi
dddqqqqqqqqkkbi
dddhhhmmmmmkkbi
dddhhhmmmmmkkbi
dddhhhmmmmmrrri
dddhhhmmmmmrrri
dddhhhnnnnnrrri
dddgggggggggggi
dddpppssssssssi
```


| MRV   | DH    | LCV   | AC3   | Visited | Time    |
|-------|-------|-------|-------|---------|---------|
| False | False | False | False | 149491  | 80.4560 |
| False | False | False | True  | 20      | 0.2125  |
| False | False | True  | False | 1621    | 0.5914  |
| False | False | True  | True  | 53      | 0.1616  |
| False | True  | False | False | N/A     | 300+    |
| False | True  | False | True  | 51      | 0.2184  |
| False | True  | True  | False | 38528   | 9.1186  |
| False | True  | True  | True  | 53      | 0.1396  |
| True  | False | False | False | 79      | 0.0623  |
| True  | False | False | True  | 14      | 0.0468  |
| True  | False | True  | False | 14      | 0.0370  |
| True  | False | True  | True  | 15      | 0.0758  |
| True  | True  | False | False | 79      | 0.0349  |
| True  | True  | False | True  | 14      | 0.0768  |
| True  | True  | True  | False | 14      | 0.0369  |
| True  | True  | True  | True  | 15      | 0.0758  |

**Table 2.** Number of recursion calls for various combinations of heuristics for CircuitBoardCSP.

The first thing to note is the apparent ineffectiveness of the degree heuristic. Compare the runtime with DH and LCV enabled to the runtime with only LCV enabled - a factor of about 18x slower. As well, Degree Heuristic visits many more nodes before it arrives at a solution. Perhaps it is not a good heuristic to use on CircuitBoardCSP, as every piece is a neighbor to itself. However, in the case where it is used as a tiebreaker (with MRV enabled), I obtain some of the fastest runtimes, less than 40 ms. (I am not confident why this is. You would think that DH would not be useful in breaking any ties, but it noticeably reduces the runtime. Perhaps it's a quirk of the implementation.)

AC3 alone is shown to be incredibly effective, reducing the number of nodes visited (recursion calls) from 149491 to 20. LCV alone does not reduce runtime as well as AC3, but it has a much lower ratio of runtime to recursion calls. MRV alone has more recursion calls than AC3 alone but is about three times faster.

Interestingly, AC3 significantly improves runtime when combined with other heuristics, but only to a certain point. In the cases where we combine MRV with DH and/or LCV, AC3 actually about doubles the runtime (but still has a runtime under 80ms nonetheless). This is probably an indicator that the heuristics do a lot of work on their own (besides DH), and that combining them all is actually rather unnecessary and can take computational power. I seem to get the best results when using MRV in combination with LCV and/or DH, with no AC-3. But of course it is important to remember that these observations are very problem dependent, and the important part is that the heuristics significantly improved upon the 80 second runtime.

Project for CS76 - Artificial Intelligence
Professor Alberto Quattrini Li
PA4: Constraint Satisfaction