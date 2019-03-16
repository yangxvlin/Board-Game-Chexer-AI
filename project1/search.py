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
import copy
from collections import deque

from Hexe import Hexe
from Player import Player
from State import State

JSON_FILE_KEYS = ["colour", "pieces", "blocks"]

REPLY = True


class Search:
    MAX_DEPTH = 100

    def __init__(self):
        self.visited_states = None
        self.found = None

    # IDDFS return all next actions version
    # IDDFS https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search
    def iterative_deeping_search(self, root, max_depth=MAX_DEPTH):
        """ returns the optimal solution of shortest steps problem in game
        chexer
        :param root
        :param max_depth:
        """
        # TODO finish this
        not_found = []
        # NOTE: use s.get_next_state to further search

        for depth in range(0, max_depth):
            # clear search history
            self.visited_states = []
            self.found = deque()  # deque([action, state], ....)

            actions = []

            # route: [[action, ...], [state, ...]]
            route = self.depth_limited_search([[], [root]], depth)
            # print(found, remaining, self.found)
            # print(found and (not remaining))
            print(depth, route)
            if route is not None:  # has result
                if route[0]:
                    return route
        return not_found

    def depth_limited_search(self, route, depth):
        cur_state = route[-1][-1]
        # print(1, route)
        if depth == 0:
            return None
        if not cur_state.has_remaining_pieces():
            return route

        # print(2, cur_state.all_possible_playing_player_action())

        for action in cur_state.all_possible_playing_player_action():

            # print(3, action, "on states[-1]:", cur_state)

            next_state = cur_state.get_next_state(action)

            # print(4, next_state not in route[1])

            if next_state not in route[1]:

                route_copy = copy.deepcopy(route)

                route_copy[0].append(action)
                route_copy[1].append(next_state)

                # print(route_copy)

                next_route = self.depth_limited_search(route_copy, depth - 1)
                if next_route:
                    # print("end")
                    return next_route

    # https://gist.github.com/damienstanton/7de65065bf584a43f96a
    @staticmethod
    def a_star_search(root):

        from functools import lru_cache

        @lru_cache(maxsize=128)
        def f(state, state_g_score):
            return state_g_score + h(state)

        @lru_cache(maxsize=128)
        def h(state):
            return state.cost_to_finish()

        def reconstruct_path(came_from_dict, current):
            """ :return [[None, root], [action 1, state 1], ...]"""
            total_path = [current, None]
            while current in came_from_dict.keys():
                total_path.append([current, came_from_dict[current][0]])

                current = came_from_dict[current][1]  # current := previous
            return total_path

        def min_open_set(cur_open_set, cur_f_score):
            cur_state = cur_open_set[0]
            cur_min_f_score = cur_f_score[current_state]

            for i in range(1, len(cur_open_set)):
                tmp_state = cur_open_set[i]

                if cur_f_score[tmp_state] < cur_min_f_score:
                    cur_min_f_score = cur_f_score[tmp_state]
                    cur_state = tmp_state

            return cur_state

        close_set = []
        open_set = [root]
        came_from = {root: [None, None]}  # {state: [action, previous_state]}

        g_score = {root: 0}
        f_score = {root: f(root, g_score[root])}

        while open_set:
            # the node in open_set having the lowest f_score[] value
            current_state = min_open_set(open_set, f_score)

            if not current_state.has_remaining_pieces():
                return reconstruct_path(came_from, current_state)

            open_set.remove(current_state)
            close_set.append(current_state)

            for action in current_state.all_possible_playing_player_action():
                next_state = current_state.get_next_state(action)

                if next_state in close_set:
                    continue

                tentative_g_score = g_score[current_state] + 1  # path cost = 1

                if (next_state not in open_set) & \
                        (tentative_g_score < g_score[next_state]):
                    came_from[next_state] = [action, current_state]
                    g_score[next_state] = tentative_g_score
                    f_score[next_state] = h(next_state)

                    if next_state not in open_set:
                        open_set.append(next_state)

        return None



    # duplicated states
        # if state in self.visited_states:
        #     return None, False
        # else:
        #     self.visited_states.append(state)

        # if depth == 0:
        #     # print(state, state.has_remaining_pieces())
        #     if not state.has_remaining_pieces():  # all finished
        #         return state, True
        #     else:
        #         return None, True  # (Not found, but may have children)
        #
        # elif depth > 0:
        #     any_remaining = False
        #     for pieces in state.player_pieces[state.playing_player]:
        #         for action in pieces.get_all_possible_actions(state.all_pieces()):
        #             found, remaining = self.depth_limited_search(
        #                 state.get_next_state(action), depth - 1)
        #             if found is not None:
        #                 # print(action, found)
        #                 # self.found.appendleft((action, state))
        #                 return found, True
        #             # (At least one state found at depth, let IDDFS deepen)
        #             if remaining:
        #                 any_remaining = True
        #     return None, any_remaining

    # IDDFS only return next action version
    # # IDDFS https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search
    # @staticmethod
    # def iterative_deeping_search(root, max_depth=MAX_DEPTH):
    #     """ returns the optimal solution of shortest steps problem in game
    #     chexer
    #     :param root
    #     :param max_depth:
    #     """
    #     # TODO finish this
    #     actions = []
    #     # NOTE: use s.get_next_state to further search
    #
    #     for depth in range(0, max_depth):
    #         found, remaining = Search.depth_limited_search(root, depth)
    #         if found is not None:
    #             return found
    #         elif not remaining:
    #             return actions
    #
    #     return actions
    #
    # @staticmethod
    # def depth_limited_search(state, depth):
    #     if depth == 0:
    #         if not state.has_remaining_pieces():
    #             return state, True
    #         else:
    #             return None, True  # (Not found, but may have children)
    #
    #     elif depth > 0:
    #         any_remaining = False
    #         for pieces in state.player_pieces[state.playing_player]:
    #             for action in pieces.get_all_possible_actions(state.obstacles):
    #                 found, remaining = Search.depth_limited_search(
    #                     state.get_next_state(action), depth - 1)
    #                 if found is not None:
    #                     return found, True
    #                 if remaining:
    #                     any_remaining = True  # (At least one state found at depth, let IDDFS deepen)
    #         return None, any_remaining


def main():
    filename = sys.argv[1]

    with open(filename) as json_file:
        data = json.load(json_file)

        player = Player.PLAYER_ORDER[data[JSON_FILE_KEYS[0]]]

        player_pieces = {player: Hexe.read_coordinates(data[JSON_FILE_KEYS[1]],
                                                       data[JSON_FILE_KEYS[0]])}
        obstacles = Hexe.read_coordinates(data[JSON_FILE_KEYS[2]],
                                          JSON_FILE_KEYS[2][:-1])

    search = Search()

    state = State(player, player_pieces, obstacles)

    search_res = search.iterative_deeping_search(state)

    # print("final: ", search_res)
    print_result(search_res, True)

    # test1(state)


def test1(state):
    print(state.player_pieces[0][0].get_all_possible_actions(state.obstacles))


def print_result(search_result, debug=True, reply_mode=REPLY):
    # print(len(search_result))
    for i in range(0, len(search_result[0])):
        state = search_result[1][i+1]
        action = search_result[0][i]
        # print("###", action, state)
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
    for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
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

