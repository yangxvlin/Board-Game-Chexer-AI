# ai-project
- COMP30024 Artificial Intelligence
- team member: XuLin Yang(笨比队友), Liguo Chen(拖油瓶)
- team name:   deep ♂ dark ♂ fantastic ♂ boys ♂ next ♂ door

## Chexers
Chexers is a three-player hexagonal turn-based race game. Test the loyalty of your band of two faced checker pieces as you charge them through a twisting and treacherous battleground. Will all your pieces stay true to your cause? Can you earn yourself some new followers in the chaos? To win this tumultuous chase, you must double-cross and triple-cross your way across the finish line before your opponents--three, two, one... go!

## Project1 Searching
In this first part of the project, we will play a single-player variant of the game of Chexers. Before you read this specification, please make sure you have carefully read the entire `Rules for the Game of Chexers' document.

The aims for Project Part A are for you and your project partner to (1) refresh and extend your Python programming skills, (2) explore some of the new algorithms we have met in lectures so far, and (3) become more familiar with some core mechanics of Chexers. This is also a chance for you to invest some time developing fundamental Python tools for working with the game: some of the functions and classes you create now may be helpful later (when you are building your game-playing program for Project Part B).

## Project1 Mark & Feedback

================================================================================
COMP30024 Artificial Intelligence - Project Part A - Marks and Feedback

================================================================================

Team: liguoc-xuliny-deep_dark_fantastic_boys_next_door

### Marks:

--------------------------

Report:       2.0    / 2.0

Code quality: 2.0    / 2.0

Auto-testing: 4.0    / 4.0

--------------------------

Total mark:   8.0    / 8.0

--------------------------

### Feedback:

- Feedback on report:

  Your representation of the problem is natural and sensible - well done!
  
  A very interesting approach to designing your heuristic. It's nice to see your
  discussion that a complex heuristic like Dijkstra can work for this problem,
  since h(n) is so good that A* doesn't need to expand too many nodes. The
  relaxation to allow a piece to jump at any time is an elegant way of making
  the heuristic admissible.
  
  Your empirical approach to determining the factors that influence the space/
  time complexity is excellent - the graphs clearly display many of the features
  we'd expect from the theoretical time/space complexity of A*.
  

## Project2

## Project2 Mark & Feedback

================================================================================

COMP30024 Artificial Intelligence - Project Part B - Marks and Feedback

================================================================================

Team: liguoc-xuliny-deep_dark_fantastic_boys_next_door

### Marks:

---------------------------

Code quality:  4.00 /  4.00  
Correctness:   4.00 /  4.00  
Performance:   6.50 /  7.00  
Creativity:    7.00 /  7.00  

---------------------------

Total mark:   21.50 / 22.00  

---------------------------

### Feedback:

- Feedback on code quality, correctness, and performance:

  Results from test games against benchmark opponents:

  ---------------------

  opponent    win ratio  

  ---------------------

  random         100.0%  
  greedy          50.0%  
  searching       62.5%
  (email Matt for logs)  

  ---------------------
 
 - Feedback on creativity:  
 Well done for the awesome number of substantial improvements you've adopted over the basic techniques included in lectures, and for your impressively creative insights into the game of Chexers itself, resulting in a highly dynamic and highly effective playing strategy. Super great!
 