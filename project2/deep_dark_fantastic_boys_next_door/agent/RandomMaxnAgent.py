"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-5-12 20:07:31
Description: 
"""

from numpy.random import choice
import numpy as np
from deep_dark_fantastic_boys_next_door.Constants import (N_PLAYER)

SEARCH_DEPTH = 3

NEGATIVE_INFINITY = float('-inf')

# TODO sum of the values for all players has a fixed upper bound
U = float('inf')  # 12 for 12 pieces on board


class RandomMaxnAgent:

    def __init__(self, depth=SEARCH_DEPTH, u=U):
        self.depth = depth
        self.u = u

    def get_next_action(self, state, player):
        # print("1", state)
        next_states, _ = self.maxn(state, self.depth, state.playing_player, NEGATIVE_INFINITY, player)
        # print(state, "->", next_state)
        assert len(next_states) > 0
        index = choice(len(next_states))
        chosen_state = next_states[index]
        # print(">>>> ", state.evaluate(state.playing_player, player.choose_eval()), "->", chosen_state.evaluate(state.playing_player, player.choose_eval()), "{}/{}".format(index, len(next_states)))
        return chosen_state.action

    # TODO check my recursion return correct move
    def maxn(self, s, depth, root_player, alpha, player):
        # s:cur state
        my_next_states = []

        # print("!!!!!!!!!", s.is_terminate())
        if depth <= 0 or s.is_terminate(player):
            return s, [s.evaluate(i, player.choose_eval()) if i == s.playing_player else None for i in range(0, 3)]

        best = [NEGATIVE_INFINITY for _ in np.arange(0, N_PLAYER)]
        cur_player = s.playing_player

        next_states = s.all_next_state()
        # print(depth, SEARCH_DEPTH)
        # print("#####", len(next_states))
        for next_state in next_states:
            # print(depth, cur_player, "{:30s}".format(str(next_state.action)), "{:.4f}".format(next_state.evaluate(s.playing_player, player.choose_eval())), best)
            next_player = next_state.playing_player

            _, result = self.maxn(next_state, depth - 1, root_player, best[next_player], player)
            if result[cur_player] is None:
                result[cur_player] = next_state.evaluate(cur_player, player.choose_eval())

            if result[cur_player] >= best[cur_player]:
                if result[cur_player] > best[cur_player]:
                    best = result
                    my_next_states = []

                # TODO place need check
                # our player
                if (depth == self.depth) and (cur_player == root_player):
                    my_next_states.append(next_state)


            # print(result, alpha, depth)
            if result[cur_player] >= U - alpha:
                print("pruned!", depth, result, alpha)
                return my_next_states, result

        return my_next_states, best

