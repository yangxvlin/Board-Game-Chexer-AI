"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-11 22:08:28
Description: max^n agent with shadow pruning
modify from:
https://project.dke.maastrichtuniversity.nl/games/files/phd/Nijssen_thesis.pdf
Page 20 index 34/205
"""

import numpy as np
from deep_dark_fantastic_boys_next_door.Constants import (N_PLAYER,
                                                          PLAYER_WIN_THRESHOLD,
                                                          MIN_EVALUATION_VALUE,
                                                          NEGATIVE_INFINITY,
                                                          POSITIVE_INFINITY)

""" maximum depth we used for our maxn agent """
SEARCH_DEPTH = 3

""" we set U = positive infinity to disable shallow pruning """
U = POSITIVE_INFINITY


class MaxnAgent:

    def __init__(self, depth=SEARCH_DEPTH, u=U):
        """
        initialize maxn agent
        :param depth: search depth
        :param u: shallow pruning threshold
        """
        self.depth = depth
        self.u = u

    def get_next_action(self, state, player, eval_index=0, opponent_index=0):
        """
        an interface provide for outside object to perform maxn search
        :param state: input state
        :param player: player object contains information parameter
        :param eval_index: player used evaluation function unique identifier
        :param opponent_index: opponent used evaluation function unique
                               identifier
        :return: searched action result
        """
        next_state, best = self.maxn(state, self.depth, state.playing_player,
                                     NEGATIVE_INFINITY, player, eval_index,
                                     opponent_index)
        assert next_state is not None
        return next_state.action

    def maxn(self, s, depth, root_player, alpha, player, eval_index=0,
             opponent_index=0):
        """
        perform maxn with depth and game termination cutoff; player and opponent
        oriented evaluation function; draw avoidance; optimized with lazy
        evaluation
        :param s: state
        :param depth: search depth left
        :param root_player: the player query the agent
        :param alpha: the maximum searched result by evaluation function
        :param player: player object
        :param eval_index: root player used evaluation identifier
        :param opponent_index: opponent players used evaluation identifier
        :return: searched result state
        """
        # result stare
        my_next_state = None

        # cut off test
        if (depth <= 0) or ((depth < self.depth) and s.is_terminate(player)):
            # evaluation value for three player
            res = []
            for i in range(0, 3):
                # lazy evaluation
                if i == s.playing_player:
                    # our player don't want to draw so early because we believe
                    # our agent can afford the result of not making the best
                    # choice
                    if player.states_counter[s.snap()] == PLAYER_WIN_THRESHOLD:
                        res.append(MIN_EVALUATION_VALUE)
                    elif i == root_player:
                        res.append(s.evaluate(i, player.choose_eval(eval_index),
                                              player))
                    else:
                        res.append(s.evaluate(i, player.choose_eval(
                            opponent_index)))
                else:
                    res.append(None)
            return None, res

        # best search result for one branch
        best = [NEGATIVE_INFINITY for _ in np.arange(0, N_PLAYER)]
        cur_player = s.playing_player

        # start search each child
        next_states = s.all_next_state()
        for next_state in next_states:
            next_player = next_state.playing_player

            # step down
            _, result = self.maxn(next_state, depth - 1, root_player,
                                  best[next_player], player, eval_index,
                                  opponent_index)

            # lazy evaluation
            if result[cur_player] is None:
                # doesn't want to draw so early
                if player.states_counter[next_state.snap()] == \
                        PLAYER_WIN_THRESHOLD:
                    result[cur_player] = MIN_EVALUATION_VALUE
                elif cur_player == root_player:
                    result[cur_player] = next_state.evaluate(
                        cur_player, player.choose_eval(eval_index), player)
                else:
                    result[cur_player] = next_state.evaluate(
                        cur_player, player.choose_eval(opponent_index))

            # compare choice
            if result[cur_player] > best[cur_player]:
                best = result
                # choose next state for our player
                if (depth == self.depth) and (cur_player == root_player):
                    my_next_state = next_state

            # shallow pruning is not used as we set U = positive infinity
            if result[cur_player] >= U - alpha:
                return next_state, result

        return my_next_state, best
