"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-4-14 23:26:22
Description: agent make random move
"""
from numpy.random import choice


class RandomAgent:

    def get_next_action(self, state):
        next_state = choice(state.all_next_state())
        return next_state.action
