"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-5-11 23:39:35
Description: create Agent
"""

from .MaxnAgent import MaxnAgent
from .RandomAgent import RandomAgent
from .GreedyAgent import GreedyAgent


class AgentFactory:

    @staticmethod
    def create_agent(agent_type, **kwargs):
        if agent_type == 0:
            return MaxnAgent(kwargs["depth"], float('inf'))
        elif agent_type == 1:
            return RandomAgent()
        elif agent_type == 2:
            return GreedyAgent()
        else:
            return RandomAgent()
