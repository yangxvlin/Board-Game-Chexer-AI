"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-11 22:08:28
Description: max^n agent with shadow pruning
https://project.dke.maastrichtuniversity.nl/games/files/phd/Nijssen_thesis.pdf
Page 20 index 34/205
"""

import numpy as np
from deep_dark_fantastic_boys_next_door.Constants import (N_PLAYER, PLAYER_WIN_THRESHOLD)

SEARCH_DEPTH = 3

NEGATIVE_INFINITY = float('-inf')

# TODO sum of the values for all players has a fixed upper bound
U = float('inf')  # 12 for 12 pieces on board


class MaxnAgent:

    # TODO Lazy evaluation

    def __init__(self, depth=SEARCH_DEPTH, u=U):
        self.depth = depth
        self.u = u

    def get_next_action(self, state, player, eval_index=0, opponent_index=0):
        # print("1", state)
        # print("2222222222", player is None)
        next_state, best = self.maxn(state, self.depth, state.playing_player, NEGATIVE_INFINITY, player, eval_index, opponent_index)
        # print(state, "->", next_state)
        # print(state)
        # print(">>>> ", best, state.evaluate(state.playing_player, player.choose_eval(eval_index), player),
        #       "->", next_state.evaluate(state.playing_player, player.choose_eval(eval_index), player))
        assert next_state is not None
        return next_state.action

    # TODO check my recursion return correct move
    def maxn(self, s, depth, root_player, alpha, player, eval_index=0, opponent_index=0):
        # print(eval_index)
        # print(depth, alpha)
        # s:cur state
        my_next_state = None

        # print("!!!!!!!!!", s.is_terminate())
        if (depth <= 0) or ((depth < self.depth) and s.is_terminate(player)):
            # print(">>>>>>")
            res = []
            for i in range(0, 3):
                if i == s.playing_player:
                    if player.states_counter[frozenset(s.pieces_player_dict)] == (PLAYER_WIN_THRESHOLD-1):
                        res.append(-100)  # doesn't want to draw so early
                    elif i == root_player:
                        res.append(s.evaluate(i, player.choose_eval(eval_index), player))
                    else:
                        res.append(s.evaluate(i, player.choose_eval(opponent_index)))
                else:
                    res.append(None)
            return s, res
            # return s, [None for i in range(0, 3)]

        best = [NEGATIVE_INFINITY for _ in np.arange(0, N_PLAYER)]
        cur_player = s.playing_player

        next_states = s.all_next_state()
        # print(next_states)
        # print(depth, SEARCH_DEPTH)
        # print("#####", len(next_states))
        for next_state in next_states:
            # print(depth, cur_player, "{:30s}".format(str(next_state.action)), "{:.4f}".format(next_state.evaluate(s.playing_player, player.choose_eval(eval_index))), best)
            next_player = next_state.playing_player

            _, result = self.maxn(next_state, depth - 1, root_player, best[next_player], player, eval_index, opponent_index)
            if result[cur_player] is None:
                if player.states_counter[frozenset(next_state.pieces_player_dict)] == (PLAYER_WIN_THRESHOLD-1):
                    result[cur_player] = -100  # doesn't want to draw so early
                # print("!!!!!")
                elif cur_player == root_player:
                    # print("1111111", player is None)
                    result[cur_player] = next_state.evaluate(cur_player, player.choose_eval(eval_index), player)
                else:
                    result[cur_player] = next_state.evaluate(cur_player, player.choose_eval(opponent_index))

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
