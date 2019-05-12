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

SEARCH_DEPTH = 3

NEGATIVE_INFINITY = float('-inf')

# TODO sum of the values for all players has a fixed upper bound
U = float('inf')  # 12 for 12 pieces on board


class MaxnAgent:

    # TODO Lazy evaluation

    def __init__(self, depth=SEARCH_DEPTH, u=U):
        self.depth = depth
        self.u = u

    def get_next_action(self, state, player):
        # print("1", state)
        next_state, _ = self.maxn(state, self.depth, state.playing_player, NEGATIVE_INFINITY, player)
        # print(state, "->", next_state)
        print(">>>> ", state.evaluate(state.playing_player, player.choose_eval()), "->", next_state.evaluate(state.playing_player, player.choose_eval()))
        assert next_state is not None
        return next_state.action

    # TODO check my recursion return correct move
    def maxn(self, s, depth, root_player, alpha, player):
        # print(depth, alpha)
        # s:cur state
        my_next_state = None

        # print("!!!!!!!!!", s.is_terminate())
        if depth <= 0 or s.is_terminate():
            return s, [s.evaluate(i, player.choose_eval()) if i == s.playing_player else None for i in range(0, 3)]

        best = [NEGATIVE_INFINITY for _ in np.arange(0, N_PLAYER)]
        cur_player = s.playing_player

        next_states = s.all_next_state()
        # print(depth, SEARCH_DEPTH)
        # print("#####", len(next_states))
        for next_state in next_states:
            # print(depth, cur_player, "{:30s}".format(str(next_state.action)), "{:.4f}".format(next_state.evaluate(s.playing_player, "")), best)
            next_player = next_state.playing_player

            _, result = self.maxn(next_state, depth - 1, root_player, best[next_player], player)
            if result[cur_player] is None:
                result[cur_player] = next_state.evaluate(cur_player, player.choose_eval())

            if result[cur_player] > best[cur_player]:
                best = result

                # TODO place need check
                # our player
                if (depth == self.depth) and (cur_player == root_player):
                    my_next_state = next_state
                    # print(">>>>>>>", next_state.action)

            # print(result, alpha, depth)
            if result[cur_player] >= U - alpha:
                print("pruned!", depth, result, alpha)
                return next_state, result

        return my_next_state, best
