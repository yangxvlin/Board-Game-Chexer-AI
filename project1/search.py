"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Author:      XuLin Yang
Student id:  904904
Date:        2019-3-15 14:56:03
Description: 
"""

import json
import os
import sys

from collections import deque
from State import State

JSON_FILE_KEYS = ["colour", "pieces", "blocks"]

REPLY = True

MAX_DEPTH = 100


# https://gist.github.com/damienstanton/7de65065bf584a43f96a
def a_star_search(root):

    from functools import lru_cache

    @lru_cache(maxsize=128)
    def f(state, state_g_score):
        return state_g_score + h(state)

    def h(state):
        return state.cost_to_finish()

    def reconstruct_path(came_from_dict, current):
        """ :return [state, ...]"""
        total_path = deque()
        total_path.append(current)
        while current in came_from_dict.keys():
            total_path.appendleft(came_from_dict[current])

            current = came_from_dict[current]  # current := previous
        return list(total_path)[1:]

    def min_open_set(cur_open_set, cur_f_score):
        cur_state = cur_open_set[0]
        cur_min_f_score = cur_f_score[cur_state]

        for i in range(1, len(cur_open_set)):
            tmp_state = cur_open_set[i]

            if cur_f_score[tmp_state] < cur_min_f_score:
                cur_min_f_score = cur_f_score[tmp_state]
                cur_state = tmp_state

        return cur_state

    close_set = []
    open_set = [root]
    came_from = {root: None}  # {state: previous_state}

    g_score = {root: 0}
    f_score = {root: f(root, g_score[root])}

    while open_set:
        # the node in open_set having the lowest f_score[] value
        current_state = min_open_set(open_set, f_score)

        if not current_state.has_remaining_pieces():
            return reconstruct_path(came_from, current_state)

        open_set.remove(current_state)
        close_set.append(current_state)

        for next_state in current_state.all_next_state():

            if next_state in close_set:
                continue

            tentative_g_score = g_score[current_state] + 1  # path cost = 1

            # print(next_state, "in", g_score)
            if next_state not in open_set:

                # newly meet next_state directly update its score
                if (next_state not in g_score.keys()) or \
                        (tentative_g_score < g_score[next_state]):
                    came_from[next_state] = current_state
                    g_score[next_state] = tentative_g_score
                    f_score[next_state] = f(next_state, g_score[next_state])

                    if next_state not in open_set:
                        open_set.append(next_state)

    return None


def main():
    from util import element_to_tuple

    filename = sys.argv[1]

    with open(filename) as json_file:
        data = json.load(json_file)

        player = data[JSON_FILE_KEYS[0]]

        player_pieces = {player: element_to_tuple(data[JSON_FILE_KEYS[1]])}
        obstacles = element_to_tuple(data[JSON_FILE_KEYS[2]])

    # print(player_pieces)
    # print(obstacles)

    state = State(player, obstacles, player_pieces)

    # search_res = iterative_deeping_search(state)
    # print_result(search_res, True)

    search_res = a_star_search(state)
    # print(search_res)
    print_result2(search_res, True)

    # from test import test1, test2
    # test1(state)
    # test2()


def print_result2(search_result, debug=True, reply_mode=REPLY):
    print(search_result)
    print_board(search_result[0].to_board_dict(), "# initial state", debug)
    if reply_mode:
        os.system('pause')

    for i in range(1, len(search_result)):
        state = search_result[i]
        action = search_result[i].action

        print_board(state.to_board_dict(), str(action), debug)

        if reply_mode:
            os.system('pause')


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
    ran = range(-3, +3+1)
    cells = []
    for qr in [(q, r) for q in ran for r in ran if -q-r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     "  # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()

