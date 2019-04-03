"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Author:      XuLin Yang
Student id:  904904
Date:        2019-3-15 14:56:03
Description: search algorithm for part a
"""

# used to map function result with function input to reduce calculation time
from functools import lru_cache
from collections import deque
from queue import PriorityQueue
from PriorityItem import PriorityItem
from util import main


def a_star_search(root):
    """ a* algorithm modified from
    https://www.redblobgames.com/pathfinding/a-star/implementation.html
    :param root: root state to start search
    :return: search result with [root, state, state, ...] or None
    """

    @lru_cache(maxsize=200000)
    def f(state, state_g_score):
        """ f(state)
        :param state: input state
        :param state_g_score: g(state)
        :return: g(state) + h(state)
        """
        return state_g_score + h(state)

    @lru_cache(maxsize=200000)
    def h(state):
        """ h(state)
        :param state: input state
        :return: heuristic of state to goal state
        """
        return state.cost_to_finish()

    def reconstruct_path(came_from_dict, current):
        """ reconstruct solution path from visited state and its parent
        :param came_from_dict: a dictionary of {state: state's parent}
        :param current: goal state
        :return: [root, state1, state2, ..., goal state]
        """

        total_path = deque()
        total_path.append(current)
        while current in came_from_dict:
            total_path.appendleft(came_from_dict[current])

            # current := previous
            current = came_from_dict[current]
        return list(total_path)[1:]

    # visited state
    close_set = set()
    # exploring state
    open_set = PriorityQueue()
    # {state: previous_state}
    came_from = {root: None}

    # g(state)
    g_score = {root: 0}
    # f(state)
    f_score = {root: f(root, g_score[root])}

    open_set.put(PriorityItem(f_score[root], root))

    while not open_set.empty():
        # the node in open_set having the lowest f_score[] value
        current_state = open_set.get().get_item()

        # find solution and reconstruct action path
        if not current_state.has_remaining_pieces():
            print("# open list size:", open_set.qsize())
            print("# close list size:", len(close_set))

            search_res = reconstruct_path(came_from, current_state)
            # for test retrun search result, d, average b
            return search_res, len(search_res) - 1, (open_set.qsize() + len(close_set)) / len(close_set)

        close_set.add(current_state)

        # search for all neighbors
        for next_state in current_state.all_next_state():

            # avoid repeated state
            if next_state in close_set:
                continue

            # 1 for `path cost = 1`
            tentative_g_score = g_score[current_state] + 1

            # newly meet next_state directly update its score
            if (next_state not in g_score) or \
                    (tentative_g_score < g_score[next_state]):
                came_from[next_state] = current_state
                g_score[next_state] = tentative_g_score
                f_score[next_state] = f(next_state, g_score[next_state])

                # if next_state not in open_set:
                open_set.put(PriorityItem(f_score[next_state], next_state))

    return None, None, None


if __name__ == '__main__':
    """ when this module is executed, run the `main` function:
    """

    import sys
    from util import read_state_from_json, print_result

    # get filename
    filename = sys.argv[1]

    # read state
    state = read_state_from_json(filename)

    # test a* running time
    from datetime import datetime
    print("#")
    print("# a* start at", datetime.now())
    search_res, path_length, average_branching_factor = a_star_search(state)
    print("# a* end at", datetime.now())

    print("# solution path length =", len(search_res) - 1, "\n#")

    # submission output
    print_result(search_res, True)

    with open('output.txt', 'w') as the_file:
        the_file.write("{}\n".format(path_length))
        the_file.write("{}\n".format(average_branching_factor))
        the_file.write("{}\n".format(abs(path_length - state.cost_to_finish())))
        the_file.write("{}\n".format(len(state.player_pieces_list[state.playing_player])))
        the_file.write("{}\n".format(len(state.obstacles)))
