"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-11 21:33:12
Description: Player class
"""

from Board import Board
# from MaxnAgent import MaxnAgent


class Player:
    # TODO lower case or upper case or sting
    PLAYER_ORDER = {'red': 0, 'green': 1, 'blue': 2}

    def __init__(self, colour):
        """ Initialize a player
        :param str colour: representing the player that control this game
        """
        self.colour = colour
        self.my_player = Player.PLAYER_ORDER[self.colour]
        self.board = Board(self.my_player)

        # self.agent = MaxnAgent(self.board)

    def action(self, turn):
        """ Perform the agent's action
        :param 
        """
        # return self.agent.get_next_move(turn)

    def update(self, action):
        """ Update opponent's action
        :param action
        """
        self.board.update_action(action)
