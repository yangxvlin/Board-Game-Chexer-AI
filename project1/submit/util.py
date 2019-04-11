"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-18 19:20:58
Description: Some helper function used in program
"""

import os
import sys
from Constants import JSON_FILE_KEYS, PLAYER_PLAYING_ORDER, PLAYER_GOAL, \
    BOARD_BOUND, MOVE_DELTA
import json
from queue import PriorityQueue
from PriorityItem import PriorityItem

""" enable pause in state replay """
PAUSE = False


def main():
    """ main function
    """
    from search import a_star_search

    # get filename
    filename = sys.argv[1]

    # read state
    state = read_state_from_json(filename)

    # test a* running time
    from datetime import datetime
    # print("#")
    # print("# a* start at", datetime.now())
    search_res = a_star_search(state)
    # print("# a* end at", datetime.now())

    # print(len(search_res) - 1)
    print("# solution path length =", len(search_res) - 1, "\n#")

    # submission output
    print_result(search_res, True)
    # debug output: enable state pause, board printed
    # print_result(search_res, True, True, True)

    # testing
    # from test import test1
    # print("#", datetime.now())
    # test1(state)
    # print("#", datetime.now())
    # test2()


def print_result(search_result, debug=True, replay_mode=PAUSE,
                 board_printed=False):
    """ print search result
    :param search_result: state from root to goal by a* search
    :param debug: True for board with axial coordinates
    :param replay_mode: enable pause if one state is printed
    :param board_printed: print state after action
    """

    # print pieces on board
    if board_printed:
        print_board(search_result[0].to_board_dict(), "# initial state", debug)

    # enable step by step play
    if replay_mode:
        os.system('pause')

    for i in range(1, len(search_result)):
        state = search_result[i]
        action = search_result[i].action

        print(action)

        # print pieces on board
        if board_printed:
            print_board(state.to_board_dict(), "", debug)

        # enable step by step play
        if replay_mode:
            os.system('pause')


def piece_min_action_to_finish(obstacles, player):
    """ preprocess the board calculate minimum action for each hexe is not 
    occupied by a block to exit and returns a {hexe axial coordinate: minimum 
    action to exit}
    :param player: player is playing
    :param obstacles: obstacles in part a
    :return: {(q, r): int}
    """
    min_action = {}
    goal_hexes = PLAYER_GOAL[player]
    visited = set()

    # priority queue used to do dijkstra
    priority_queue = PriorityQueue()

    for goal_hexe in goal_hexes:
        if goal_hexe not in obstacles:
            # 1 action for exit
            min_action[goal_hexe] = 1

            priority_queue.put(PriorityItem(min_action[goal_hexe], goal_hexe))

    # run dijkstra to update cost for place around the investigating piece
    while not priority_queue.empty():
        # get stored item with min priority
        item = priority_queue.get()
        # current piece's min number of action to exit
        cost_so_far = item.get_priority()
        # piece used to update all its neighbor within 2 move
        piece = item.get_item()

        for delta in MOVE_DELTA:
            # update one moved to piece
            piece_one_move = vector_add(piece, delta)

            # moved to place is on board
            if on_board(piece_one_move):
                tentative_cost = cost_so_far + 1

                # moved to place not occupied
                if piece_one_move not in obstacles:
                    if piece_one_move not in visited:
                        visited.add(piece_one_move)
                        try:
                            if (tentative_cost < min_action[piece_one_move]):
                                # +1 for one action
                                # min(one move to cur piece, original action)
                                min_action[piece_one_move] = tentative_cost
                                priority_queue.put(PriorityItem(
                                                    min_action[piece_one_move], 
                                                    piece_one_move))
                        # not explored
                        except KeyError:
                            min_action[piece_one_move] = tentative_cost
                            priority_queue.put(PriorityItem(
                                                min_action[piece_one_move], 
                                                piece_one_move))

                # update jumped to place is on board and not occupied
                piece_one_jump = vector_add(piece_one_move, delta)
                if on_board(piece_one_jump) and \
                        (piece_one_jump not in obstacles):
                    if piece_one_jump not in visited:
                        visited.add(piece_one_jump)
                        try:
                            if (tentative_cost < min_action[piece_one_jump]):
                                # +1 for one action
                                # min(one jump to cur piece, original action)
                                min_action[piece_one_jump] = tentative_cost
                                priority_queue.put(PriorityItem(
                                                    min_action[piece_one_jump], 
                                                    piece_one_jump))
                        # not explored
                        except KeyError:
                            min_action[piece_one_jump] = tentative_cost
                            priority_queue.put(PriorityItem(
                                                min_action[piece_one_jump], 
                                                piece_one_jump))

    return min_action


def read_state_from_json(filename):
    """ read State from file
    :param filename: json file path
    :return: State(file)
    """

    with open(filename) as json_file:
        data = json.load(json_file)

        player = data[JSON_FILE_KEYS[0]]
        player_pieces = element_to_tuple(data[JSON_FILE_KEYS[1]])
        obstacles = element_to_tuple(data[JSON_FILE_KEYS[2]])

    for obstacle in obstacles:
        if obstacle in PLAYER_GOAL[PLAYER_PLAYING_ORDER[player]]:
            PLAYER_GOAL[PLAYER_PLAYING_ORDER[player]].remove(obstacle)

    return make_state(player, obstacles, player_pieces)


def make_state(cur_player, obstacles, pieces):
    """ return State given data read from json file
    :param cur_player: player is playing
    :param obstacles: obstacles in part a
    :param pieces: player's pieces
    :return: a State object
    """
    from State import State

    player_pieces = []

    # set other two player with empty pieces
    for player in PLAYER_PLAYING_ORDER.keys():
        if player == cur_player:
            player_pieces.append(pieces)
        else:
            player_pieces.append([])

    return State(PLAYER_PLAYING_ORDER[cur_player], obstacles, player_pieces)


def vector_add(a, b):
    """ perform vector addition assume input vectors have same dimension
    :param a: vector a
    :param b: vector b
    :returns:  a + b
    """
    assert(len(a) == len(b))

    from operator import add
    return tuple(map(add, a, b))


def axial_to_cube(axial):
    """ convert an cube coordinate from axial coordinate
    modified from https://www.redblobgames.com/grids/hexagons/#conversions
    :param axial: an axial coordinate in hexagonal system
    :return: cube coordinate in hexagonal system
    """
    x = axial[0]  # q
    z = axial[1]  # r
    y = -x-z
    return tuple([x, y, z])


def on_board(hexe):
    """ check if an hexe piece is on the chexer board by turning an axial
    coordinate hexe to a cube coordinate hexe
    :param hexe: axial coordinate in hexagonal system
    :returns: True if on bard, otherwise False
    """

    cube = axial_to_cube(hexe)

    # check each bound
    for axis in cube:
        if abs(axis) > BOARD_BOUND:
            return False
    return True


def action_to_string(action, from_hexe, to_hexe=None):
    """ return an action in chexer in string
    :param action: action name in String
    :param from_hexe: an axial coordinate hexe on board
    :param to_hexe: an axial coordinate hexe on board
    :return: action.toString()
    """
    res = " ".join([action, "from", str(from_hexe)])

    if to_hexe is not None:
            res = " ".join([res, "to", str(to_hexe)])

    return "".join([res, "."])


def is_in_goal_hexe(hexe, player):
    """ check whether a hexe has moved in player's goal hexes
    :param hexe: an axial coordinate hexe on board
    :param player: the player is playing
    :return: True if hexe is in player's goal hexes, otherwise False
    """
    assert(player in PLAYER_GOAL)

    return hexe in PLAYER_GOAL[player]


def element_to_tuple(list_of_elements):
    """ return list of tuple element
    :param list_of_elements: list of iterable elements
    :return: list of tuple elements
    """
    return list(map(lambda x: tuple(x), list_of_elements))


def print_board(board_dict, message="", debug=False, **kwargs):
    """
    Helper function to print a drawing of a hexagonal board's contents.

    Arguments:

    * `board_dict` -- dictionary with tuples for keys and anything printable
    for values. The tuple keys are interpreted as hexagonal coordinates (using
    the axial coordinate system outlined in the project specification) and the
    values are formatted as strings and placed in the drawing at the corres-
    ponding location (only the first 5 characters of each string are used, to
    keep the drawings small). Coordinates with missing values are left blank.

    Keyword arguments:

    * `message` -- an optional message to include on the first line of the
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates
    inside each hex, set this to `True` -- default `False`.
    * Or, any other keyword arguments! They will be forwarded to `print()`.
    """

    # Set up the board template:
    if not debug:
        # Use the normal board template (smaller, not showing coordinates)
        template = """{0}
#           .-'-._.-'-._.-'-._.-'-.
#          |{16:}|{23:}|{29:}|{34:}| 
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |{10:}|{17:}|{24:}|{30:}|{35:}| 
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}| 
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}| 
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}| 
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{03:}|{08:}|{14:}|{21:}|{28:}| 
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{04:}|{09:}|{15:}|{22:}|
#          '-._.-'-._.-'-._.-'-._.-'"""
    else:
        # Use the debug board template (larger, showing coordinates)
        template = """{0}
#              ,-' `-._,-' `-._,-' `-._,-' `-.
#             | {16:} | {23:} | {29:} | {34:} | 
#             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {10:} | {17:} | {24:} | {30:} | {35:} |
#         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-. 
#     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
#     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
# | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
#     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#         | {03:} | {08:} | {14:} | {21:} | {28:} |
#         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
#             | {04:} | {09:} | {15:} | {22:} |   | input |
#             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
#              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

    # prepare the provided board contents as strings, formatted to size.
    ran = range(-3, +3 + 1)
    cells = []
    for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     "  # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)
