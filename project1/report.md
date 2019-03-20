# COMP30024 Artificial Intelligence Project 1 Report
team member: XuLin Yang(904904), Liguo Chen()

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

### a* search 
- time complexity
    - best case ∈ O(d) if we disregard the complexity of the heuristic calculation
    - average case ∈ O(b<sup>δd</sup>) (from lecture)
    - worst case ∈ O(b<sup>d</sup>) (because it is uniform cost search now)
- space complexity ∈ O(b<sup>δd</sup>) (because "keep all nodes in memory")
- completeness
    - Yes, as we are guaranteed in the specification "at least one winning sequence of actions exists"
- optimality
    - Yes, as long as h(s) <= h*(s) ∀ s ∈ state space

### heuristic function
- admissibility

## problem feature impact
### search tree
- branching factor
- depth 

### other features of the input impact on search algorithm
- time complexity 
- space complexity