"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-11 21:33:12
Description: Player class (planned)
"""

from Board import Board
from MaxnAgent import MaxnAgent


class Player:

    def __init__(self, colour):
        """ Initialize a player
        :param str colour: representing the player that control this game
        """
        self.colour = colour
        self.board = Board()

        self.agent = MaxnAgent(self.board)

        # self.my_player =  # give an index

    def action(self):
        """ Perform the agent's action
        :param 
        """
        return self.agent.get_next_move()

    def update(self, action):
        """ Update opponent's action
        :param action
        """
        self.board.update_action(action)

    def get_board(self):
        return self.board
