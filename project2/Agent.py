"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-11 21:31:22
Description: Agent abstract class
"""
from abc import abstractmethod, ABCMeta


class Agent(metaclass=ABCMeta):
    NEGATIVE_INFINITY = float('-inf')
    POSITIVE_INFINITY = float('inf')

    @abstractmethod
    def get_next_move(self):
        pass
