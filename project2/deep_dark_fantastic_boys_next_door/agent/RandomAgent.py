"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-4-14 23:26:22
Description: agent make random move (not adapted)
"""
from numpy.random import choice


class RandomAgent:

    def get_next_action(self, state, player):
        # print(state.all_next_action())
        next_actions = state.all_next_action()
        return next_actions[choice(len(next_actions))]
