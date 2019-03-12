"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-11 22:08:28
Description: max^n agent with shadow pruning
             https://project.dke.maastrichtuniversity.nl/games/files/phd/Nijssen_thesis.pdf
"""
from Agent import Agent
import numpy as np


class MaxnAgent(Agent):
    SEARCH_DEPTH = 4

    # TODO sum of the values for all players has a fixed upper bound
    U = 12  # 12 for 12 pieces on board

    def __init__(self, board, depth=SEARCH_DEPTH):
        self.board = board  # copy board for ai search
        self.depth = depth

    def get_next_move(self):
        next_move, _ = self.maxn(self.board.get_current_state(), self.depth, self.board.get_playing_player(),
                                 Agent.NEGATIVE_INFINITY)

        return next_move

    # TODO check my recursion return correct move
    def maxn(self, s, depth, cur_player, alpha):
        # s:cur state
        next_move = None

        if self.board.is_terminate(s) or depth <= 0:
            return next_move, self.board.evaluate_state(s)

        best = [Agent.NEGATIVE_INFINITY for _ in np.arange(0, self.board.N_PLAYER)]

        possible_moves = self.board.get_all_moves(s)

        for possible_move in possible_moves:
            next_state = self.board.get_next_state(s, possible_move)
            next_player = self.board.get_cur_player(next_state)

            _, result = self.maxn(next_state,
                                  depth - 1,
                                  next_player,
                                  best[next_player])
            if result[cur_player] > best[cur_player]:
                best = result

                # TODO place need check
                # our player
                if self.board.is_my_player_playing(cur_player):
                    next_move = possible_move

            if result[cur_player] >= self.U - alpha:
                return next_move, result

        return next_move, best
