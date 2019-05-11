"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-5-9 17:20:06
Description: 
"""

from .MaxnAgent import MaxnAgent


class GreedyAgent:
    SEARCH_DEPTH = 1

    def __init__(self):
        self.agent = MaxnAgent(GreedyAgent.SEARCH_DEPTH)

    def get_next_action(self, state, player):
        return self.agent.get_next_action(state, player)
