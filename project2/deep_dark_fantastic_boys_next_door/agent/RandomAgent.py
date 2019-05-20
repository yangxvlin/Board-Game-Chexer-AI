"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-4-14 23:26:22
Description: agent make random move
"""

from numpy.random import choice


class RandomAgent:

    def get_next_action(self, state, player):
        """"
        an interface provide for outside object to perform random choice
        :param state: input state
        :param player: player object contains information parameter
        :return: randomly chosen searched action result
        """
        next_actions = state.all_next_action()
        return next_actions[choice(len(next_actions))]
