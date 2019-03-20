# COMP30024 Artificial Intelligence Project 1 Report
<p align="right"/>team member: XuLin Yang(904904), Liguo Chen()

## search problem formulation
- _**State**_: player pieces and obstacle pieces' location on board
- _**Action**_: player can move, jump or exit one player piece per turn defined in specification
- _**Goal Test**_: no player's piece on board
- _**Path Cost**_: 1 cost per action

## search algorithms
### terminology
- _**b**_: branching factor for search tree
- _**d**_: length for the solution path in search tree
- _**δ**_: relative error in heuristic = |h*(s) - h(s)|
- _**dist<sub>SLD</sub>()**_: straight line distance in hexe
- _**h()**_:  heuristic function

### a* search 
- time complexity
    - best case ∈ O(d) if we disregard the complexity of the heuristic calculation
    - average case ∈ O(b<sup>δd</sup>) (from lecture)
    - worst case ∈ O(b<sup>d</sup>) (because it is uniform cost search now)
- space complexity ∈ O(b<sup>δd</sup>) (because "keep all nodes in memory")
- completeness
    - Yes, as we are guaranteed in the specification "at least one winning sequence of actions exists"
- optimality
    - Yes, as long as h(s) ≤ h*(s) ∀ s ∈ state space

### heuristic function
- h(state) = $\sum_{piece ∈ player} (\lceil \frac{dist_{SLD} (piece)}{2}  \rceil + 1)​$
- admissibility:  
  - Discussing Red player is similar for Green and Blue player as they are parallel cases. So we can only discuss Red player case at here.  
    Fastest path for a single piece on board to reach in goal hexe is that the piece can jump to goal hexe as much as possible (optionally plus one move if next to the goal hexe) and then exit.  
    i.e. h(piece to goal hexe) = $\lceil{\frac{number \, of \, move \, action}{2}}\rceil$ as one jump is considered as two move actions. Where #move action = SLD distance  
    ∵# jump action (optionally plus one move if next the goal hexe) is the ideal(lower bound of) length of path for the piece to reach the goal hexe as described above  
    ∴h\*(piece) ≥ h(piece to goal hexe) + 1. Note: plus 1 for exit action  
    ∴ h\*(state) ≥ $\sum_{piece ∈ player}$h(piece) = $\sum_{piece ∈ player} (\lceil \frac{dist_{SLD} (piece)}{2}  \rceil + 1)​$

## problem feature impact
### search tree
- branching factor
- depth 

### other features of the input impact on search algorithm
- time complexity 
- space complexity