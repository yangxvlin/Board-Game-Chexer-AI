"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-11 22:08:28
Description: max^n agent with shadow pruning
https://project.dke.maastrichtuniversity.nl/games/files/phd/Nijssen_thesis.pdf
Page 20 index 34/205
"""

import numpy as np
from deep_dark_fantastic_boys_next_door.Constants import (N_PLAYER)

SEARCH_DEPTH = 4

NEGATIVE_INFINITY = float('-inf')

# TODO sum of the values for all players has a fixed upper bound
U = 12  # 12 for 12 pieces on board


class MaxnAgent:

    # TODO Lazy evaluation

    def __init__(self, depth=SEARCH_DEPTH, u=U):
        self.depth = depth
        self.u = u

    def get_next_move(self, state):
        next_state, _ = self.maxn(state, self.depth, state.playing_player,
                                  NEGATIVE_INFINITY)
        assert next_state is not None
        return next_state.action

    # TODO check my recursion return correct move
    def maxn(self, s, depth, root_player, alpha):
        # s:cur state
        my_next_state = None

        if depth <= 0 or s.is_terminate():
            return my_next_state, s.evaluate()

        best = [NEGATIVE_INFINITY for _ in np.arange(0, N_PLAYER)]

        cur_player = s.playing_player

        next_states = s.all_next_state()

        for next_state in next_states:
            next_player = next_state.playing_player

            _, result = self.maxn(next_state, depth - 1, root_player,
                                  best[next_player])
            if result[cur_player] > best[cur_player]:
                best = result

                # TODO place need check
                # our player
                if (depth == SEARCH_DEPTH) and (cur_player == root_player):
                    my_next_state = next_state

            if result[cur_player] >= U - alpha:
                return next_state, result

        return my_next_state, best
