# ai-project
- COMP30024 Artificial Intelligence
- team member: XuLin Yang(笨比队友), Liguo Chen(拖油瓶)
- team name:   deep ♂ dark ♂ fantastic ♂ boys ♂ next ♂ door

## Chexers
Chexers is a three-player hexagonal turn-based race game. Test the loyalty of your band of two faced checker pieces as you charge them through a twisting and treacherous battleground. Will all your pieces stay true to your cause? Can you earn yourself some new followers in the chaos? To win this tumultuous chase, you must double-cross and triple-cross your way across the finish line before your opponents--three, two, one... go!

## Project1 Searching
In this first part of the project, we will play a single-player variant of the game of Chexers. Before you read this specification, please make sure you have carefully read the entire `Rules for the Game of Chexers' document.

The aims for Project Part A are for you and your project partner to (1) refresh and extend your Python programming skills, (2) explore some of the new algorithms we have met in lectures so far, and (3) become more familiar with some core mechanics of Chexers. This is also a chance for you to invest some time developing fundamental Python tools for working with the game: some of the functions and classes you create now may be helpful later (when you are building your game-playing program for Project Part B).

Our grade: 8.0 / 8.0  
Report: 2.0 / 2.0  
Code quality: 2.0 / 2.0  
Auto-testing: 4.0 / 4.0

Feedback:  
Feedback on report: Your representation of the problem is natural and sensible - well done! A very interesting approach to designing your heuristic. It's nice to see your discussion that a complex heuristic like Dijkstra can work for this problem, since h(n) is so good that A* doesn't need to expand too many nodes. The relaxation to allow a piece to jump at any time is an elegant way of making the heuristic admissible. Your empirical approach to determining the factors that influence the space/ time complexity is excellent - the graphs clearly display many of the features we'd expect from the theoretical time/space complexity of A*. Overall, a great report.  

Feedback on code quality: Your program is very readable, well done. In particular: * Great use of docstrings * Good use of Python OO concepts (classes, magic methods) * Good choices of data structure * Nice adherence to Python naming conventions One minor comment would be that you seem to use a pattern like "".join([... list of strings ...]) a lot. Have you considered using Python's f-strings? They're easier to read and more efficient.

## Project2

In this second part of the project we will play the original, three-player version of Chexers (as introduced in week 1).
Before you read this specification you may wish to re-read the “Rules for the Game of Chexers” document.
The aims for Project Part B are for you and your project partner to (1) practice game-playing algorithms
discussed in lectures and tutorials, (2) develop your own strategies for playing Chexers, and (3) conduct your own
research into more advanced game-playing algorithms; all for the purpose of creating the best Chexers-playing
program the world has ever seen.

Your task is twofold. Firstly, your team will design and implement a program that ‘plays’ a game of Chexers—
given information about the evolving state of a game, your program will decide on an action to take on each of its
turns. We provide a driver program that coordinates a game of Chexers between three such programs (the ‘referee’,
described in the ‘Running your program’ section).
Secondly, your team will write a report discussing the strategies your program uses to play the game, the
algorithmic techniques you have implemented, and any other creative aspects of your work.

Our grade: 21.5 / 22.0  
Code quality: 4.00 / 4.00  
Correctness: 4.00 / 4.00  
Performance: 6.50 / 7.00  
Creativity: 7.00 / 7.00

Feedback:
Feedback on code quality, correctness, and performance:  
Results from test games against benchmark opponents:  
--------------------- opponent win ratio ---------------------  
random 100.0% greedy 50.0% searching 62.5% (email Matt for logs)  
Well done, the performance of your player against our benchmarks was really excellent! 

Feedback on creativity: Well done for the awesome number of substantial improvements you've adopted over the basic techniques included in lectures, and for your impressively creative insights into the game of Chexers itself, resulting in a highly dynamic and highly effective playing strategy. Super great!
