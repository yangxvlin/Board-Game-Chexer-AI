"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-11 22:42:08
Description: MP Mixed agent (not adapted)
             https://www.aaai.org/ocs/index.php/IJCAI/IJCAI-09/paper/viewFile/507/728
"""
from Agent import Agent
import numpy as np

from MaxnAgent import MaxnAgent
from OffensiveAgent import OffensiveAgent
from ParanoidAgent import ParanoidAgent


class MPMixedAgent(Agent):
    DEFENSIVE_THRESHOLDS = 4  # be careful
    OFFENSIVE_THRESHOLDS = 5  # attack that leading player next door (:3_ヽ)_

    def __init__(self, board):
        self.board = board  # copy board for ai search
        self.strategy = None

    def get_next_move(self):
        pass

    def mp_mixed(self, defensive_thresholds, offensive_thresholds):
        player_state_values = []

        for i in range(0, self.board.N_PLAYER):
            player_state_values.append(self.board.evaluate_player_state(i))

        first_max, second_max, _ = sorted(player_state_values, reverse=True)
        leading_edge = first_max - second_max
        leading_player = np.argmax(np.array(player_state_values))

        # if (leader = root player) then
        if self.board.is_my_player_playing(leading_player):
            if leading_edge >= defensive_thresholds:
                # paranoid
                self.strategy = ParanoidAgent(self.board)
                return self.strategy.get_next_move()
        else:
            if leading_edge >= offensive_thresholds:
                # only be offensive when our player is not leading
                assert leading_player != self.board.get_playing_player()

                # offensive
                self.strategy = OffensiveAgent(self.board, leading_player)

        # max n
        self.strategy = MaxnAgent(self.board)
        return self.strategy.get_next_move()
