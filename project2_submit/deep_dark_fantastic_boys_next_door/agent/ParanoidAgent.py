"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-11 22:33:05
Description: paranoid agent with alpha-beta pruning (not adapted)
             https://project.dke.maastrichtuniversity.nl/games/files/phd/Nijssen_thesis.pdf
"""

from deep_dark_fantastic_boys_next_door.Constants import (NEGATIVE_INFINITY,
                                                          POSITIVE_INFINITY)


class ParanoidAgent:
    SEARCH_DEPTH = 4

    def __init__(self, depth=SEARCH_DEPTH):
        self.depth = depth

    def get_next_action(self, state, player):
        # print(">>>>", self.depth)
        next_state, alpha = self.paranoid(state,
                                          self.depth,
                                          state.playing_player,
                                          state.playing_player,
                                          NEGATIVE_INFINITY,
                                          POSITIVE_INFINITY,
                                          player)
        # print("#####", self.depth)
        # print(">>>> ", state.evaluate(state.playing_player, player.choose_eval()), "->", next_state.evaluate(state.playing_player, player.choose_eval()), alpha)
        assert next_state is not None
        return next_state.action

    def paranoid(self, s, depth, cur_player, root_player, alpha, beta, player):
        # s:cur state

        my_next_state = None

        if depth <= 0 or s.is_terminate(player):
            # print(">>>>>")
            # if currentPlayer == rootPlayer then
            if cur_player == root_player:
                return s, s.evaluate(root_player, player.choose_eval())
            else:
                return s, -s.evaluate(root_player, player.choose_eval())

        next_states = s.all_next_state()
        for next_state in next_states:
            next_player = next_state.playing_player

            # print(depth, cur_player, "->", next_player, "{:30s}".format(str(next_state.action)), "{:.4f}".format(next_state.evaluate(root_player, player.choose_eval())), [alpha, beta])

            # TODO max & np.max
            # if currentPlayer == rootPlayer or nextPlayer == rootPlayer then
            #     α = max(α, –ALPHABETA(c, depth–1, nextPlayer, −β, −α));
            # else
            #     α = max(α, ALPHABETA(c, depth–1, nextPlayer, α, β));
            # end if
            if cur_player == root_player or next_player == root_player:
                _, next_alpha = self.paranoid(next_state, depth - 1, next_player, root_player, -beta, -alpha, player)
                next_alpha = -next_alpha
            else:
                _, next_alpha = self.paranoid(next_state, depth - 1, next_player, root_player, alpha, beta, player)
            # alpha = max(alpha, next_alpha)
            if next_alpha > alpha:
                alpha = next_alpha
                my_next_state = next_state

            if alpha >= beta:
                # my_next_state = next_state
                return my_next_state, beta

        return my_next_state, alpha



