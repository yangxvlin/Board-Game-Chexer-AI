"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-11 22:08:28
Description: max^n agent with shadow pruning
https://project.dke.maastrichtuniversity.nl/games/files/phd/Nijssen_thesis.pdf
Page 20 index 34/205
"""

import numpy as np
from Constants import N_PLAYER, PLAYER_OEDER_DICT

SEARCH_DEPTH = 4

NEGATIVE_INFINITY = float('-inf')

# TODO sum of the values for all players has a fixed upper bound
U = 12  # 12 for 12 pieces on board


def get_next_move(state):
    next_state, _ = maxn(state, SEARCH_DEPTH, state.playing_player, 
                        NEGATIVE_INFINITY)

    return next_state.action

# TODO check my recursion return correct move
def maxn(s, depth, root_player, alpha):
    # s:cur state
    next_state = None

    if depth <= 0 or s.is_terminate():
        return next_state, s.evaluate()

    best = [NEGATIVE_INFINITY for _ in np.arange(0, N_PLAYER)]

    cur_player = s.playing_player
    cur_player_index = PLAYER_OEDER_DICT[cur_player]

    next_states = s.all_next_state()

    for next_state in next_states:
        next_player = next_state.playing_player

        _, result = maxn(next_state, depth - 1, root_player, best[next_player])
        if result[cur_player_index] > best[cur_player_index]:
            best = result

            # TODO place need check
            # our player
            if (depth == SEARCH_DEPTH) and (cur_player == root_player):
                my_next_state = next_state

        if result[cur_player_index] >= U - alpha:
            return next_state, result

    return my_next_state, best
