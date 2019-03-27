"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-18 19:20:58
Description: Some helper function used in program
"""

""" enable pause in state replay """
PAUSE = False


def main():
    """ main function
    """
    from search import a_star_search
    import sys

    filename = sys.argv[1]

    state = read_state_from_json(filename)

    # test a* running time
    from datetime import datetime
    print("#", datetime.now())
    search_res = a_star_search(state)
    print("#", datetime.now())

    print("# solution path length =", len(search_res) - 1, "\n#")

    # submission output
    print_result(search_res, True)
    # debug output: enable state pause, board printed
    # print_result(search_res, True, True, True)

    # testing
    # from test import test1, test2
    # test1(state)
    # test2()


def print_result(search_result, debug=True, replay_mode=PAUSE,
                 board_printed=False):
    """ print search result
    :param search_result: state from root to goal by a* search
    :param debug: True for board with axial coordinates
    :param replay_mode: enable pause if one state is printed
    :param board_printed: print state after action
    """

    import os

    if board_printed:
        print_board(search_result[0].to_board_dict(), "# initial state", debug)

    if replay_mode:
        os.system('pause')

    for i in range(1, len(search_result)):
        state = search_result[i]
        action = search_result[i].action

        print(action)

        if board_printed:
            print_board(state.to_board_dict(), "", debug)

        if replay_mode:
            os.system('pause')


def read_state_from_json(filename):
    """ read State from file
    :param filename: json file path
    :return: State(file)
    """

    from Constants import JSON_FILE_KEYS
    from State import State
    import json

    with open(filename) as json_file:
        data = json.load(json_file)

        player = data[JSON_FILE_KEYS[0]]
        player_pieces = {player: element_to_tuple(data[JSON_FILE_KEYS[1]])}
        obstacles = element_to_tuple(data[JSON_FILE_KEYS[2]])

    return State(player, obstacles, player_pieces)


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
    from Constants import BOARD_BOUND

    cube = axial_to_cube(hexe)

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
    from Constants import PLAYER_GOAL
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
