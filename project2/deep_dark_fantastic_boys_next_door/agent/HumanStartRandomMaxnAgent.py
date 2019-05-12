"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-5-12 20:35:19
Description: 
"""

from .RandomMaxnAgent import RandomMaxnAgent
from deep_dark_fantastic_boys_next_door.Constants import (OPEN_GAME_AGENT,
                                                          OPEN_GAME_TURN_LIMIT,
                                                          NEGATIVE_INFINITY)


class HumanStartRandomMaxnAgent(RandomMaxnAgent):
    SEARCH_DEPTH = 3

    def __init__(self, depth=SEARCH_DEPTH):
        super().__init__(depth)

    def get_next_action(self, state, player):
        if state.turns < OPEN_GAME_TURN_LIMIT:
            return OPEN_GAME_AGENT[state.playing_player][state.turns]
        else:
            return super().get_next_action(state, player)
