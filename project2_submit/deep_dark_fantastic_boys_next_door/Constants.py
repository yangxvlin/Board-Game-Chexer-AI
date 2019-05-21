"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-18 19:23:57
Description: Constants used in program
"""

""" initial score for players """
INITIAL_SCORE = [0, 0, 0]

""" an empty board """
EMPTY_BOARD = [[], [], []]

""" size of the chexer board """
BOARD_BOUND = 3

""" hexe piece's moving delta """
MOVE_DELTA = [(-1, 0), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 1)]

""" 
a modified moving delta (based on direction to the player's goal hexes) for 
each player 
"""
PLAYER_PREFERRED_MOVE_DELTA = {0: [(1, -1), (1, 0), (0, -1),
                                   (0, 1), (-1, 1), (-1, 0)],
                               1: [(-1, 1), (0, 1), (-1, 0),
                                   (1, 0), (0, -1), (1, -1)],
                               2: [(-1, 0), (0, -1), (1, -1),
                                   (-1, 1), (1, 0), (0, 1)]}

""" move action """
MOVE = "MOVE"

""" jump action """
JUMP = "JUMP"

""" exit action """
EXIT = "EXIT"

""" pass action """
PASS = "PASS"

""" a predefined pass action in the chexer game """
PASS_ACTION = ("PASS", None)

""" player win when 4 pieces exit """
PLAYER_WIN_THRESHOLD = 4

""" max number of game turns """
MAX_TURN = 256

""" map player string with player playing order """
PLAYER_PLAYING_ORDER = {"red": 0, "green": 1, "blue": 2}

""" player index playing order """
PLAYER_ORDER = [0, 1, 2]

""" index representation of blue player """
BLUE_PLAYER_INDEX = 2

""" player playing order with map player string """
PLAYING_ORDER_PLAYER_MAP = {0: "red", 1: "green", 2: "blue"}

""" each player's goal hexes' axial coordinates """
PLAYER_GOAL = {0: [(BOARD_BOUND, -i) for i in range(0, PLAYER_WIN_THRESHOLD)],
               1: [(i-BOARD_BOUND, BOARD_BOUND)
                   for i in range(0, PLAYER_WIN_THRESHOLD)],
               2: [(-i, i-BOARD_BOUND) for i in range(0, PLAYER_WIN_THRESHOLD)]}

""" 
the corner point in player's goal hexes are considered as important  strategy 
points 
"""
PLAYER_GOAL_STRATEGY_POINTS = {0: ((3, -3), (3,  0)),
                               1: ((0,  3), (-3, 3)),
                               2: ((-3, 0), (0, -3))}

""" maximum evaluation function value """
MAX_EVALUATION_VALUE = 100

""" minimum evaluation function value """
MIN_EVALUATION_VALUE = -100

""" number of players in game """
N_PLAYER = 3

""" 
open game human-start strategy for each player's starting turns to achieve a 
good started hexe pattern for MoZi Agent
{player: {turn: action/actions}} 
"""
THE_ART_OF_WAR = {0: {0: (MOVE, ((-3, 0), (-2, -1))),
                      1: ((JUMP, ((-2, -1), (0, -3))),
                          (MOVE, ((-3, 1), (-3, 0))),
                          (MOVE, ((-2, -1), (-1, -2))))},
                  1: {0: (MOVE, ((3, -3), (3,  -2))),
                      1: ((JUMP, ((3, -2), (3, 0))),
                          (MOVE, ((2, -3), (3, -3))),
                          (MOVE, ((3, -2), (3, -1))))},
                  2: {0: (MOVE, ((0,  3), (-1,  3))),
                      1: ((JUMP, ((-1, 3), (-3, 3))),
                          (MOVE, ((1, 2), (0, 3))),
                          (MOVE, ((-1, 3), (-2, 3))))}}

""" turn using human strategy """
THE_ART_OF_WAR_TURN_LIMIT = 1

""" negative infinity used in program """
NEGATIVE_INFINITY = float('-inf')

""" positive infinity used in program """
POSITIVE_INFINITY = float('inf')

# *****************************************************************************
# ** customized board hexe configure to highlight important points for agent **
# *****************************************************************************
""" 
strategy points for each player to capture used by MoZi Agent
{player: (upstream points, downstream points)} 
"""
STRATEGIC_POINTS = {0: [(0, -3), (-3, 0), (0, 3), (-3, 3)],
                    1: [(3,  0), (3, -3), (-3, 0), (0, -3)],
                    2: [(-3, 3), (0,  3), (3, -3), (3, 0)]}

""" all strategy points on board """
ALL_STRATEGIC_POINTS = [(-3, 0), (0, -3), (3, -3), (3, 0), (0, 3), (-3, 3)]

""" mapping between player with their wall points """
PLAYER_WALLS = {0: [(-2, -1), (-1, -2), (-2,  3), (-1,  3)],
                1: [(3,  -1), (3,  -2), (-2, -1), (-1, -2)],
                2: [(-2,  3), (-1,  3), (3,  -2), (3,  -1)]}

""" mapping between wall points and strategy points """
STRATEGY_POINTS_AND_WALL = {((-3, 0), (0, -3)): ((-2, -1), (-1, -2)),
                            ((0, -3), (-3, 0)): ((-2, -1), (-1, -2)),
                            ((-3, 3), (0,  3)): ((-2,  3), (-1,  3)),
                            ((0,  3), (-3, 3)): ((-2, 3), (-1, 3)),
                            ((3, -3), (3,  0)): ((3,  -1), (3,  -2)),
                            ((3,  0), (3, -3)): ((3, -1), (3, -2))}

""" 
points highlight how agent to evaluate the jump action to capture enemy points 
"""
STRATEGY_JUMP_FROM_TO_POINTS = (((0, -3), (-1, -2), (-2, -1)),
                                ((-3, 0), (-2, -1), (-1, -2)),
                                ((-3, 3), (-2, 3),  (-1,  3)),
                                ((0,  3), (-1, 3),  (-2,  3)),
                                ((3, 0),  (3, -1),  (3,  -2)),
                                ((3, -3), (3, -2),  (3,  -1)))

""" points highlight how agent to evaluate the jump action to outside """
STRATEGY_JUMP_FROM_TO_OUTSIDE_POINTS = {(0, -3): ((1, -3), (2, -3), (0, -2)),
                                        (-3, 0): ((-3, 1), (-3, 2), (-2, 0)),
                                        (-3, 3): ((-3, 2), (-3, 1), (-2, 2)),
                                        (0,  3): ((1,  2), (2,  1), (0,  2)),
                                        (3,  0): ((2,  1), (1,  2), (2,  0)),
                                        (3, -3): ((2, -3), (1, -3), (2, -2))}

""" 
points highlight how agent to evaluate the move action to outside
"""
STRATEGY_SAFE_MOVE_TO_OUTSIDE_POINTS = {
    (0, -3): (((-1, -2), (0, -2), (1, -3), (-2, -1)),
              ((1, -3), (2, -3), (0, -2), (-1, -2)),
              ((0, -2), (1, -3), (-1, -2), (-1, -1), (1, -2), (0, -1))),
    (-3, 0): (((-2, -1), (-2, 0), (-3, 1), (-1, -2)),
              ((-3, 1), (-3, 2), (-2, -1), (-2, 0)),
              ((-2, 0), (-3, 1), (-2, 1), (-1, 0), (-1, -1), (-2, -1))),
    (-3, 3): (((-2, 3), (-3, 2), (-2, 2), (-1, 3)),
              ((-3, 2), (-2, 2), (-2, 3), (-3, 1)),
              ((-2, 2), (-3, 2), (-2, 1), (-1, 1), (-1, 2), (-2, 3))),
    (0,  3): (((-1, 3), (-2, 3), (0, 2), (1, 2)),
              ((1, 2), (0, 2), (2, 1), (-1, 3)),
              ((0, 2), (-1, 3), (-1, 2), (0, 1), (1, 1), (1, 2))),
    (3,  0): (((3, -1), (2, 1), (2, 0), (3, -2)),
              ((2, 1), (1, 2), (2, 0), (3, -1)),
              ((2, 0), (2, 1), (1, 1), (1, 0), (2, -1), (3, -1))),
    (3, -3): (((3, -2), (3, -1), (2, -2), (2, -3)),
              ((2, -3), (1, -3), (2, -2), (3, -2)),
              ((2, -2), (2, -3), (1, -2), (1, -1), (2, -1), (3, -2)))
}

""" an important point """
DEATH_POINT = (-2, 3)

# ************************* unused but worth a look ***************************
""" 
open game human-start strategy for each player's starting turns to achieve a 
good started hexe pattern for adversarial agents
{player: {turn: action}} 
"""
OPEN_GAME_AGENT = {0: {0: (MOVE, ((-3, 0), (-2, 0))),
                       1: (MOVE, ((-2, 0), (-2, 1))),
                       2: (MOVE, ((-3, 3), (-2, 2)))},
                   1: {0: (MOVE, ((0, -3), (0, -2))),
                       1: (MOVE, ((0, -2), (1, -2))),
                       2: (MOVE, ((3, -3), (2, -2)))},
                   2: {0: (MOVE, ((0,  3), (0,  2))),
                       1: (MOVE, ((2,  1), (1,  1))),
                       2: (MOVE, ((3,  0), (2,  1)))}}

""" the number of turn of open game human-start strategy """
OPEN_GAME_TURN_LIMIT = 3
