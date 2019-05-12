"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-5-12 11:06:22
Description: 
"""

from .MaxnAgent import MaxnAgent
from deep_dark_fantastic_boys_next_door.Constants import (OPEN_GAME_AGENT,
                                                          OPEN_GAME_TURN_LIMIT,
                                                          NEGATIVE_INFINITY)


class HumanStartMaxnAgent(MaxnAgent):
    SEARCH_DEPTH = 3

    def get_next_action(self, state, player):
        if state.turns < OPEN_GAME_TURN_LIMIT:
            return OPEN_GAME_AGENT[state.playing_player][state.turns]
        else:
            return super().get_next_action(state, player)
