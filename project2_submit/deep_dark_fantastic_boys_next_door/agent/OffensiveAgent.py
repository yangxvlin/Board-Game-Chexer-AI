"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-12 11:14:03
Description: Offensive Agent (not adapted)
             https://www.aaai.org/ocs/index.php/IJCAI/IJCAI-09/paper/viewFile/507/728
"""
from Agent import Agent
import numpy as np


class OffensiveAgent(Agent):
    SEARCH_DEPTH = 3  # as we only consider to attack

    # TODO sum of the values for all players has a fixed upper bound
    U = 12  # 12 for 12 pieces on board

    def __init__(self, board, target_player, depth=SEARCH_DEPTH):
        self.board = board  # copy board for ai search
        self.target_player = target_player
        self.depth = depth

    def get_next_move(self):
        next_move, _ = self.offensive(self.board.get_current_state(), self.depth, self.board.get_playing_player(),
                                      Agent.NEGATIVE_INFINITY)

        return next_move

    # TODO check my recursion return correct move
    def offensive(self, s, depth, cur_player, alpha):
        # s:cur state
        next_move = None

        if self.board.is_terminate(s) or depth <= 0:
            return next_move, self.board.evaluate_player_state(cur_player, s)

        if self.board.is_my_player_playing(cur_player):
            # min node for leading player
            best = [Agent.POSITIVE_INFINITY for _ in np.arange(0, self.board.N_PLAYER)]
        else:
            # max node
            best = [Agent.NEGATIVE_INFINITY for _ in np.arange(0, self.board.N_PLAYER)]

        possible_moves = self.board.get_all_moves(s)

        for possible_move in possible_moves:
            next_state = self.board.get_next_state(s, possible_move)
            next_player = self.board.get_cur_player(next_state)

            _, result = self.offensive(next_state,
                                       depth - 1,
                                       next_player,
                                       best[next_player])

            # max node
            if self.board.is_my_player_playing(cur_player):
                if result[cur_player] > best[cur_player]:
                    best = result

                if result[cur_player] >= self.U - alpha:
                    return next_move, result
            # min node
            else:
                if result[self.target_player] < best[self.target_player]:
                    best = result

                    next_move = possible_move

        return next_move, best
