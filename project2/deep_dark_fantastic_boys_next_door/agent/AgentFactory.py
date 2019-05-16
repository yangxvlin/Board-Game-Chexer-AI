"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-5-11 23:39:35
Description: create Agent
"""

from .MaxnAgent import MaxnAgent
from .RandomAgent import RandomAgent
from .GreedyAgent import GreedyAgent
from .ParanoidAgent import ParanoidAgent
from .RandomMaxnAgent import RandomMaxnAgent
from .MoZiAgent import MoZiAgent
from .HumanAgent import HumanAgent


class AgentFactory:

    @staticmethod
    def create_agent(agent_type, **kwargs):
        if agent_type == 0:
            return MaxnAgent(kwargs["depth"], float('inf'))
        elif agent_type == 1:
            return RandomAgent()
        elif agent_type == 2:
            return GreedyAgent()
        elif agent_type == 4:
            return ParanoidAgent(kwargs["depth"])
        elif agent_type == 5:
            return RandomMaxnAgent(kwargs["depth"])
        elif agent_type == 6:
            return MoZiAgent(kwargs["upstream"], kwargs["downstream"], kwargs["depth"])
        elif agent_type == 7:
            return HumanAgent(kwargs["upstream"], kwargs["downstream"], kwargs["depth"])
        else:
            return RandomAgent()
