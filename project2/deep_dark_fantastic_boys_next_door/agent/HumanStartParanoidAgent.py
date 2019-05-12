"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-5-12 16:32:19
Description: 
"""

from .ParanoidAgent import ParanoidAgent


from deep_dark_fantastic_boys_next_door.Constants import (OPEN_GAME_AGENT,
                                                          OPEN_GAME_TURN_LIMIT,
                                                          NEGATIVE_INFINITY)


class HumanStartParanoidAgent(ParanoidAgent):
    SEARCH_DEPTH = 3

    def __init__(self, depth):
        super().__init__(depth)

    def get_next_action(self, state, player):
        if state.turns < OPEN_GAME_TURN_LIMIT:
            return OPEN_GAME_AGENT[state.playing_player][state.turns]
        else:
            return super().get_next_action(state, player)
